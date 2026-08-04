import asyncio
import json
import types


class FakeRequest:
    """Mock thay cho starlette Request; endpoint chỉ truy cập req.client.host."""

    def __init__(self, host="127.0.0.1"):
        self.client = types.SimpleNamespace(host=host)


def _collect_sse(response):
    """Consume a StreamingResponse body and parse SSE blocks into [(event, data), ...]."""

    async def _consume():
        raw = ""
        async for chunk in response.body_iterator:
            if isinstance(chunk, bytes):
                raw += chunk.decode("utf-8")
            else:
                raw += chunk
        return raw

    raw = asyncio.run(_consume())
    events = []
    for block in raw.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        event_name = "message"
        data = {}
        for line in block.split("\n"):
            if line.startswith("event: "):
                event_name = line[len("event: "):]
            elif line.startswith("data: "):
                data = json.loads(line[len("data: "):])
        events.append((event_name, data))
    return events


def test_chat_openai_endpoint_streams_meta_delta_sources_done(monkeypatch):
    import api.routes.chat_openai as chat_route
    from core.schema import RetrievedDocument

    chat_route.sessions.clear()

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

    async def fake_stream_answer(context: str, question: str):
        assert "NMK Architects" in context
        assert question == "Thông tin công ty"
        yield "NMK Architects "
        yield "là công ty "
        yield "tư vấn kiến trúc."

    monkeypatch.setattr(chat_route, "hybrid_retrieve", fake_hybrid_retrieve)
    monkeypatch.setattr(chat_route, "stream_answer_async", fake_stream_answer)
    monkeypatch.setattr(chat_route, "get_bm25", lambda: object())
    monkeypatch.setattr(chat_route, "get_reranker", lambda: None)

    response = asyncio.run(
        chat_route.chat_openai_endpoint(
            chat_route.ChatRequest(query="Thông tin công ty"),
            FakeRequest(),
        )
    )

    assert response.media_type == "text/event-stream"

    events = _collect_sse(response)
    event_names = [name for name, _ in events]

    assert event_names == ["meta", "delta", "delta", "delta", "sources", "done"]

    _, meta_data = events[0]
    assert meta_data["session_id"]

    deltas = "".join(data["delta"] for name, data in events if name == "delta")
    assert deltas == "NMK Architects là công ty tư vấn kiến trúc."

    sources_data = next((data for name, data in events if name == "sources"), {})
    assert sources_data["sources"][0]["metadata"] == {
        "source": "companyInfo.json",
        "type": "company_info",
    }

    _, done_data = events[-1]
    assert done_data["answer"] == "NMK Architects là công ty tư vấn kiến trúc."
    assert done_data["session_id"] == meta_data["session_id"]

    # Session saved with the full answer after streaming completes
    saved = chat_route.sessions[meta_data["session_id"]][0]
    assert saved["question"] == "Thông tin công ty"
    assert saved["answer"] == "NMK Architects là công ty tư vấn kiến trúc."
    assert saved["sources"][0]["metadata"] == {
        "source": "companyInfo.json",
        "type": "company_info",
    }


def test_chat_openai_endpoint_streams_not_found_when_no_documents(monkeypatch):
    import api.routes.chat_openai as chat_route

    chat_route.sessions.clear()

    monkeypatch.setattr(chat_route, "hybrid_retrieve", lambda question, bm25: [])
    monkeypatch.setattr(chat_route, "get_bm25", lambda: object())
    monkeypatch.setattr(chat_route, "get_reranker", lambda: None)

    response = asyncio.run(
        chat_route.chat_openai_endpoint(
            chat_route.ChatRequest(query="Câu hỏi không có dữ liệu"),
            FakeRequest(),
        )
    )

    events = _collect_sse(response)
    event_names = [name for name, _ in events]

    assert event_names == ["meta", "delta", "sources", "done"]

    _, meta_data = events[0]
    _, delta_data = events[1]
    _, sources_data = events[2]
    _, done_data = events[3]

    assert delta_data["delta"] == "Tôi không tìm thấy thông tin phù hợp trong dữ liệu hiện có."
    assert sources_data["sources"] == []
    assert done_data["answer"] == delta_data["delta"]
    assert done_data["session_id"] == meta_data["session_id"]


def test_chat_openai_endpoint_uses_reranker_when_available(monkeypatch):
    import api.routes.chat_openai as chat_route
    from core.schema import RetrievedDocument

    class FakeReranker:
        def __init__(self):
            self.calls = []

        def rerank(self, query, documents, top_k=None):
            self.calls.append((query, top_k))
            return documents[:top_k]

    fake_reranker = FakeReranker()

    def fake_hybrid_retrieve(question, bm25):
        assert question == "Dự án quán cà phê"
        return [
            RetrievedDocument(id=f"doc-{i}", score=0.9, text=f"Nội dung dự án {i}", metadata={})
            for i in range(7)
        ]

    async def fake_stream_answer(context: str, question: str):
        assert question == "Dự án quán cà phê"
        yield "Đã trả lời."

    monkeypatch.setattr(chat_route, "hybrid_retrieve", fake_hybrid_retrieve)
    monkeypatch.setattr(chat_route, "stream_answer_async", fake_stream_answer)
    monkeypatch.setattr(chat_route, "get_bm25", lambda: object())
    monkeypatch.setattr(chat_route, "get_reranker", lambda: fake_reranker)

    response = asyncio.run(
        chat_route.chat_openai_endpoint(
            chat_route.ChatRequest(query="Dự án quán cà phê"),
            FakeRequest(),
        )
    )

    events = _collect_sse(response)
    sources_data = next(data for name, data in events if name == "sources")

    assert fake_reranker.calls[0][0] == "Dự án quán cà phê"
    assert fake_reranker.calls[0][1] == chat_route.RERRANKING_TOP_K
    assert len(sources_data["sources"]) == chat_route.RERRANKING_TOP_K


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


def test_check_rate_limit_sliding_window(monkeypatch):
    import api.routes.chat_openai as chat_route

    fake_time = [1_000_000.0]
    monkeypatch.setattr(chat_route.time, "time", lambda: fake_time[0])

    for _ in range(60):
        assert chat_route.check_rate_limit("10.0.0.1") is True
    assert chat_route.check_rate_limit("10.0.0.1") is False

    fake_time[0] += 61
    assert chat_route.check_rate_limit("10.0.0.1") is True
