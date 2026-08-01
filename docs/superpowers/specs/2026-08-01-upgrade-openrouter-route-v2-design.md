# Design: Nâng cấp luồng OpenRouter lên v2

- Ngày: 2026-08-01
- Trạng thái: đã được người dùng xác nhận (design approval)
- Nhánh: `UpdateV2`

## 1. Mục tiêu

Đưa endpoint `POST /api/chat/openai` lên đúng chuẩn v2 của dự án: hybrid retrieval (dense + BM25), reranking bằng CrossEncoder và build context bằng `ContextBuilder` — trong khi vẫn dùng OpenRouter qua OpenAI Agents SDK (`llm/generator_openai.py`).

Lý do: hiện tại toàn bộ phần nâng cấp v2 (hybrid, BM25, reranker, context builder) mới chỉ được nối vào `/api/chat`, route này lại gọi legacy `llm/generator.py` chỉ hỗ trợ provider `ollama`. Máy người dùng không chạy được Ollama nên cấu hình đang dùng OpenRouter, do đó luồng thực dùng là `/api/chat/openai` nhưng vẫn đang là luồng v1 (dense-only).

## 2. Quyết định đã chốt

- Giữ 2 endpoint hiện tại; nâng cấp `/api/chat/openai` lên v2.
- Frontend không đổi, vẫn gọi `POST /api/chat/openai`.
- Dùng `ContextBuilder` cho cả 2 route (`chat_openai.py` và `chat.py`).
- Thêm rate limit in-memory cho `/api/chat/openai` giống `/api/chat`.
- Cập nhật `tests/test_api_chat_openai.py` theo luồng v2 và thêm case 429/503.
- Giữ `retrieval/retriever.py` làm legacy dense-only (không route nào gọi sau khi thay đổi).
- Không sửa `llm/generator_openai.py` (đã đúng chuẩn v2).

## 3. Thay đổi code

### 3.1 `api/routes/chat_openai.py`

- Import thay đổi:
  - `hybrid_retrieve` từ `retrieval.hybrid_retriever` (thay `retrieve` từ `retrieval.retriever`).
  - `get_bm25`, `get_reranker` từ `core.startup`.
  - `ContextBuilder` từ `retrieval.context_builder`.
  - `Request` từ `fastapi`.
- Thêm rate limit giống `chat.py`:
  - `RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))`.
  - `rate_limit_storage = {}` và helper `check_rate_limit(client_ip)`.
  - Endpoint nhận thêm tham số `req: Request`, lấy `req.client.host`, trả `HTTPException 429` khi vượt giới hạn.
- Thêm `RERRANKING_TOP_K = settings.get("reranking", {}).get("top_k", 5)` (đọc từ `config/settings.yaml`, giống `chat.py`).
- Luồng endpoint mới:
  1. Kiểm tra rate limit.
  2. Strip query, nếu rỗng trả 400.
  3. Tạo `session_id` nếu chưa có.
  4. Lấy `bm25 = get_bm25()` và `reranker = get_reranker()` từ `core.startup`.
  5. Nếu `bm25 is None`, trả `HTTPException 503` "Hệ thống chưa sẵn sàng. Vui lòng thử lại sau."
  6. `documents = hybrid_retrieve(question, bm25)`.
  7. Nếu không có document, trả `ChatResponse` với answer mặc định.
  8. Nếu có reranker: `documents = reranker.rerank(question, documents, top_k=RERRANKING_TOP_K)`; nếu không có, cắt `documents[:RERRANKING_TOP_K]`.
  9. `context = ContextBuilder().build(documents)` (mặc định max_documents=5, max_context_length=3000, separator `\n\n---\n\n`).
  10. `answer = await generate_answer_async(context, question)`.
  11. Build `sources` (text[:200], metadata, score), lưu session, trả `ChatResponse`.

### 3.2 `api/routes/chat.py`

- Thay phần ghép context tay `"\n\n".join(...)` bằng `ContextBuilder().build(documents)` ở cả endpoint `chat_endpoint` và hàm CLI `chat(question)`.
- Giữ nguyên mọi logic khác: rate limit, hybrid retrieval, reranker, legacy `generate_answer`, session.

### 3.3 `tests/test_api_chat_openai.py`

- Sửa monkeypatch cho luồng v2: `hybrid_retrieve`, `get_bm25`, `get_reranker`, `generate_answer_async`.
- Truyền object mock có thuộc tính `client.host` cho tham số `req: Request` (gọi trực tiếp endpoint function, không dùng TestClient để tránh lifespan startup).
- Giữ nguyên case cũ (happy path, không gọi Qdrant/OpenRouter thật).
- Thêm 2 case mới:
  - Vượt rate limit → `HTTPException` 429.
  - `get_bm25` trả `None` → `HTTPException` 503.

## 4. Không đổi

- `llm/generator_openai.py` — đã đúng chuẩn v2 (OpenAI Agents SDK, OpenRouter, tắt reasoning).
- `llm/generator.py` — legacy Ollama, giữ nguyên.
- `retrieval/retriever.py` — legacy dense-only, giữ nguyên, không còn route gọi.
- `core/startup.py`, `vectorstore/*`, `embedding/*`, `scoring/*`, `reranking/*` — không đổi.
- `frontend/*` — endpoint không đổi nên frontend không cần sửa.

## 5. Lưu ý hành vi

- Với `ContextBuilder`, text gửi LLM không còn số thứ tự `[1]` và nhãn `(Nguồn: ...)` như trước; chỉ còn nội dung document ngăn cách bởi separator `\n\n---\n\n`. Đây đúng thiết kế p2/9.
- Metadata nguồn vẫn được trả đầy đủ trong `sources` của `ChatResponse`, nên frontend không bị ảnh hưởng.
- Rate limit lưu in-memory, mất khi restart server và không chia sẻ giữa nhiều process (giống `chat.py`).

## 6. Cập nhật tài liệu

Mỗi file được sửa phải thêm dòng mới vào mục Nhật Ký Cập Nhật (giờ UTC+7).

- 5 file ghi trạng thái pipeline hybrid đã chạy thành công (collection hybrid, 450 points): `report/Project_status.md`, `vectorstore/README_vectorstore.md`, `ingestion/README_ingestion.md`, `RUN_GUIDE.md`, `README.md`.
- Các file README phản ánh thay đổi code: `api/routes/README_routes.md`, `api/README_api.md`, `retrieval/README_retrieval.md` (ContextBuilder đã được route dùng; retriever.py còn là legacy), `tests/README_tests.md`, `report/README_report.md`.
- `llm/README_llm.md` không cần sửa vì `generator_openai.py` không thay đổi.

## 7. Kiểm tra sau khi sửa

- `uv run python -m py_compile api/routes/chat_openai.py api/routes/chat.py tests/test_api_chat_openai.py`.
- `uv run pytest tests/test_llm_generator_openai.py tests/test_api_chat_openai.py -q`.
- Kiểm tra import: `import api.app`.
- Không commit trừ khi người dùng yêu cầu.
