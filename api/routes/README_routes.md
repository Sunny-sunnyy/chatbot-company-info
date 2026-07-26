# README_routes

## Nhật Ký Cập Nhật

- 2026-07-26 21:02 +07 - Tạo README cho thư mục `api/routes` sau buổi 7, đối chiếu với mã nguồn route hiện tại.

## Nhiệm Vụ Của Thư Mục

Thư mục `api/routes` chứa các route được đăng ký vào FastAPI app.

Hiện tại thư mục có route chat và file gom router để `api/app.py` import.

## File Tài Liệu Trong Thư Mục

### `README_routes.md`

File này mô tả nhiệm vụ của thư mục `api/routes` và trạng thái từng file mã nguồn trong thư mục.

## Nhiệm Vụ Các File Mã Nguồn

### `chat.py`

File này đã có mã nguồn.

Nội dung chính:

- Import `APIRouter` và `HTTPException`.
- Import `BaseModel` và `Field` từ Pydantic.
- Import `retrieve` từ `retrieval.retriever`.
- Import `generate_answer` từ `llm.generator`.
- Đọc `MAX_QUERY_LENGTH` từ biến môi trường, mặc định `500`.
- Tạo dictionary `sessions` trong memory.
- Định nghĩa Pydantic model `ChatRequest`.
- Định nghĩa Pydantic model `ChatResponse`.
- Định nghĩa endpoint `POST /chat`.

Vai trò và luồng hoạt động:

- `chat.py` nhận câu hỏi từ frontend qua API.
- `ChatRequest` nhận `query` và `session_id` tùy chọn.
- `ChatResponse` trả `answer`, `sources` và `session_id`.
- `chat_endpoint(request)` strip query, tạo session id nếu chưa có, gọi `retrieve(question)`, build context từ các document truy xuất được, gọi `generate_answer(context, question)`, rồi trả câu trả lời và sources.
- Input chính là JSON body dạng `{"query": "...", "session_id": "..."}`.
- Output chính là JSON response theo `ChatResponse`.
- Trạng thái hiện tại: file import được sau khi `core/schema.py` có `RetrievedDocument`. Khi chạy thật, route vẫn phụ thuộc Qdrant, embedding model và `llm/generator.py`.

### `__init__.py`

File này đã có mã nguồn.

Nội dung chính:

- Import `router` từ `api.routes.chat` thành `chat_router`.
- Import `router` từ `api.health` thành `health_router`.
- Khai báo `__all__ = ["chat_router", "health_router"]`.

Vai trò và luồng hoạt động:

- `__init__.py` gom router để `api/app.py` có thể import từ `api.routes`.
- File này không tự chạy server.

## Cách Hoạt Động Hiện Tại

`api/app.py` đăng ký `chat_router` với prefix `/api`, nên endpoint chat đầy đủ là:

```text
POST /api/chat
```

## Ghi Chú Kỹ Thuật

Session đang được lưu bằng dictionary trong memory của process Python. Dữ liệu session sẽ mất khi server restart.
