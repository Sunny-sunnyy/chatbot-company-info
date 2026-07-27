import asyncio


def test_chat_openai_endpoint_returns_answer_with_sources(monkeypatch):
    import sys
    import types

    retrieval_module = types.ModuleType("retrieval.retriever")
    retrieval_module.retrieve = lambda question: []
    monkeypatch.setitem(sys.modules, "retrieval.retriever", retrieval_module)

    import api.routes.chat_openai as chat_route
    from core.schema import RetrievedDocument

    def fake_retrieve(question: str):
        assert question == "Thông tin công ty"
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

    monkeypatch.setattr(chat_route, "retrieve", fake_retrieve)
    monkeypatch.setattr(chat_route, "generate_answer_async", fake_generate_answer)

    response = asyncio.run(
        chat_route.chat_openai_endpoint(
            chat_route.ChatRequest(query="Thông tin công ty")
        )
    )

    data = response.model_dump()
    assert data["answer"] == "NMK Architects là công ty tư vấn kiến trúc và nội thất."
    assert data["sources"][0]["metadata"] == {
        "source": "companyInfo.json",
        "type": "company_info",
    }
    assert data["session_id"]
