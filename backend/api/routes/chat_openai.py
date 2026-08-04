import json
import logging
import os
import time
from typing import Optional
import uuid

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from llm.generator_openai import stream_answer_async
from retrieval.hybrid_retriever import hybrid_retrieve
from retrieval.context_builder import ContextBuilder
from core.startup import get_bm25, get_reranker
from core.settings_loader import load_settings

settings = load_settings()
logger = logging.getLogger("chat")
router = APIRouter()

MAX_QUERY_LENGTH = int(os.getenv("MAX_QUERY_LENGTH", "500"))
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
RERRANKING_TOP_K = settings.get("reranking", {}).get("top_k", 5)

sessions = {}
rate_limit_storage = {}


def check_rate_limit(client_ip: str) -> bool:
    """Check if client has exceeded rate limit"""
    current_time = time.time()
    minute_ago = current_time - 60

    if client_ip not in rate_limit_storage:
        rate_limit_storage[client_ip] = []

    rate_limit_storage[client_ip] = [
        ts for ts in rate_limit_storage[client_ip] if ts > minute_ago
    ]

    if len(rate_limit_storage[client_ip]) >= RATE_LIMIT_PER_MINUTE:
        return False

    rate_limit_storage[client_ip].append(current_time)
    return True


class ChatRequest(BaseModel):
    """Chat request model."""

    query: str = Field(..., min_length=1, max_length=MAX_QUERY_LENGTH, description="User's question")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")


class ChatResponse(BaseModel):
    """Chat response model."""

    answer: str = Field(..., description="Bot's answer")
    sources: list = Field(default_factory=list, description="Source documents")
    session_id: str = Field(..., description="Session ID")


def _sse_event(event: str, data: dict) -> str:
    """Format an SSE event frame."""
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@router.post("/chat/openai")
async def chat_openai_endpoint(request: ChatRequest, req: Request):
    # Rate limiting check
    client_ip = req.client.host if req.client else "unknown"
    if not check_rate_limit(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(
            status_code=429,
            detail=f"Tốc độ request quá nhanh. Vui lòng thử lại sau. (Max {RATE_LIMIT_PER_MINUTE} requests/minute)"
        )

    question = request.query.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Vui lòng nhập câu hỏi.")

    session_id = request.session_id or str(uuid.uuid4())

    logger.info(f"Session {session_id}: Received OpenRouter question: {question}")

    # Get BM25 and Reranker from startup
    bm25 = get_bm25()
    reranker = get_reranker()

    if bm25 is None:
        logger.error(f"Session {session_id}: BM25 not initialized!")
        raise HTTPException(
            status_code=503,
            detail="Hệ thống chưa sẵn sàng. Vui lòng thử lại sau."
        )

    async def event_generator():
        try:
            yield _sse_event("meta", {"session_id": session_id})

            # Step 1: Hybrid retrieval (Dense + BM25)
            logger.info(f"Session {session_id}: Running hybrid retrieval...")
            documents = hybrid_retrieve(question, bm25)

            if not documents:
                logger.warning(f"Session {session_id}: No documents retrieved")
                not_found_message = "Tôi không tìm thấy thông tin phù hợp trong dữ liệu hiện có."
                yield _sse_event("delta", {"delta": not_found_message})
                yield _sse_event("sources", {"sources": []})
                yield _sse_event("done", {"answer": not_found_message, "session_id": session_id})
                return

            logger.info(f"Session {session_id}: Retrieved {len(documents)} documents from hybrid search")

            # Step 2: Reranking (if available)
            if reranker is not None:
                logger.info(f"Session {session_id}: Reranking documents...")
                documents = reranker.rerank(question, documents, top_k=RERRANKING_TOP_K)
                logger.info(f"Session {session_id}: After reranking: {len(documents)} documents")
            else:
                logger.warning(f"Session {session_id}: Reranker not available, using hybrid scores only")
                documents = documents[:RERRANKING_TOP_K]  # Cut to top K

            # Step 3: Build context and stream answer
            context = ContextBuilder().build(documents)
            logger.info(f"Session {session_id}: Retrieved {len(documents)} documents")

            answer_parts = []
            async for delta in stream_answer_async(context, question):
                if delta:
                    answer_parts.append(delta)
                    yield _sse_event("delta", {"delta": delta})

            answer = "".join(answer_parts).strip()
            logger.info(f"Session {session_id}: Generated OpenRouter answer successfully")

            sources = [
                {
                    "text": doc.text[:200] + "..." if len(doc.text) > 200 else doc.text,
                    "metadata": doc.metadata,
                    "score": doc.score,
                }
                for doc in documents
            ]

            if session_id not in sessions:
                sessions[session_id] = []
            sessions[session_id].append({
                "question": question,
                "answer": answer,
                "sources": sources,
            })

            yield _sse_event("sources", {"sources": sources})
            yield _sse_event("done", {"answer": answer, "session_id": session_id})

        except Exception as error:
            logger.error(f"Session {session_id}: Error in OpenRouter chat: {error}", exc_info=True)
            yield _sse_event(
                "error",
                {"message": "Xin lỗi, đã xảy ra lỗi khi xử lý câu hỏi của bạn. Vui lòng thử lại sau."},
            )

    return StreamingResponse(event_generator(), media_type="text/event-stream")
