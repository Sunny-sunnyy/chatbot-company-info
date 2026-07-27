# README_api

## Nhật Ký Cập Nhật

- 2026-07-26 21:02 +07 - Tạo README cho thư mục `api` sau buổi 7, đối chiếu với mã nguồn FastAPI hiện tại.
- 2026-07-27 16:03 +07 - Bổ sung mô tả route OpenRouter mới `POST /api/chat/openai` và trạng thái đăng ký router trong `api/app.py`.
- 2026-07-27 17:13 +07 - Cập nhật entrypoint `api/app.py` để `uv run python -m api.app` chạy Uvicorn không bật reload và chỉ bind `127.0.0.1`.
- 2026-07-27 17:19 +07 - Đổi host Uvicorn trong `api/app.py` từ `127.0.0.1` sang `localhost` theo yêu cầu chạy backend tại `localhost:8000`.

## Nhiệm Vụ Của Thư Mục

Thư mục `api` chứa backend FastAPI cho chatbot.

Backend hiện khai báo app FastAPI, cấu hình CORS, đăng ký route health check, route chat legacy và route chat OpenRouter.

## File Tài Liệu Trong Thư Mục

### `README_api.md`

File này mô tả nhiệm vụ của thư mục `api`, trạng thái từng file mã nguồn trong thư mục và cách backend hiện được nối với các module RAG.

## Nhiệm Vụ Các File Mã Nguồn

### `app.py`

File này đã có mã nguồn.

Nội dung chính:

- Import `FastAPI`.
- Import `CORSMiddleware`.
- Import `setup_logging` từ `core.logging_setup`.
- Gọi `setup_logging()`.
- Tạo app FastAPI với title, description và version.
- Cấu hình CORS cho mọi origin, method và header.
- Import `chat_router`, `chat_openai_router` và `health_router` từ `api.routes`.
- Đăng ký `health_router` ở root path.
- Đăng ký `chat_router` với prefix `/api`.
- Đăng ký `chat_openai_router` với prefix `/api`.
- Định nghĩa endpoint root `GET /`.
- Nếu chạy file bằng module, gọi `uvicorn.run("api.app:app", host="localhost", port=8000, reload=False)`.

Vai trò và luồng hoạt động:

- `app.py` là entrypoint backend API.
- Input chính là HTTP request từ frontend hoặc client API.
- Output là response JSON từ các route đã đăng ký.
- Trạng thái kiểm tra hiện tại: `api.app` import được bằng `uv run`; server chưa được chạy trong phiên kiểm tra này.

### `health.py`

File này đã có mã nguồn.

Nội dung chính:

- Import `APIRouter`.
- Import `get_qdrant_client` từ `vectorstore.qdrant`.
- Import `load_settings` từ `core.settings_loader`.
- Tạo `router`.
- Định nghĩa endpoint `GET /health`.

Vai trò và luồng hoạt động:

- `health.py` kiểm tra trạng thái các thành phần backend chính.
- Endpoint `/health` thử kết nối Qdrant và đọc danh sách collection.
- Endpoint cũng thử load embedding model bằng `embedding.embedder.get_model()`.
- Endpoint đọc cấu hình LLM và trả provider/model đang cấu hình.
- Input là HTTP request `GET /health`.
- Output là JSON health status có nhóm `services`.
- Trạng thái hiện tại: code import được. Lưu ý endpoint này có thể load embedding model khi được gọi, nên health check có thể nặng hơn health check chỉ kiểm tra process.

### `__init__.py`

File này hiện đang rỗng.

File đánh dấu `api` là Python package.

## Thư Mục Con Hiện Có

### `routes/`

Thư mục này chứa route module của API.

README chi tiết nằm ở `api/routes/README_routes.md`.

## Cách Chạy Hiện Tại

Chạy backend từ thư mục gốc bằng `uv`:

```bash
uv run python -m api.app
```

Backend mặc định chạy ở:

```text
http://localhost:8000
```

Route hiện có:

- `GET /`
- `GET /health`
- `POST /api/chat`
- `POST /api/chat/openai`

## Ghi Chú Kỹ Thuật

`POST /api/chat` hiện gọi `retrieve(question)` và `generate_answer(context, question)` từ legacy `llm/generator.py`.

`POST /api/chat/openai` hiện gọi `retrieve(question)` và `await generate_answer_async(context, question)` từ `llm/generator_openai.py`.

`llm/generator.py` được giữ nguyên làm legacy Ollama generator. Luồng OpenRouter mới nằm trong `llm/generator_openai.py`.

`api/app.py` hiện không bật Uvicorn reload khi chạy bằng `uv run python -m api.app`. Trạng thái này tránh việc WatchFiles theo dõi toàn bộ repo, bao gồm frontend build/cache, khiến backend bị treo hoặc response không ổn định trong lúc test local.
