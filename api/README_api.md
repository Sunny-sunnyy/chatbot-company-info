# README_api

## Nhật Ký Cập Nhật

- 2026-07-26 21:02 +07 - Tạo README cho thư mục `api` sau buổi 7, đối chiếu với mã nguồn FastAPI hiện tại.

## Nhiệm Vụ Của Thư Mục

Thư mục `api` chứa backend FastAPI cho chatbot.

Backend hiện khai báo app FastAPI, cấu hình CORS, đăng ký route health check và route chat.

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
- Import `chat_router` và `health_router` từ `api.routes`.
- Đăng ký `health_router` ở root path.
- Đăng ký `chat_router` với prefix `/api`.
- Định nghĩa endpoint root `GET /`.
- Nếu chạy file bằng module, gọi `uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)`.

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

## Ghi Chú Kỹ Thuật

`POST /api/chat` hiện gọi `retrieve(question)` và `generate_answer(context, question)`.

`llm/generator.py` chưa được sửa trong lần cập nhật này. Với cấu hình hiện tại `llm.provider` là `openrouter`, generator vẫn trả thông báo provider không được hỗ trợ vì code hiện chỉ có nhánh `ollama`.
