# README_llm

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Rút gọn nội dung vì các file trong thư mục hiện chưa có dòng mã nguồn nào.
- 2026-07-24 21:24 +07 - Bổ sung mô tả trạng thái và nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-24 21:39 +07 - Chuẩn hóa phần mô tả nhiệm vụ các file mã nguồn.
- 2026-07-26 16:54 +07 - Cập nhật trạng thái sau buổi 6: `llm.py` đã được đổi tên thành `generator.py`; `generator.py` và `prompt.py` đã có code.

## Nhiệm Vụ Của Thư Mục

Thư mục `llm` chứa mã tạo prompt và gọi mô hình ngôn ngữ để sinh câu trả lời từ context đã truy xuất.

Tính tới sau buổi 6, thư mục này có prompt template và generator gọi Ollama. File `llm.py` không còn trong cây thư mục hiện tại; mã generator nằm ở `generator.py`.

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
- Trạng thái chạy hiện tại: code chỉ hỗ trợ nhánh `ollama`, trong khi `config/settings.yaml` hiện đang cấu hình `llm.provider` là `openrouter`. Với cấu hình hiện tại, hàm sẽ trả về thông báo nhà cung cấp mô hình không được hỗ trợ thay vì gọi LLM.

### `__init__.py`

File này hiện đang rỗng.

File đánh dấu `llm` là Python package.

## Cách Hoạt Động Hiện Tại

Luồng LLM theo code hiện tại:

1. Nhận context và question.
2. Build prompt bằng `llm.prompt.build_prompt`.
3. Kiểm tra provider trong settings.
4. Nếu provider là `ollama`, gọi Ollama local để sinh câu trả lời.
5. Trả về câu trả lời hoặc thông báo lỗi tiếng Việt.

Luồng này chưa được nối với `chat.py`, vì `chat.py` hiện vẫn rỗng.

## Ghi Chú Kỹ Thuật

Dependency `ollama` đã có trong `pyproject.toml`.

Các giá trị cấu hình LLM hiện đọc từ `config/settings.yaml`, gồm:

- `llm.provider`
- `llm.model_name`
- `llm.base_url`
- `llm.temperature`
- `llm.max_tokens`
- `llm.timeout`
