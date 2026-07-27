import asyncio


def test_generate_answer_async_returns_message_for_empty_context():
    from llm.generator_openai import generate_answer_async

    answer = asyncio.run(generate_answer_async("", "Thông tin công ty"))

    assert answer == "Dữ liệu ngữ cảnh không được để trống."


def test_generate_answer_async_returns_message_for_empty_question():
    from llm.generator_openai import generate_answer_async

    answer = asyncio.run(generate_answer_async("NMK Architects", ""))

    assert answer == "Câu hỏi không được để trống."


def test_generate_answer_async_returns_message_when_openrouter_key_missing(monkeypatch):
    import llm.generator_openai as generator

    monkeypatch.setattr(generator, "MODEL_PROVIDER", "openrouter")
    monkeypatch.setattr(generator, "OPENROUTER_API_KEY", None)

    answer = asyncio.run(generator.generate_answer_async("NMK Architects", "Thông tin công ty"))

    assert answer == "Thiếu cấu hình API key cho OpenRouter."


def test_generate_answer_async_openrouter_uses_runner(monkeypatch):
    import llm.generator_openai as generator

    class FakeResult:
        final_output = "Câu trả lời từ OpenRouter"

    async def fake_run(agent, prompt):
        assert agent.name == "nmk_chatbot"
        assert agent.model_settings.temperature == 0.2
        assert agent.model_settings.max_tokens == 1024
        assert agent.model_settings.extra_body == {"reasoning": {"effort": "none"}}
        assert "CONTEXT" in prompt
        assert "NMK Architects" in prompt
        assert "Thông tin công ty" in prompt
        return FakeResult()

    monkeypatch.setattr(generator, "MODEL_PROVIDER", "openrouter")
    monkeypatch.setattr(generator, "MODEL_NAME", "test/model")
    monkeypatch.setattr(generator, "MODEL_BASE_URL", "https://openrouter.ai/api/v1")
    monkeypatch.setattr(generator, "MODEL_TEMPERATURE", 0.2)
    monkeypatch.setattr(generator, "MODEL_MAX_TOKENS", 1024)
    monkeypatch.setattr(generator, "MODEL_TIMEOUT", 60)
    monkeypatch.setattr(generator, "OPENROUTER_API_KEY", "test-key")
    monkeypatch.setattr(generator.Runner, "run", fake_run)

    answer = asyncio.run(
        generator.generate_answer_async("NMK Architects", "Thông tin công ty")
    )

    assert answer == "Câu trả lời từ OpenRouter"
