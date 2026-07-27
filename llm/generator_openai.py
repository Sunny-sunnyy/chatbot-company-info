import logging
import time

from agents import (
    Agent,
    ModelSettings,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,
)
from openai import APIConnectionError, APITimeoutError, AsyncOpenAI, OpenAIError

from core.settings_loader import load_settings
from llm.prompt import SYSTEM_PROMPT, build_prompt


settings = load_settings()
logger = logging.getLogger("llm")

LLM_CONFIG = settings["llm"]
MODEL_PROVIDER = LLM_CONFIG.get("provider", "openrouter")
MODEL_NAME = LLM_CONFIG.get("model_name", "qwen/qwen3.5-9b")
MODEL_BASE_URL = LLM_CONFIG.get("base_url", "https://openrouter.ai/api/v1")
MODEL_TEMPERATURE = LLM_CONFIG.get("temperature", 0.2)
MODEL_MAX_TOKENS = LLM_CONFIG.get("max_tokens", 1024)
MODEL_TIMEOUT = LLM_CONFIG.get("timeout", 60)
OPENROUTER_API_KEY = LLM_CONFIG.get("openrouter_api_key")


def _validate_inputs(context: str, question: str) -> str | None:
    if not context or not context.strip():
        logger.warning("Received empty context for answer generation.")
        return "Dữ liệu ngữ cảnh không được để trống."

    if not question or not question.strip():
        logger.warning("Received empty question for answer generation.")
        return "Câu hỏi không được để trống."

    return None


def _build_openrouter_agent() -> Agent:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is not configured.")

    set_tracing_disabled(True)

    client = AsyncOpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=MODEL_BASE_URL,
        timeout=MODEL_TIMEOUT,
    )
    model = OpenAIChatCompletionsModel(
        model=MODEL_NAME,
        openai_client=client,
    )
    return Agent(
        name="nmk_chatbot",
        instructions=SYSTEM_PROMPT,
        model=model,
        model_settings=ModelSettings(
            temperature=MODEL_TEMPERATURE,
            max_tokens=MODEL_MAX_TOKENS,
            extra_body={"reasoning": {"effort": "none"}},
        ),
    )


async def generate_answer_async(context: str, question: str) -> str:
    validation_error = _validate_inputs(context, question)
    if validation_error:
        return validation_error

    if MODEL_PROVIDER != "openrouter":
        logger.error(f"Unsupported model provider for OpenRouter generator: {MODEL_PROVIDER}")
        return "Nhà cung cấp mô hình không được hỗ trợ."

    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY is not configured.")
        return "Thiếu cấu hình API key cho OpenRouter."

    prompt = build_prompt(context, question)
    start = time.time()
    logger.info(f"Generating answer using provider={MODEL_PROVIDER}, model={MODEL_NAME}")

    try:
        agent = _build_openrouter_agent()
        result = await Runner.run(agent, prompt)
        answer = str(result.final_output).strip()
        logger.info("Answer generation completed successfully.")
        logger.info(f"Time taken for generation: {time.time() - start:.2f} seconds")
        return answer
    except ValueError as error:
        logger.error(str(error))
        return "Thiếu cấu hình API key cho OpenRouter."
    except APITimeoutError:
        logger.error(f"OpenRouter request timeout after {MODEL_TIMEOUT}s")
        return "Yêu cầu xử lý quá lâu. Vui lòng thử lại với câu hỏi ngắn gọn hơn."
    except APIConnectionError as error:
        logger.error(f"Cannot connect to OpenRouter: {error}")
        return "Không thể kết nối đến dịch vụ AI. Vui lòng kiểm tra cấu hình."
    except OpenAIError as error:
        logger.error(f"OpenRouter API error: {error}")
        return "Xin lỗi, mô hình ngôn ngữ đang gặp vấn đề. Vui lòng thử lại sau."
    except Exception as error:
        logger.error(f"Error during answer generation: {error}", exc_info=True)
        return "Đã xảy ra lỗi trong quá trình tạo câu trả lời."
