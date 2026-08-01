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
