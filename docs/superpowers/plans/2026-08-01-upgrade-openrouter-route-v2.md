# Nâng cấp luồng OpenRouter lên v2 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đưa endpoint `POST /api/chat/openai` lên chuẩn v2 (hybrid retrieval + BM25 + reranker + ContextBuilder) trong khi vẫn dùng OpenRouter qua OpenAI Agents SDK, và cập nhật tài liệu theo trạng thái thật.

**Architecture:** `chat_openai.py` sẽ đi theo luồng giống `chat.py` đã v2: lấy BM25/reranker từ `core.startup`, gọi `hybrid_retrieve()`, rerank, build context bằng `ContextBuilder` — nhưng vẫn gọi `generate_answer_async()` (OpenRouter). `chat.py` chỉ thay phần ghép context tay bằng `ContextBuilder`. `generator_openai.py`, `retriever.py`, `core/startup.py`, `vectorstore/*`, `frontend/*` không đổi.

**Tech Stack:** Python 3.12+, FastAPI, Pydantic, OpenAI Agents SDK, OpenRouter, pytest.

## Global Constraints

- Không commit trừ khi người dùng yêu cầu rõ ràng (mọi bước commit bị bỏ qua).
- Không đọc hoặc in nội dung `.env` / API key.
- Tài liệu markdown viết tiếng Việt có dấu; thuật ngữ kỹ thuật (RAG, LLM, chunking, Qdrant, OpenRouter, BM25, reranker) giữ nguyên.
- Mỗi file markdown được sửa phải thêm dòng mới vào mục `Nhật Ký Cập Nhật` với giờ Việt Nam (UTC+7) tại thời điểm thực hiện cập nhật (ngày 2026-08-01, giờ hiện tại khoảng 20:14 +07).
- Chạy lệnh bằng `uv run` (tuyệt đối không `python3`).
- Test không gọi Qdrant thật, OpenRouter thật hoặc cần API key thật.
- Code viết tiếng Anh, không emoji.
- Chỉ sửa đúng các file liệt kê trong task; không refactor code không liên quan.

---

### Task 1: Viết lại test cho route `/api/chat/openai` theo luồng v2 (RED)

**Files:**
- Modify: `tests/test_api_chat_openai.py` (thay toàn bộ nội dung)

**Interfaces:**
- Consumes: chưa cần (test sẽ fail vì route chưa có tham số `req`, chưa có `check_rate_limit`, chưa import `get_bm25`).
- Produces: 3 test functions xác định hành vi kỳ vọng của `chat_openai_endpoint` v2: happy path (hybrid + reranker None), BM25 chưa sẵn sàng → 503, vượt rate limit → 429.

- [ ] **Step 1: Ghi toàn bộ nội dung mới cho `tests/test_api_chat_openai.py`**

```python
import asyncio
import types


class FakeRequest:
    """Mock thay cho starlette Request; endpoint chỉ truy cập req.client.host."""

    def __init__(self, host="127.0.0.1"):
        self.client = types.SimpleNamespace(host=host)


def test_chat_openai_endpoint_returns_answer_with_sources(monkeypatch):
    import api.routes.chat_openai as chat_route
    from core.schema import RetrievedDocument

    def fake_hybrid_retrieve(question: str, bm25):
        assert question == "Thông tin công ty"
        assert bm25 is not None
        return [
            RetrievedDocument(
                id="doc-1",
                score=0.9,
                text="NMK Architects là công ty tư vấn kiến trúc và nội thất.",
                metadata={"source": "companyInfo.json", "type": "company_info"},
            )
        ]

    async def fake_generate_answer(context: str, question: str):
        assert "NMK Architects" in context
        assert question == "Thông tin công ty"
        return "NMK Architects là công ty tư vấn kiến trúc và nội thất."

    monkeypatch.setattr(chat_route, "hybrid_retrieve", fake_hybrid_retrieve)
    monkeypatch.setattr(chat_route, "generate_answer_async", fake_generate_answer)
    monkeypatch.setattr(chat_route, "get_bm25", lambda: object())
    monkeypatch.setattr(chat_route, "get_reranker", lambda: None)

    response = asyncio.run(
        chat_route.chat_openai_endpoint(
            chat_route.ChatRequest(query="Thông tin công ty"),
            FakeRequest(),
        )
    )

    data = response.model_dump()
    assert data["answer"] == "NMK Architects là công ty tư vấn kiến trúc và nội thất."
    assert data["sources"][0]["metadata"] == {
        "source": "companyInfo.json",
        "type": "company_info",
    }
    assert data["session_id"]


def test_chat_openai_endpoint_returns_503_when_bm25_not_ready(monkeypatch):
    import api.routes.chat_openai as chat_route
    from fastapi import HTTPException

    monkeypatch.setattr(chat_route, "get_bm25", lambda: None)

    try:
        asyncio.run(
            chat_route.chat_openai_endpoint(
                chat_route.ChatRequest(query="Thông tin công ty"),
                FakeRequest(),
            )
        )
    except HTTPException as exc:
        assert exc.status_code == 503
    else:
        raise AssertionError("Expected HTTPException with status 503")


def test_chat_openai_endpoint_returns_429_when_rate_limited(monkeypatch):
    import api.routes.chat_openai as chat_route
    from fastapi import HTTPException

    monkeypatch.setattr(chat_route, "check_rate_limit", lambda client_ip: False)

    try:
        asyncio.run(
            chat_route.chat_openai_endpoint(
                chat_route.ChatRequest(query="Thông tin công ty"),
                FakeRequest(),
            )
        )
    except HTTPException as exc:
        assert exc.status_code == 429
    else:
        raise AssertionError("Expected HTTPException with status 429")
```

- [ ] **Step 2: Chạy test và xác nhận FAIL (RED)**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_chat_openai.py -q`
Expected: FAIL — ví dụ `TypeError: chat_openai_endpoint() got an unexpected keyword argument 'req'` (route hiện tại chưa có tham số `req` và chưa có `check_rate_limit`).

- [ ] **Step 3: Không commit** (theo Global Constraints).

---

### Task 2: Nâng cấp `api/routes/chat_openai.py` lên v2 (GREEN)

**Files:**
- Modify: `api/routes/chat_openai.py` (thay toàn bộ nội dung)

**Interfaces:**
- Consumes: `hybrid_retrieve(query, bm25)` từ `retrieval.hybrid_retriever`; `get_bm25()`, `get_reranker()` từ `core.startup`; `ContextBuilder()` từ `retrieval.context_builder`; `generate_answer_async(context, question)` từ `llm.generator_openai`.
- Produces: `chat_openai_endpoint(request: ChatRequest, req: Request)` — trả `ChatResponse` (answer, sources, session_id); `check_rate_limit(client_ip) -> bool`; hằng `RERRANKING_TOP_K`.

- [ ] **Step 1: Ghi toàn bộ nội dung mới cho `api/routes/chat_openai.py`**

```python
import logging
import os
import time
from typing import Optional
import uuid

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from llm.generator_openai import generate_answer_async
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


@router.post("/chat/openai", response_model=ChatResponse)
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

    try:
        # Get BM25 and Reranker from startup
        bm25 = get_bm25()
        reranker = get_reranker()

        if bm25 is None:
            logger.error(f"Session {session_id}: BM25 not initialized!")
            raise HTTPException(
                status_code=503,
                detail="Hệ thống chưa sẵn sàng. Vui lòng thử lại sau."
            )

        # Step 1: Hybrid retrieval (Dense + BM25)
        logger.info(f"Session {session_id}: Running hybrid retrieval...")
        documents = hybrid_retrieve(question, bm25)

        if not documents:
            logger.warning(f"Session {session_id}: No documents retrieved")
            return ChatResponse(
                answer="Tôi không tìm thấy thông tin phù hợp trong dữ liệu hiện có.",
                sources=[],
                session_id=session_id,
            )

        logger.info(f"Session {session_id}: Retrieved {len(documents)} documents from hybrid search")

        # Step 2: Reranking (if available)
        if reranker is not None:
            logger.info(f"Session {session_id}: Reranking documents...")
            documents = reranker.rerank(question, documents, top_k=RERRANKING_TOP_K)
            logger.info(f"Session {session_id}: After reranking: {len(documents)} documents")
        else:
            logger.warning(f"Session {session_id}: Reranker not available, using hybrid scores only")
            documents = documents[:RERRANKING_TOP_K]  # Cut to top K

        # Step 3: Build context and generate answer
        context = ContextBuilder().build(documents)
        logger.info(f"Session {session_id}: Retrieved {len(documents)} documents")

        answer = await generate_answer_async(context, question)
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

        return ChatResponse(
            answer=answer,
            sources=sources,
            session_id=session_id,
        )

    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Session {session_id}: Error in OpenRouter chat: {error}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Xin lỗi, đã xảy ra lỗi khi xử lý câu hỏi của bạn. Vui lòng thử lại sau.",
        )
```

- [ ] **Step 2: Chạy test và xác nhận PASS (GREEN)**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_chat_openai.py -q`
Expected: `3 passed`

- [ ] **Step 3: Không commit** (theo Global Constraints).

---

### Task 3: Đổi `api/routes/chat.py` sang dùng `ContextBuilder`

**Files:**
- Modify: `api/routes/chat.py`
  - Thêm import `ContextBuilder`.
  - Thay 2 chỗ ghép context tay bằng `ContextBuilder().build(documents)`.

**Interfaces:**
- Consumes: `ContextBuilder` từ `retrieval.context_builder` (class đã có, mặc định max_documents=5, max_context_length=3000, separator `\n\n---\n\n`).
- Produces: endpoint `chat_endpoint` và hàm CLI `chat(question)` vẫn giữ nguyên chữ ký, chỉ đổi cách build context.

- [ ] **Step 1: Thêm import**

Trong `api/routes/chat.py`, ngay sau dòng `from retrieval.hybrid_retriever import hybrid_retrieve`, thêm:

```python
from retrieval.context_builder import ContextBuilder
```

- [ ] **Step 2: Thay context trong `chat_endpoint`**

Thay block sau (đang ở dòng ~116-119 trong file hiện tại):

```python
        context = "\n\n".join(
            f"[{i+1}] {doc.text}\n(Nguồn: {doc.metadata})" 
            for i, doc in enumerate(documents)
        )
```

bằng:

```python
        context = ContextBuilder().build(documents)
```

- [ ] **Step 3: Thay context trong hàm CLI `chat(question)`**

Thay dòng sau (đang ở dòng ~188):

```python
        context = "\n\n".join(f"[{i+1}] {doc.text}\n(Nguồn: {doc.metadata})" for i, doc in enumerate(documents))
```

bằng:

```python
        context = ContextBuilder().build(documents)
```

- [ ] **Step 4: Kiểm tra compile và import**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile api/routes/chat.py api/routes/chat_openai.py tests/test_api_chat_openai.py`
Expected: exit 0, không có output.

- [ ] **Step 5: Chạy toàn bộ test hiện có**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/ -q`
Expected: tất cả test pass (hiện có `test_llm_generator_openai.py` và `test_api_chat_openai.py`).

- [ ] **Step 6: Không commit** (theo Global Constraints).

Ghi chú (không sửa trong task này): `chat.py` hiện raise `HTTPException(503)` bên trong khối `try`, nên sẽ bị `except Exception` bắt và trả về 500 thay vì 503. Hành vi này có sẵn trước thay đổi và nằm ngoài phạm vi task; chỉ báo cáo lại.

---

### Task 4: Cập nhật tài liệu — trạng thái pipeline hybrid đã chạy thành công

**Files:**
- Modify: `vectorstore/README_vectorstore.md`
- Modify: `ingestion/README_ingestion.md`
- Modify: `RUN_GUIDE.md`

Quy tắc chung mỗi file: thêm 1 dòng mới vào mục `Nhật Ký Cập Nhật` (đầu danh sách) với nội dung:

```text
- 2026-08-01 20:xx +07 - Cập nhật trạng thái sau khi kiểm tra log chạy thật: pipeline hybrid đã chạy thành công, collection `nmk_chatbot_collection` đã có schema hybrid và chứa 450 points; lỗi `Not existing vector name error: sparse` chỉ xảy ra ở lần chạy đầu với collection cũ dense-only.
```

(ghi đúng giờ hiện tại thay cho `20:xx`)

- [ ] **Step 1: Sửa `vectorstore/README_vectorstore.md`**

Trong mục `## Trạng Thái Chạy Hiện Tại`, thay đoạn sau:

```text
Sau cập nhật `p2/10`, người dùng đã chạy pipeline hybrid và gặp lỗi Qdrant:

Wrong input: Not existing vector name error: sparse

Theo code hiện tại, nguyên nhân là collection `nmk_chatbot_collection` đã tồn tại từ luồng dense-only cũ nên `ensure_collection()` chỉ log rồi return, không tạo lại schema có sparse vector. `upsert.py` sau đó gửi point có vector `sparse` vào collection không có vector name này, nên Qdrant trả `400 Bad Request`.
```

bằng:

```text
Sau cập nhật `p2/10`, người dùng đã chạy pipeline hybrid. Lần chạy đầu gặp lỗi Qdrant `Wrong input: Not existing vector name error: sparse` vì collection cũ dense-only chưa có vector name `sparse`. Sau khi xoá collection cũ, pipeline chạy lại thành công theo log thực tế:

- Collection `nmk_chatbot_collection` được tạo lại với named vector `dense` (384, cosine) và sparse vector `sparse`.
- `SparseEmbedder` fit trên 450 documents, vocabulary size 1486.
- `build_hybrid_qdrant_points()` build 450 hybrid Qdrant points.
- `upsert_chunks()` upsert 450 hybrid points vào collection.
- `run_ingestion_pipeline()` log `Upserted 450 chunks into the vector store`.
```

Sau đó thay đoạn cuối mục (bắt đầu bằng `Để upsert thật thành công...`):

```text
Để upsert thật thành công với code hiện tại, collection trong Qdrant phải có named vector `dense` và sparse vector `sparse`. Nếu còn collection dense-only cũ, cần xoá collection cũ hoặc dùng collection name mới trước khi chạy lại pipeline.
```

bằng:

```text
Trạng thái hiện tại: collection `nmk_chatbot_collection` trong Qdrant local đã có đúng schema hybrid (named vector `dense` + sparse vector `sparse`) và chứa 450 hybrid points theo log chạy pipeline. Nếu sau này chạy lại pipeline khi collection đang giữ schema cũ dense-only, cần xoá collection cũ trước để `ensure_collection()` tạo lại đúng schema hybrid.
```

Thêm dòng Nhật Ký Cập Nhật (theo quy tắc chung).

- [ ] **Step 2: Sửa `ingestion/README_ingestion.md`**

Trong mục `## Cách Hoạt Động Hiện Tại`, thay đoạn sau:

```text
Sau cập nhật `p2/10`, kiểm tra tĩnh hiện tại đã pass:
```

không đổi, nhưng thay đoạn ngay sau nó:

```text
Nếu collection cũ dense-only vẫn tồn tại trong Qdrant local, pipeline hybrid có thể lỗi:

Wrong input: Not existing vector name error: sparse

Nguyên nhân là `ensure_collection()` chỉ bỏ qua khi collection đã tồn tại, không tự migrate schema. Cần xoá collection cũ hoặc đổi tên collection, rồi chạy lại pipeline để Qdrant tạo collection có named vector `dense` và sparse vector `sparse`.
```

bằng:

```text
Người dùng đã chạy pipeline hybrid và upsert thành công theo log thực tế: collection `nmk_chatbot_collection` được tạo lại với named vector `dense` và sparse vector `sparse`, 450 hybrid points được build và upsert, pipeline log `Upserted 450 chunks into the vector store`. Lỗi `Not existing vector name error: sparse` chỉ xảy ra ở lần chạy đầu khi collection cũ dense-only chưa được xoá; sau khi xoá collection cũ, luồng chạy thành công.
```

Thêm dòng Nhật Ký Cập Nhật (theo quy tắc chung).

- [ ] **Step 3: Sửa `RUN_GUIDE.md`**

Trong mục `## 2. Nạp Dữ Liệu Vào Qdrant`, sau block lỗi:

```text
Nếu gặp lỗi:

Wrong input: Not existing vector name error: sparse

nguyên nhân là Qdrant đang giữ collection cũ dense-only. Xóa collection cũ hoặc đổi `vector_database.collection_name`, sau đó chạy lại pipeline để collection được tạo lại đúng schema hybrid.
```

thêm đoạn trạng thái hiện tại:

```text
Trạng thái hiện tại: pipeline hybrid đã chạy thành công; collection `nmk_chatbot_collection` đang có schema hybrid (named vector `dense` + sparse vector `sparse`) và chứa 450 points. Block lỗi phía trên là hướng dẫn khắc phục nếu chạy lại với collection cũ.
```

Thêm dòng Nhật Ký Cập Nhật (theo quy tắc chung).

- [ ] **Step 4: Kiểm tra tài liệu**

Run: `grep -c "Nhật Ký Cập Nhật" vectorstore/README_vectorstore.md ingestion/README_ingestion.md RUN_GUIDE.md` và đọc lại các đoạn vừa sửa để xác nhận không còn mô tả lỗi sparse là trạng thái hiện tại.

- [ ] **Step 5: Không commit** (theo Global Constraints).

---

### Task 5: Cập nhật tài liệu — trạng thái code sau khi nâng cấp OpenRouter route

**Files:**
- Modify: `report/Project_status.md`
- Modify: `README.md` (thư mục gốc)
- Modify: `api/routes/README_routes.md`
- Modify: `api/README_api.md`
- Modify: `retrieval/README_retrieval.md`
- Modify: `tests/README_tests.md`
- Modify: `report/README_report.md`

Quy tắc chung mỗi file: thêm dòng mới vào mục `Nhật Ký Cập Nhật` với giờ hiện tại (UTC+7) mô tả ngắn nội dung cập nhật.

- [ ] **Step 1: Sửa `report/Project_status.md`**

1. Thêm dòng Nhật Ký Cập Nhật:
```text
- 2026-08-01 20:xx +07 - Cập nhật trạng thái sau khi nâng cấp `/api/chat/openai` lên v2 (hybrid retrieval + BM25 + reranker + ContextBuilder, vẫn dùng OpenRouter qua OpenAI Agents SDK) và ghi nhận pipeline hybrid đã chạy thành công với collection hybrid 450 points.
```

2. Trong mục `## Trạng Thái Chạy Hiện Tại`, thay đoạn mô tả lỗi sparse (bắt đầu `Người dùng đã chạy Qdrant bằng Docker Compose và chạy lại pipeline hybrid. Log chạy pipeline đã build 450 hybrid Qdrant points nhưng upsert bị Qdrant trả lỗi:` cho tới hết đoạn `...nên Qdrant trả `400 Bad Request`.` bằng:
```text
Người dùng đã chạy Qdrant bằng Docker Compose và chạy pipeline hybrid. Lần chạy đầu upsert bị Qdrant trả lỗi `Wrong input: Not existing vector name error: sparse` vì collection cũ dense-only chưa có vector name `sparse`. Sau khi xoá collection cũ, pipeline chạy lại thành công: collection `nmk_chatbot_collection` được tạo lại với named vector `dense` (384, cosine) và sparse vector `sparse`, 450 hybrid points được build và upsert, pipeline log `Upserted 450 chunks into the vector store`. `SparseEmbedder` fit trên 450 documents với vocabulary size 1486.
```

3. Sửa câu trong `## Mốc Học Hiện Tại` (đoạn dài kết thúc bằng `...`Frontend hiện gọi `POST /api/chat/openai`.`): thay cụm `Endpoint `POST /api/chat/openai` vẫn dùng `retrieval/retriever.py` dense-only và `llm/generator_openai.py`.` bằng `Endpoint `POST /api/chat/openai` hiện dùng hybrid retrieval + BM25 + reranker + `ContextBuilder` và vẫn gọi `llm/generator_openai.py` (OpenRouter).`.

4. Trong mục `## Phần Đã Có Mã Nguồn`, thay toàn bộ mô tả `api/routes/chat_openai.py` (đoạn bắt đầu `api/routes/chat_openai.py` đã có endpoint...` cho tới `...trả `answer`, `sources`, `session_id`.` bằng:
```text
`api/routes/chat_openai.py` đã có endpoint `POST /chat/openai`. Vì `api/app.py` đăng ký router với prefix `/api`, endpoint đầy đủ là `POST /api/chat/openai`. Route nhận `query` và `session_id`, kiểm tra rate limit in-memory theo IP, lấy BM25/reranker từ `core.startup`, gọi `hybrid_retrieve(question, bm25)`, rerank document nếu reranker sẵn sàng, build context bằng `ContextBuilder`, gọi `await generate_answer_async(context, question)` từ `llm/generator_openai.py`, lưu session trong memory và trả `answer`, `sources`, `session_id`. Nếu BM25 chưa khởi tạo, route trả `503`.
```

5. Trong mục `## Phần Đã Có Mã Nguồn`, cập nhật mô tả `api/routes/chat.py`: thay cụm `tự build context từ document truy xuất được` bằng `build context bằng `ContextBuilder`` (đoạn mô tả `chat.py` hiện có nội dung `...tự build context từ document truy xuất được, gọi `generate_answer(context, question)`...`).

6. Trong mục `## Quyết Định Kỹ Thuật Hiện Tại` (đoạn dài cuối cùng, bắt đầu `Dữ liệu được xử lý theo hướng tách bảng...`), thay cụm `Endpoint `POST /api/chat/openai` vẫn dùng retrieval dense-only và OpenRouter.` bằng `Endpoint `POST /api/chat/openai` hiện dùng hybrid retrieval + BM25 + reranker + `ContextBuilder` và vẫn dùng OpenRouter.`. Đồng thời thay cụm `ContextBuilder` vẫn chưa được route dùng.` bằng `ContextBuilder` hiện được cả hai route chat dùng.`.

7. Cập nhật mục `## Trạng Thái Dữ Liệu Hiện Tại`: thay câu cuối `Qdrant local hiện có dữ liệu được lưu trong `qdrant_storage/`...Sau cập nhật `p2/2`, code chunking đã đổi thành phần chunk nhưng chưa chạy lại ingestion để thay thế dữ liệu trong Qdrant trong phiên kiểm tra này.` bằng:
```text
Qdrant local hiện có dữ liệu trong `qdrant_storage/` do Docker Compose mount. Collection `nmk_chatbot_collection` hiện có schema hybrid (named vector `dense` + sparse vector `sparse`) và chứa 450 hybrid points theo log chạy pipeline hybrid.
```

- [ ] **Step 2: Sửa `README.md` (thư mục gốc)**

1. Thêm dòng Nhật Ký Cập Nhật:
```text
- 2026-08-01 20:xx +07 - Cập nhật trạng thái sau khi nâng cấp `/api/chat/openai` lên v2 (hybrid + BM25 + reranker + ContextBuilder, vẫn OpenRouter) và ghi nhận pipeline hybrid đã chạy thành công với collection hybrid 450 points.
```

2. Trong mục `### `qdrant_storage``: thay câu `Sau cập nhật `p2/10`, pipeline hiện upsert hybrid points dense+sparse. Nếu collection cũ dense-only vẫn còn trong Qdrant local, cần xoá collection cũ để pipeline tạo lại collection hybrid đúng schema.` bằng `Sau cập nhật `p2/10`, pipeline upsert hybrid points dense+sparse và đã chạy thành công: collection `nmk_chatbot_collection` hiện có schema hybrid và chứa 450 points.`

3. Trong mục `## Lệnh Chạy Dự Án Bằng `uv``, thay đoạn `Sau cập nhật `p2/10`, pipeline sẽ build/upsert hybrid points. Nếu Qdrant đang giữ collection `nmk_chatbot_collection` cũ dense-only từ lần chạy trước, xoá collection đó trước rồi chạy pipeline để collection được tạo lại với named vector `dense` và sparse vector `sparse`.` bằng `Sau cập nhật `p2/10`, pipeline build/upsert hybrid points và đã chạy thành công. Nếu chạy lại khi collection đang giữ schema cũ dense-only, xoá collection đó trước để pipeline tạo lại collection với named vector `dense` và sparse vector `sparse`.`

4. Trong mục `## Lưu Ý Chạy Hiện Tại`, thay đoạn `Endpoint `POST /api/chat/openai` dùng OpenRouter đúng theo cấu hình hiện tại nhưng vẫn dùng dense retriever `retrieval/retriever.py`. Frontend hiện gọi `POST /api/chat/openai`.` bằng `Endpoint `POST /api/chat/openai` dùng OpenRouter qua OpenAI Agents SDK, đồng thời dùng hybrid retrieval + BM25 + reranker + `ContextBuilder` giống luồng v2. `retrieval/retriever.py` (dense-only) được giữ làm legacy nhưng không còn route nào gọi. Frontend hiện gọi `POST /api/chat/openai`.` Và thay cụm ``retrieval/context_builder.py` hiện đã có `ContextBuilder`, nhưng route chat hiện vẫn tự ghép context bằng `"\n\n".join(...)` và chưa dùng class này.` bằng ``retrieval/context_builder.py` đã có `ContextBuilder` và cả hai route chat (`/api/chat`, `/api/chat/openai`) hiện đều dùng class này để build context.`

- [ ] **Step 3: Sửa `api/routes/README_routes.md`**

1. Thêm dòng Nhật Ký Cập Nhật:
```text
- 2026-08-01 20:xx +07 - Cập nhật `chat_openai.py` sau khi nâng cấp lên v2: hybrid retrieval, BM25/reranker từ `core.startup`, `ContextBuilder`, rate limit in-memory; `chat.py` cũng chuyển sang `ContextBuilder`.
```

2. Cập nhật mô tả `chat_openai.py`: thay đoạn từ `Import `retrieve` từ `retrieval.retriever`.` cho tới `- `chat_openai_endpoint(request)` strip query...` bằng nội dung khớp code mới: import `hybrid_retrieve`, `get_bm25`/`get_reranker`, `ContextBuilder`, `Request`; thêm rate limit; endpoint `chat_openai_endpoint(request, req)`; luồng v2; trả 429 khi vượt rate limit và 503 khi BM25 chưa sẵn sàng.

3. Cập nhật mô tả `chat.py`: thay cụm `tự build context bằng `"\n\n".join(...)`` bằng `build context bằng `ContextBuilder``.

4. Sửa mục `## Nhiệm Vụ Của Thư Mục` nếu cần cho khớp trạng thái mới (cả 2 route giờ đều là v2 retrieval; `chat.py` dùng legacy generator, `chat_openai.py` dùng OpenRouter generator).

- [ ] **Step 4: Sửa `api/README_api.md`**

1. Thêm dòng Nhật Ký Cập Nhật tương tự bước 1 ở trên.
2. Trong mục `## Ghi Chú Kỹ Thuật`, thay đoạn `POST /api/chat/openai` hiện gọi `retrieve(question)` và `await generate_answer_async(context, question)` từ `llm/generator_openai.py`.` bằng `POST /api/chat/openai` hiện gọi `hybrid_retrieve(question, bm25)`, rerank bằng `CrossEncoderReranker` nếu startup khởi tạo được, build context bằng `ContextBuilder` và gọi `await generate_answer_async(context, question)` từ `llm/generator_openai.py`. Route này cũng có rate limit in-memory theo IP như `/api/chat`.
3. Cập nhật mô tả `app.py` (nếu mô tả route hiện nêu `retrieve`) cho khớp.

- [ ] **Step 5: Sửa `retrieval/README_retrieval.md`**

1. Thêm dòng Nhật Ký Cập Nhật:
```text
- 2026-08-01 20:xx +07 - Cập nhật trạng thái sau khi nâng cấp `/api/chat/openai` lên v2: `hybrid_retrieve()` hiện được cả hai route dùng; `ContextBuilder` được route dùng; `retriever.py` còn là legacy dense-only không route nào gọi.
```

2. Sửa mục `## Nhiệm Vụ Của Thư Mục`: thay cụm `Endpoint `POST /api/chat` hiện đã gọi `hybrid_retrieve()`, còn `POST /api/chat/openai` vẫn dùng dense retriever `retrieval/retriever.py`. Route chat hiện vẫn tự build context trong route và chưa dùng `ContextBuilder`.` bằng `Cả hai endpoint `POST /api/chat` và `POST /api/chat/openai` hiện đều gọi `hybrid_retrieve()`. Cả hai route đều build context bằng `ContextBuilder`. `retrieval/retriever.py` (dense-only) được giữ làm legacy nhưng không còn route nào gọi.`

3. Cập nhật mô tả `context_builder.py`: thay cụm `Trạng thái hiện tại: file đã có code nhưng chưa được `api/routes/chat.py`, `api/routes/chat_openai.py` hoặc generator gọi. Route `/api/chat` hiện tự ghép context bằng `"\n\n".join(...)`.` bằng `Trạng thái hiện tại: `ContextBuilder` được cả `api/routes/chat.py` và `api/routes/chat_openai.py` dùng để build context trước khi gọi generator.`

4. Cập nhật mô tả `retriever.py`: thêm câu `Trạng thái hiện tại: không còn route nào gọi hàm `retrieve()`; file được giữ làm legacy dense-only.` và cập nhật mô tả `hybrid_retriever.py` (bỏ cụm `Endpoint `POST /api/chat/openai` hiện chưa gọi file này và vẫn dùng `retrieval/retriever.py`.`).

- [ ] **Step 6: Sửa `tests/README_tests.md`**

1. Thêm dòng Nhật Ký Cập Nhật:
```text
- 2026-08-01 20:xx +07 - Cập nhật sau khi nâng cấp `/api/chat/openai` lên v2: test route giờ cover luồng hybrid + rate limit 429 + BM25 chưa sẵn sàng 503.
```

2. Cập nhật mô tả `test_api_chat_openai.py`: thay nội dung cũ bằng nội dung mới — test `chat_openai_endpoint()` với mock `hybrid_retrieve`, `get_bm25`, `get_reranker`, `generate_answer_async` và object `req` giả; thêm case 429 (rate limit) và 503 (BM25 chưa sẵn sàng); không gọi Qdrant hoặc OpenRouter thật.

3. Sửa mục `## Ghi Chú Kỹ Thuật`: thay câu `Endpoint `POST /api/chat` sau p2 đã dùng hybrid retrieval, BM25 và reranker, nhưng hiện chưa có automated test riêng trong thư mục `tests`.` bằng `Endpoint `POST /api/chat` sau p2 dùng hybrid retrieval, BM25 và reranker nhưng vẫn chưa có automated test riêng; test hiện có bao phủ luồng v2 của `POST /api/chat/openai` (hybrid, rate limit, 503).`

- [ ] **Step 7: Sửa `report/README_report.md`**

1. Thêm dòng Nhật Ký Cập Nhật:
```text
- 2026-08-01 20:xx +07 - Cập nhật mô tả `Project_status.md` sau khi nâng cấp `/api/chat/openai` lên v2 và ghi nhận pipeline hybrid chạy thành công.
```

2. Trong mục mô tả `Project_status.md`, cập nhật dòng bullet về ghi chú tích hợp (`- Ghi chú tích hợp hiện tại: /api/chat dùng hybrid/reranker nhưng gọi legacy llm/generator.py; /api/chat/openai dùng OpenRouter nhưng vẫn dense-only; frontend hiện gọi /api/chat/openai.`) thành: `/api/chat` dùng hybrid/reranker/ContextBuilder nhưng gọi legacy `llm/generator.py`; `/api/chat/openai` dùng hybrid/reranker/ContextBuilder và gọi OpenRouter qua OpenAI Agents SDK; frontend hiện gọi `/api/chat/openai`.

- [ ] **Step 8: Kiểm tra tài liệu**

Run: `rg -n "dense-only|retrieve\(question\)|chưa được route dùng|Not existing vector name" report/Project_status.md README.md api/routes/README_routes.md api/README_api.md retrieval/README_retrieval.md tests/README_tests.md report/README_report.md`
Expected: các cụm từ mô tả trạng thái cũ không còn ở những chỗ đã sửa (có thể còn ở mô tả lịch sử/nhật ký — đó là chấp nhận được).

- [ ] **Step 9: Không commit** (theo Global Constraints).

---

### Task 6: Kiểm tra tổng thể cuối cùng

**Files:** không sửa file nào; chỉ chạy kiểm tra.

- [ ] **Step 1: Compile toàn bộ file Python bị ảnh hưởng**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile api/routes/chat.py api/routes/chat_openai.py tests/test_api_chat_openai.py core/startup.py retrieval/hybrid_retriever.py retrieval/context_builder.py`
Expected: exit 0, không output.

- [ ] **Step 2: Chạy toàn bộ automated tests**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/ -q`
Expected: tất cả pass — `test_llm_generator_openai.py` (các case generator OpenRouter) và `test_api_chat_openai.py` (3 case: happy path, 503, 429).

- [ ] **Step 3: Kiểm tra import backend**

Run: `UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import api.app; print('api.app import ok')"`
Expected: `api.app import ok`

- [ ] **Step 4: Xác nhận frontend không cần sửa**

Run: `rg -n "chat/openai" frontend/lib/api.ts`
Expected: `sendMessage` vẫn gọi `${API_URL}/api/chat/openai` — frontend giữ nguyên, không sửa file.

- [ ] **Step 5: Rà soát diff**

Run: `git diff --stat`
Expected: chỉ các file code (2 file .py) và test + các file markdown theo kế hoạch; không có file ngoài phạm vi.

- [ ] **Step 6: Không commit** (theo Global Constraints). Báo cáo kết quả cho người dùng và hỏi có muốn commit không.
