# README_routes

## Nhật Ký Cập Nhật

- 2026-08-01 20:40 +07 - Cập nhật `chat_openai.py` sau khi nâng cấp lên v2: hybrid retrieval, BM25/reranker từ `core.startup`, `ContextBuilder`, rate limit in-memory; `chat.py` cũng chuyển sang `ContextBuilder`.
- 2026-07-26 21:02 +07 - Tạo README cho thư mục `api/routes` sau buổi 7, đối chiếu với mã nguồn route hiện tại.
- 2026-07-27 16:03 +07 - Bổ sung mô tả `chat_openai.py` và export `chat_openai_router` cho endpoint `POST /api/chat/openai`.
- 2026-08-01 17:58 +07 - Cập nhật `chat.py` sau p2: route `/api/chat` dùng hybrid retrieval, BM25/reranker từ `core.startup` và rate limit in-memory.

## Nhiệm Vụ Của Thư Mục

Thư mục `api/routes` chứa các route được đăng ký vào FastAPI app.

Hiện tại thư mục có hai route chat đều dùng luồng v2 retrieval (hybrid + BM25 + reranker + `ContextBuilder`): `chat.py` gọi legacy generator, `chat_openai.py` gọi OpenRouter generator; cùng file gom router để `api/app.py` import.

## File Tài Liệu Trong Thư Mục

### `README_routes.md`

File này mô tả nhiệm vụ của thư mục `api/routes` và trạng thái từng file mã nguồn trong thư mục.

## Nhiệm Vụ Các File Mã Nguồn

### `chat.py`

File này đã có mã nguồn.

Nội dung chính:

- Import `APIRouter` và `HTTPException`.
- Import `Request`.
- Import `BaseModel` và `Field` từ Pydantic.
- Import `hybrid_retrieve` từ `retrieval.hybrid_retriever`.
- Import `get_bm25` và `get_reranker` từ `core.startup`.
- Import `generate_answer` từ `llm.generator`.
- Đọc `MAX_QUERY_LENGTH` từ biến môi trường, mặc định `500`.
- Đọc `RATE_LIMIT_PER_MINUTE` từ biến môi trường, mặc định `60`.
- Đọc `reranking.top_k` từ settings vào hằng `RERRANKING_TOP_K`.
- Tạo dictionary `sessions` trong memory.
- Tạo dictionary `rate_limit_storage` trong memory.
- Định nghĩa helper `check_rate_limit(client_ip)`.
- Định nghĩa Pydantic model `ChatRequest`.
- Định nghĩa Pydantic model `ChatResponse`.
- Định nghĩa endpoint `POST /chat`.
- Định nghĩa hàm legacy CLI `chat(question: str)`.

Vai trò và luồng hoạt động:

- `chat.py` nhận câu hỏi từ client qua API `POST /api/chat`.
- `ChatRequest` nhận `query` và `session_id` tùy chọn.
- `ChatResponse` trả `answer`, `sources` và `session_id`.
- `chat_endpoint(request, req)` lấy IP client, kiểm tra rate limit, strip query, tạo session id nếu chưa có, lấy BM25 và reranker từ `core.startup`, gọi `hybrid_retrieve(question, bm25)`, rerank document nếu có reranker, build context bằng `ContextBuilder`, gọi `generate_answer(context, question)`, rồi trả câu trả lời và sources.
- Input chính là JSON body dạng `{"query": "...", "session_id": "..."}`.
- Output chính là JSON response theo `ChatResponse`.
- Trạng thái hiện tại: file import được. Khi chạy thật, route phụ thuộc Qdrant collection hybrid có named vector `dense`, embedding model, BM25 đã được `core/startup.py` khởi tạo, reranker nếu có, và `llm/generator.py`.
- Lưu ý tích hợp: `llm/generator.py` hiện chỉ hỗ trợ provider `ollama`, trong khi `config/settings.yaml` đang đặt `llm.provider: openrouter`.

### `__init__.py`

File này đã có mã nguồn.

Nội dung chính:

- Có docstring ngắn `API Routes for NMK Chatbot`.
- Import `router` từ `api.routes.chat` thành `chat_router`.
- Import `router` từ `api.routes.chat_openai` thành `chat_openai_router`.
- Import `router` từ `api.health` thành `health_router`.
- Khai báo `__all__ = ["chat_router", "chat_openai_router", "health_router"]`.

Vai trò và luồng hoạt động:

- `__init__.py` gom router để `api/app.py` có thể import từ `api.routes`.
- File này không tự chạy server.

### `chat_openai.py`

File này đã có mã nguồn.

Nội dung chính:

- Import `APIRouter` và `HTTPException`.
- Import `Request`.
- Import `BaseModel` và `Field` từ Pydantic.
- Import `hybrid_retrieve` từ `retrieval.hybrid_retriever`.
- Import `get_bm25` và `get_reranker` từ `core.startup`.
- Import `ContextBuilder` từ `retrieval.context_builder`.
- Import `generate_answer_async` từ `llm.generator_openai`.
- Đọc `MAX_QUERY_LENGTH` từ biến môi trường, mặc định `500`.
- Đọc `RATE_LIMIT_PER_MINUTE` từ biến môi trường, mặc định `60`.
- Đọc `reranking.top_k` từ settings vào hằng `RERRANKING_TOP_K`.
- Tạo dictionary `sessions` và `rate_limit_storage` trong memory.
- Định nghĩa helper `check_rate_limit(client_ip)`.
- Định nghĩa Pydantic model riêng `ChatRequest`.
- Định nghĩa Pydantic model riêng `ChatResponse`.
- Định nghĩa endpoint `POST /chat/openai`.

Vai trò và luồng hoạt động:

- `chat_openai.py` là route OpenRouter song song với route legacy `chat.py`.
- File nhận câu hỏi từ frontend qua API mới.
- `ChatRequest` nhận `query` và `session_id` tùy chọn.
- `ChatResponse` trả `answer`, `sources` và `session_id`.
- `chat_openai_endpoint(request, req)` lấy IP client, kiểm tra rate limit, strip query, tạo session id nếu chưa có, lấy BM25 và reranker từ `core.startup`, gọi `hybrid_retrieve(question, bm25)`, rerank document nếu có reranker (cắt về `RERRANKING_TOP_K` nếu không), build context bằng `ContextBuilder`, gọi `await generate_answer_async(context, question)`, rồi trả câu trả lời và sources.
- Khi vượt rate limit in-memory, route trả `429`; khi BM25 chưa khởi tạo, route trả `503`.
- Input chính là JSON body dạng `{"query": "...", "session_id": "..."}`.
- Output chính là JSON response theo `ChatResponse`.
- Trạng thái hiện tại: file có automated test trong `tests/test_api_chat_openai.py`; test monkeypatch `hybrid_retrieve`, `get_bm25`, `get_reranker` và `generate_answer_async` nên không gọi Qdrant hoặc OpenRouter thật.

## Cách Hoạt Động Hiện Tại

`api/app.py` đăng ký `chat_router` với prefix `/api`, nên endpoint chat hybrid/legacy-generator đầy đủ là:

```text
POST /api/chat
```

`api/app.py` cũng đăng ký `chat_openai_router` với prefix `/api`, nên endpoint chat OpenRouter đầy đủ là:

```text
POST /api/chat/openai
```

## Ghi Chú Kỹ Thuật

Session đang được lưu bằng dictionary trong memory của process Python. Dữ liệu session sẽ mất khi server restart.

Rate limit của `chat.py` cũng đang lưu trong memory của process Python. Bộ đếm sẽ mất khi server restart và không chia sẻ giữa nhiều process.

Frontend hiện gọi `POST /api/chat/openai` trong `frontend/lib/api.ts`, không gọi `POST /api/chat`.
