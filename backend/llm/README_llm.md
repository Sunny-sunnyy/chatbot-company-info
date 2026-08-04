# README_llm

## Nhật Ký Cập Nhật

- 2026-08-04 17:33 +07 - Cập nhật `generator_openai.py` sau khi thêm hàm streaming `stream_answer_async()`: hàm này dùng `Runner.run_streamed()` (sync, trả `RunResultStreaming` trực tiếp, không `await`), lặp `async for event in result.stream_events()` và yield text delta khi event là `raw_response_event` và data là `ResponseTextDeltaEvent`; `generate_answer_async()` giữ nguyên dùng `Runner.run()` cho non-stream.
- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Rút gọn nội dung vì các file trong thư mục hiện chưa có dòng mã nguồn nào.
- 2026-07-24 21:24 +07 - Bổ sung mô tả trạng thái và nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-24 21:39 +07 - Chuẩn hóa phần mô tả nhiệm vụ các file mã nguồn.
- 2026-07-26 16:54 +07 - Cập nhật trạng thái sau buổi 6: `llm.py` đã được đổi tên thành `generator.py`; `generator.py` và `prompt.py` đã có code.
- 2026-07-26 21:02 +07 - Cập nhật trạng thái sau buổi 7: `api/routes/chat.py` đã gọi `generate_answer`, nhưng `generator.py` vẫn chưa hỗ trợ provider `openrouter`.
- 2026-07-26 21:16 +07 - Cập nhật trạng thái sau khi `chat.py` ở thư mục gốc được xoá.
- 2026-07-27 16:03 +07 - Bổ sung `generator_openai.py` dùng OpenAI Agents SDK với OpenRouter, giữ `generator.py` làm legacy Ollama generator.
- 2026-07-27 17:04 +07 - Cập nhật `generator_openai.py` để tắt reasoning của OpenRouter bằng `ModelSettings.extra_body`, tránh trường hợp model dùng hết `max_tokens` cho reasoning và trả `final_output` rỗng.

## Nhiệm Vụ Của Thư Mục

Thư mục `llm` chứa mã tạo prompt và gọi mô hình ngôn ngữ để sinh câu trả lời từ context đã truy xuất.

Tính tới thời điểm hiện tại, thư mục này có prompt template, legacy generator gọi Ollama trong `generator.py`, và generator OpenRouter mới trong `generator_openai.py`.

File `llm.py` không còn trong cây thư mục hiện tại.

## File Tài Liệu Trong Thư Mục

### `README_llm.md`

File này mô tả nhiệm vụ của thư mục `llm`, trạng thái hiện tại của từng file mã nguồn và trạng thái chạy của luồng generator.

## Nhiệm Vụ Các File Mã Nguồn

### `prompt.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Định nghĩa hằng `SYSTEM_PROMPT`.
- Định nghĩa hàm `build_prompt(context: str, question: str) -> str`.

`SYSTEM_PROMPT` hiện mô tả chatbot của NMK Architects bằng tiếng Việt, yêu cầu phong cách trả lời thân thiện, dùng thông tin trong context, không bịa thêm thông tin và có câu trả lời mặc định khi không tìm thấy thông tin.

Hàm `build_prompt()` nhận `context` và `question`, ghép với `SYSTEM_PROMPT`, rồi trả về prompt hoàn chỉnh cho LLM.

Vai trò và luồng hoạt động:

- `prompt.py` chịu trách nhiệm biến context từ retrieval và câu hỏi người dùng thành prompt cuối cùng.
- Input chính là `context: str` và `question: str`.
- Output là một chuỗi prompt đã strip khoảng trắng đầu/cuối.
- File này không gọi LLM trực tiếp.

### `generator.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `logging`, `ollama` và `time`.
- Import `build_prompt` từ `llm.prompt`.
- Import `load_settings` từ `core.settings_loader`.
- Đọc cấu hình `llm` từ settings.
- Định nghĩa hàm `generate_answer(context: str, question: str) -> str`.

Hàm `generate_answer()` hiện đang làm các việc sau:

- Kiểm tra context rỗng; nếu rỗng thì log warning và trả về thông báo lỗi tiếng Việt.
- Kiểm tra question rỗng; nếu rỗng thì log warning và trả về thông báo lỗi tiếng Việt.
- Gọi `build_prompt(context, question)` để tạo prompt.
- Đo thời gian sinh câu trả lời bằng `time.time()`.
- Nếu `MODEL_PROVIDER == "ollama"`, tạo `ollama.Client(host=MODEL_BASE_URL, timeout=MODEL_TIMEOUT)`.
- Gọi `client.chat(...)` với role `system`, content là prompt, temperature và `num_predict`.
- Lấy câu trả lời từ `response["message"]["content"]`.
- Log trạng thái hoàn tất và thời gian chạy.
- Trả về câu trả lời dạng string.
- Nếu provider không phải `ollama`, log lỗi và trả về thông báo nhà cung cấp mô hình không được hỗ trợ.
- Bắt lỗi `ollama.ResponseError`, `ollama.RequestError`, `TimeoutError` và lỗi chung để trả về thông báo lỗi tiếng Việt.

Vai trò và luồng hoạt động:

- `generator.py` chịu trách nhiệm gọi LLM để sinh câu trả lời dựa trên prompt đã build.
- Input chính là `context: str` và `question: str`.
- Output là câu trả lời dạng `str`.
- Trạng thái chạy hiện tại: file này được giữ nguyên làm legacy Ollama generator. Code chỉ hỗ trợ nhánh `ollama`; với cấu hình `llm.provider: openrouter`, file này sẽ trả về thông báo nhà cung cấp mô hình không được hỗ trợ.

### `generator_openai.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `Agent`, `ModelSettings`, `OpenAIChatCompletionsModel`, `Runner` và `set_tracing_disabled` từ OpenAI Agents SDK.
- Import `AsyncOpenAI` và các exception OpenAI client.
- Import `ResponseTextDeltaEvent` từ `openai.types.responses`.
- Import `SYSTEM_PROMPT` và `build_prompt` từ `llm.prompt`.
- Đọc cấu hình `llm` từ `core.settings_loader.load_settings()`.
- Định nghĩa helper `_validate_inputs(context, question)`.
- Định nghĩa helper `_build_openrouter_agent()`.
- Định nghĩa async function `generate_answer_async(context: str, question: str) -> str`.
- Định nghĩa async generator `stream_answer_async(context: str, question: str)`.

Vai trò và luồng hoạt động:

- `generator_openai.py` chịu trách nhiệm sinh câu trả lời bằng OpenRouter qua OpenAI Agents SDK.
- Input chính là `context: str` và `question: str`.
- `generate_answer_async()` trả câu trả lời dạng `str`: kiểm tra context/question rỗng, kiểm tra provider `openrouter`, kiểm tra API key OpenRouter đã được cấu hình, build prompt, tạo OpenRouter-compatible `AsyncOpenAI`, tạo `OpenAIChatCompletionsModel`, tạo `Agent` tên `nmk_chatbot`, rồi gọi `await Runner.run(agent, prompt)`.
- `stream_answer_async()` yield từng text delta dạng `str`: dùng chung `_validate_inputs()`, `_build_openrouter_agent()` và `build_prompt()`, gọi `Runner.run_streamed(agent, prompt)` (sync function trong SDK 0.18.3, trả `RunResultStreaming` trực tiếp, không `await`), lặp `async for event in result.stream_events()`, và chỉ yield `event.data.delta` khi `event.type == "raw_response_event"` và `event.data` là `ResponseTextDeltaEvent`.
- File dùng `ModelSettings` để truyền `temperature` và `max_tokens`.
- File dùng `ModelSettings.extra_body={"reasoning": {"effort": "none"}}` để tắt reasoning tokens ở OpenRouter.
- File truyền `timeout` vào `AsyncOpenAI`.
- File gọi `set_tracing_disabled(True)` trước khi chạy OpenRouter để tránh yêu cầu tracing về OpenAI platform trong luồng dùng OpenRouter.
- Cả hai hàm trả/yield thông báo tiếng Việt an toàn khi thiếu API key, provider không hỗ trợ, timeout, lỗi kết nối hoặc lỗi API; không expose stack trace hoặc secret.
- File không đọc hoặc in nội dung secret; API key được lấy từ settings đã được nạp từ biến môi trường.
- Trạng thái test hiện tại: `tests/test_llm_generator_openai.py` kiểm tra cả `generate_answer_async()` (monkeypatch `Runner.run`) và `stream_answer_async()` (monkeypatch `Runner.run_streamed` bằng fake sync function trả `FakeStreamingResult`), không gọi OpenRouter thật.

### `__init__.py`

File này hiện đang rỗng.

File đánh dấu `llm` là Python package.

## Cách Hoạt Động Hiện Tại

Luồng legacy Ollama theo `generator.py`:

1. Nhận context và question.
2. Build prompt bằng `llm.prompt.build_prompt`.
3. Kiểm tra provider trong settings.
4. Nếu provider là `ollama`, gọi Ollama local để sinh câu trả lời.
5. Trả về câu trả lời hoặc thông báo lỗi tiếng Việt.

Luồng này hiện đã được `api/routes/chat.py` gọi trong endpoint `POST /api/chat`.

Luồng OpenRouter mới theo `generator_openai.py`:

1. Nhận context và question.
2. Build prompt bằng `llm.prompt.build_prompt`.
3. Kiểm tra provider trong settings là `openrouter`.
4. Tạo OpenRouter-compatible model bằng OpenAI Agents SDK.
5. Đường non-stream: gọi `Runner.run(...)` async để sinh câu trả lời full string.
6. Đường streaming: gọi `Runner.run_streamed(...)` rồi yield từng text delta từ `stream_events()`.
7. Trả về/yield câu trả lời hoặc thông báo lỗi tiếng Việt.

Với model hiện tại `qwen/qwen3.5-9b`, nếu không tắt reasoning, OpenRouter có thể trả HTTP 200 nhưng `result.final_output` rỗng vì toàn bộ `max_tokens` bị dùng cho reasoning tokens. Vì vậy `generator_openai.py` hiện tắt reasoning bằng `extra_body`.

Luồng này hiện được `api/routes/chat_openai.py` gọi trong endpoint `POST /api/chat/openai`.

`chat.py` ở thư mục gốc đã được xoá. Backend hiện chạy qua `api/app.py`.

## Ghi Chú Kỹ Thuật

Dependency `ollama`, `openai` và `openai-agents` đã có trong `pyproject.toml`.

Các giá trị cấu hình LLM hiện đọc từ `config/settings.yaml`, gồm:

- `llm.provider`
- `llm.model_name`
- `llm.base_url`
- `llm.temperature`
- `llm.max_tokens`
- `llm.timeout`
