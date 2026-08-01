# README_tests

## Nhật Ký Cập Nhật

- 2026-08-01 22:04 +07 - Bổ sung mô tả `tests/test_context_builder.py` và cập nhật trạng thái test theo route OpenRouter hybrid hiện tại.
- 2026-08-01 20:40 +07 - Cập nhật sau khi nâng cấp `/api/chat/openai` lên v2: test route giờ cover luồng hybrid + rate limit 429 + BM25 chưa sẵn sàng 503.
- 2026-07-27 16:03 +07 - Tạo README cho thư mục `tests` sau khi thêm automated tests cho luồng OpenRouter isolated path.
- 2026-07-27 17:04 +07 - Cập nhật mô tả test generator sau khi bổ sung kiểm tra cấu hình tắt OpenRouter reasoning bằng `ModelSettings.extra_body`.
- 2026-08-01 17:58 +07 - Cập nhật trạng thái test sau p2 hoàn chỉnh; sau mốc này test route OpenRouter đã được cập nhật để cover luồng hybrid, rate limit và BM25 chưa sẵn sàng.

## Nhiệm Vụ Của Thư Mục

Thư mục `tests` chứa automated tests cho các phần backend mới được thêm vào dự án.

Các test hiện tại không gọi OpenRouter thật, không cần API key thật và không truy vấn Qdrant thật. Những phụ thuộc ngoài như retrieval và LLM call được thay bằng monkeypatch hoặc gọi trực tiếp endpoint function.

## File Tài Liệu Trong Thư Mục

### `README_tests.md`

File này mô tả nhiệm vụ của thư mục `tests` và trạng thái từng file test hiện có.

## Nhiệm Vụ Các File Mã Nguồn

### `conftest.py`

File này đã có mã nguồn.

Vai trò hiện tại:

- Thêm project root vào `sys.path` khi chạy `pytest`.
- Giúp test import được các package local như `api`, `llm` và `core`.

### `test_llm_generator_openai.py`

File này đã có mã nguồn.

Vai trò hiện tại:

- Test `llm.generator_openai.generate_answer_async`.
- Kiểm tra context rỗng.
- Kiểm tra question rỗng.
- Kiểm tra thiếu `OPENROUTER_API_KEY`.
- Kiểm tra happy path bằng monkeypatch `Runner.run`, không gọi OpenRouter thật.
- Kiểm tra `ModelSettings.extra_body` có `{"reasoning": {"effort": "none"}}`.

### `test_api_chat_openai.py`

File này đã có mã nguồn.

Vai trò hiện tại:

- Test `api.routes.chat_openai.chat_openai_endpoint`.
- Monkeypatch `hybrid_retrieve(...)`, `get_bm25(...)`, `get_reranker(...)` và `generate_answer_async(...)` để không gọi Qdrant, BM25/reranker thật hoặc OpenRouter.
- Dùng object `FakeRequest` giả thay cho `Request` của Starlette; endpoint chỉ truy cập `req.client.host`.
- Gọi trực tiếp async endpoint function bằng `asyncio.run(...)` để tránh phụ thuộc `TestClient` trong môi trường hiện tại.
- Happy path kiểm tra response trả `answer`, `sources` và `session_id`.
- Case 429 khi vượt rate limit in-memory (monkeypatch `check_rate_limit(...)` trả `False`).
- Case 503 khi `get_bm25()` trả `None` (BM25 chưa khởi tạo).

### `test_context_builder.py`

File này đã có mã nguồn.

Vai trò hiện tại:

- Test `retrieval.context_builder.ContextBuilder`.
- Kiểm tra ghép nhiều document bằng separator mặc định.
- Kiểm tra giới hạn số document bằng `max_documents`.
- Kiểm tra cắt context khi vượt `max_context_length`.
- Kiểm tra bỏ qua document có text rỗng.
- Kiểm tra trả chuỗi rỗng khi không có document.

## Cách Chạy Hiện Tại

Chạy các test mới từ thư mục gốc:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_llm_generator_openai.py tests/test_api_chat_openai.py tests/test_context_builder.py -q
```

## Ghi Chú Kỹ Thuật

E2E thật với Qdrant, backend, frontend và OpenRouter không nằm trong automated tests hiện tại. Luồng đó cần chạy thủ công bằng nhiều terminal để kiểm tra toàn bộ ứng dụng.

Endpoint `POST /api/chat` sau p2 dùng hybrid retrieval, BM25 và reranker nhưng vẫn chưa có automated test riêng; test hiện có bao phủ luồng v2 của `POST /api/chat/openai` (hybrid, rate limit, 503).
