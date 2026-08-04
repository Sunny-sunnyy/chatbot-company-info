import asyncio
import types


async def _collect_deltas(async_gen):
    return [delta async for delta in async_gen]


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


def test_stream_answer_async_returns_message_for_empty_context():
    from llm.generator_openai import stream_answer_async

    deltas = asyncio.run(_collect_deltas(stream_answer_async("", "Thông tin công ty")))

    assert deltas == ["Dữ liệu ngữ cảnh không được để trống."]


def test_stream_answer_async_returns_message_for_empty_question():
    from llm.generator_openai import stream_answer_async

    deltas = asyncio.run(_collect_deltas(stream_answer_async("NMK Architects", "")))

    assert deltas == ["Câu hỏi không được để trống."]


def test_stream_answer_async_returns_message_when_openrouter_key_missing(monkeypatch):
    import llm.generator_openai as generator

    monkeypatch.setattr(generator, "MODEL_PROVIDER", "openrouter")
    monkeypatch.setattr(generator, "OPENROUTER_API_KEY", None)

    deltas = asyncio.run(
        _collect_deltas(generator.stream_answer_async("NMK Architects", "Thông tin công ty"))
    )

    assert deltas == ["Thiếu cấu hình API key cho OpenRouter."]


def test_stream_answer_async_yields_deltas_from_run_streamed(monkeypatch):
    import llm.generator_openai as generator
    from openai.types.responses import ResponseTextDeltaEvent

    class FakeStreamingResult:
        def __init__(self, deltas):
            self._deltas = deltas

        async def stream_events(self):
            for delta in self._deltas:
                yield types.SimpleNamespace(
                    type="raw_response_event",
                    data=ResponseTextDeltaEvent(
                        content_index=0,
                        delta=delta,
                        item_id="item-1",
                        logprobs=[],
                        output_index=0,
                        sequence_number=0,
                        type="response.output_text.delta",
                    ),
                )

    def fake_run_streamed(agent, prompt):
        assert agent.name == "nmk_chatbot"
        assert agent.model_settings.temperature == 0.2
        assert agent.model_settings.max_tokens == 1024
        assert agent.model_settings.extra_body == {"reasoning": {"effort": "none"}}
        assert "CONTEXT" in prompt
        assert "NMK Architects" in prompt
        assert "Thông tin công ty" in prompt
        return FakeStreamingResult(["Câu trả lời ", "từ OpenRouter"])

    monkeypatch.setattr(generator, "MODEL_PROVIDER", "openrouter")
    monkeypatch.setattr(generator, "MODEL_NAME", "test/model")
    monkeypatch.setattr(generator, "MODEL_BASE_URL", "https://openrouter.ai/api/v1")
    monkeypatch.setattr(generator, "MODEL_TEMPERATURE", 0.2)
    monkeypatch.setattr(generator, "MODEL_MAX_TOKENS", 1024)
    monkeypatch.setattr(generator, "MODEL_TIMEOUT", 60)
    monkeypatch.setattr(generator, "OPENROUTER_API_KEY", "test-key")
    monkeypatch.setattr(generator.Runner, "run_streamed", fake_run_streamed)

    deltas = asyncio.run(
        _collect_deltas(generator.stream_answer_async("NMK Architects", "Thông tin công ty"))
    )

    assert deltas == ["Câu trả lời ", "từ OpenRouter"]


def test_stream_answer_async_skips_non_text_events(monkeypatch):
    import llm.generator_openai as generator

    class FakeStreamingResult:
        async def stream_events(self):
            yield types.SimpleNamespace(type="run_item_stream_event", data=object())
            yield types.SimpleNamespace(type="raw_response_event", data=object())
            yield types.SimpleNamespace(type="raw_response_event", data="not-a-delta-event")

    def fake_run_streamed(agent, prompt):
        return FakeStreamingResult()

    monkeypatch.setattr(generator, "MODEL_PROVIDER", "openrouter")
    monkeypatch.setattr(generator, "OPENROUTER_API_KEY", "test-key")
    monkeypatch.setattr(generator.Runner, "run_streamed", fake_run_streamed)

    deltas = asyncio.run(
        _collect_deltas(generator.stream_answer_async("NMK Architects", "Thông tin công ty"))
    )

    assert deltas == []
