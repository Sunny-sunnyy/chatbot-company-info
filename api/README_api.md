# README_api

## Nhật Ký Cập Nhật

- 2026-08-01 20:40 +07 - Cập nhật trạng thái sau khi nâng cấp `/api/chat/openai` lên v2: route dùng hybrid retrieval + BM25 + reranker + `ContextBuilder` và có rate limit in-memory theo IP; `/api/chat` cũng chuyển sang dùng `ContextBuilder`.
- 2026-07-26 21:02 +07 - Tạo README cho thư mục `api` sau buổi 7, đối chiếu với mã nguồn FastAPI hiện tại.
- 2026-07-27 16:03 +07 - Bổ sung mô tả route OpenRouter mới `POST /api/chat/openai` và trạng thái đăng ký router trong `api/app.py`.
- 2026-07-27 17:13 +07 - Cập nhật entrypoint `api/app.py` để `uv run python -m api.app` chạy Uvicorn không bật reload và chỉ bind `127.0.0.1`.
- 2026-07-27 17:19 +07 - Đổi host Uvicorn trong `api/app.py` từ `127.0.0.1` sang `localhost` theo yêu cầu chạy backend tại `localhost:8000`.
- 2026-08-01 17:58 +07 - Cập nhật trạng thái API sau p2 hoàn chỉnh: lifespan startup khởi tạo RAG components, middleware response time, `/health` trả trạng thái RAG và `/api/chat` dùng hybrid retrieval + reranker.

## Nhiệm Vụ Của Thư Mục

Thư mục `api` chứa backend FastAPI cho chatbot.

Backend hiện khai báo app FastAPI, cấu hình CORS, khởi tạo RAG components trong lifespan startup, gắn middleware đo response time, đăng ký route health check, route chat hybrid legacy-generator và route chat OpenRouter.

## File Tài Liệu Trong Thư Mục

### `README_api.md`

File này mô tả nhiệm vụ của thư mục `api`, trạng thái từng file mã nguồn trong thư mục và cách backend hiện được nối với các module RAG.

## Nhiệm Vụ Các File Mã Nguồn

### `app.py`

File này đã có mã nguồn.

Nội dung chính:

- Import `FastAPI`.
- Import `Request`.
- Import `CORSMiddleware`.
- Import `asynccontextmanager`, `logging` và `time`.
- Import `setup_logging` từ `core.logging_setup`.
- Import `initialize_rag_components` từ `core.startup`.
- Gọi `setup_logging()`.
- Định nghĩa lifespan startup/shutdown cho FastAPI.
- Trong startup, gọi `initialize_rag_components()` để load corpus từ Qdrant, fit sparse embedder, khởi tạo BM25 và reranker.
- Tạo app FastAPI với title, description, version và lifespan.
- Cấu hình CORS cho mọi origin, method và header.
- Định nghĩa middleware `track_response_time` để thêm header `X-Response-Time` và log thời gian xử lý request.
- Import `chat_router`, `chat_openai_router` và `health_router` từ `api.routes`.
- Đăng ký `health_router` ở root path.
- Đăng ký `chat_router` với prefix `/api`.
- Đăng ký `chat_openai_router` với prefix `/api`.
- Định nghĩa endpoint root `GET /`.
- Nếu chạy file bằng module, gọi `uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)`.

Vai trò và luồng hoạt động:

- `app.py` là entrypoint backend API.
- Input chính là HTTP request từ frontend hoặc client API; lúc server startup còn cần Qdrant đang chạy và collection có dữ liệu nếu muốn khởi tạo đủ BM25/reranker.
- Output là response JSON từ các route đã đăng ký.
- Trạng thái kiểm tra hiện tại: `api.app` import được bằng `uv run`; lifespan startup chỉ chạy khi khởi động server thật.

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
- Endpoint đọc trạng thái RAG components từ `core.startup.get_initialization_status()`, gồm initialized, sparse embedder, BM25, reranker, vocabulary size và average document length.
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

`POST /api/chat` hiện gọi `hybrid_retrieve(question, bm25)`, rerank bằng `CrossEncoderReranker` nếu startup đã khởi tạo được, build context bằng `ContextBuilder` và gọi `generate_answer(context, question)` từ legacy `llm/generator.py`. Route này có rate limit in-memory theo IP qua `RATE_LIMIT_PER_MINUTE`.

`POST /api/chat/openai` hiện gọi `hybrid_retrieve(question, bm25)`, rerank bằng `CrossEncoderReranker` nếu startup khởi tạo được, build context bằng `ContextBuilder` và gọi `await generate_answer_async(context, question)` từ `llm/generator_openai.py`. Route này cũng có rate limit in-memory theo IP như `/api/chat`.

`llm/generator.py` được giữ nguyên làm legacy Ollama generator. Luồng OpenRouter mới nằm trong `llm/generator_openai.py`.

`config/settings.yaml` hiện đặt `llm.provider: openrouter`. Vì vậy endpoint `/api/chat/openai` khớp provider OpenRouter hiện tại; endpoint `/api/chat` chỉ sinh answer thật qua `llm/generator.py` nếu cấu hình provider được đổi sang `ollama`.
