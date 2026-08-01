# README_tests

## Nhật Ký Cập Nhật

- 2026-07-27 16:03 +07 - Tạo README cho thư mục `tests` sau khi thêm automated tests cho luồng OpenRouter isolated path.
- 2026-07-27 17:04 +07 - Cập nhật mô tả test generator sau khi bổ sung kiểm tra cấu hình tắt OpenRouter reasoning bằng `ModelSettings.extra_body`.
- 2026-08-01 17:58 +07 - Cập nhật trạng thái test sau p2 hoàn chỉnh: test hiện có vẫn chỉ bao phủ luồng OpenRouter isolated path, chưa có test cho `/api/chat` hybrid/reranker.

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
- Monkeypatch `retrieve(...)` để không gọi Qdrant thật.
- Monkeypatch `generate_answer_async(...)` để không gọi OpenRouter thật.
- Gọi trực tiếp async endpoint function để tránh phụ thuộc `TestClient` trong môi trường hiện tại.

## Cách Chạy Hiện Tại

Chạy các test mới từ thư mục gốc:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_llm_generator_openai.py tests/test_api_chat_openai.py -q
```

## Ghi Chú Kỹ Thuật

E2E thật với Qdrant, backend, frontend và OpenRouter không nằm trong automated tests hiện tại. Luồng đó cần chạy thủ công bằng nhiều terminal để kiểm tra toàn bộ ứng dụng.

Endpoint `POST /api/chat` sau p2 đã dùng hybrid retrieval, BM25 và reranker, nhưng hiện chưa có automated test riêng trong thư mục `tests`.
