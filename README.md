# Chatbot thông tin công ty

## Nhật Ký Cập Nhật

- 2026-08-04 17:33 +07 - Cập nhật trạng thái sau khi triển khai streaming + Markdown: `POST /api/chat/openai` trả SSE `text/event-stream` (`meta`/`delta`/`sources`/`done`/`error`); `llm/generator_openai.py` có `stream_answer_async()` dùng `Runner.run_streamed`; frontend gọi endpoint qua `fetch` streaming trong `sendMessageStream` và render Markdown live bằng `react-markdown` + `remark-gfm` (dependency mới trong `frontend/package.json`).
- 2026-08-04 15:41 +07 - Tắt Uvicorn reload trong `api/app.py` để tránh WatchFiles theo dõi toàn repo và restart/kẹt startup khi Qdrant/log/cache thay đổi; backend vẫn bind `0.0.0.0:8000`.
- 2026-08-01 22:04 +07 - Cập nhật trạng thái CodeGraph mới nhất và xác nhận luồng frontend hiện gọi `/api/chat/openai` OpenRouter với hybrid retrieval.
- 2026-08-01 20:40 +07 - Cập nhật trạng thái sau khi nâng cấp `/api/chat/openai` lên v2 (hybrid + BM25 + reranker + ContextBuilder, vẫn OpenRouter) và ghi nhận pipeline hybrid đã chạy thành công với collection hybrid 450 points.
- 2026-07-24 21:39 +07 - Bổ sung mô tả nhiệm vụ file mã nguồn ở thư mục gốc.
- 2026-07-25 17:34 +07 - Bổ sung trạng thái CodeGraph, `.gitignore` và các file tài liệu/cấu hình ở thư mục gốc.
- 2026-07-25 20:22 +07 - Bổ sung chuẩn mô tả vai trò file mã nguồn; tại thời điểm đó `chat.py` vẫn rỗng và chưa có luồng xử lý.
- 2026-07-26 12:23 +07 - Bổ sung mô tả `docker-compose.yml`, `README_docker.md` và trạng thái Qdrant local sau buổi 5.
- 2026-07-26 16:54 +07 - Cập nhật trạng thái sau buổi 6: tại thời điểm đó `chat.py` vẫn rỗng, còn retrieval và LLM đã có code trong các folder riêng.
- 2026-07-26 21:02 +07 - Cập nhật trạng thái sau buổi 7: bổ sung mô tả `api`, `frontend`, `core/schema.py` và lệnh chạy dự án bằng `uv`.
- 2026-07-26 21:16 +07 - Cập nhật trạng thái sau khi xoá `chat.py` ở thư mục gốc; luồng chat hiện nằm trong `api/routes/chat.py`.
- 2026-07-27 16:03 +07 - Bổ sung luồng OpenRouter isolated path: `llm/generator_openai.py`, `api/routes/chat_openai.py`, endpoint `POST /api/chat/openai`, frontend gọi endpoint mới và automated tests liên quan.
- 2026-07-27 17:13 +07 - Cập nhật trạng thái backend entrypoint: `uv run python -m api.app` không còn bật Uvicorn reload để tránh WatchFiles theo dõi toàn repo.
- 2026-07-27 17:19 +07 - Đổi backend entrypoint sang host `localhost` để backend chạy tại `localhost:8000`.
- 2026-07-29 20:56 +07 - Cập nhật trạng thái sau `tai_lieu/p2/2.txt`: pipeline chunking không còn dùng `heroSlides.py`, kiểm tra import pipeline và số chunk hiện tại.
- 2026-07-30 10:54 +07 - Cập nhật trạng thái sau `tai_lieu/p2/3.txt` và `tai_lieu/p2/4.txt`: bổ sung sparse embedder, dữ liệu raw mới trùng nội dung với raw cũ và trạng thái CodeGraph mới nhất.
- 2026-07-30 12:20 +07 - Cập nhật trạng thái sau `tai_lieu/p2/5.txt`, `tai_lieu/p2/6.txt` và `tai_lieu/p2/7.txt`: bổ sung hybrid index, BM25 scorer, hybrid retriever và trạng thái chưa nối vào pipeline/API.
- 2026-07-31 17:07 +07 - Cập nhật trạng thái sau `tai_lieu/p2/8.txt` và `tai_lieu/p2/9.txt`: bổ sung folder `reranking`, `retrieval/context_builder.py` và trạng thái chưa nối vào API.
- 2026-08-01 16:51 +07 - Cập nhật trạng thái khi đang ở `tai_lieu/p2/10.txt`: bổ sung `core/startup.py`, vectorstore/upsert hybrid và lệnh chạy pipeline với lưu ý collection Qdrant cũ.
- 2026-08-01 17:58 +07 - Cập nhật trạng thái sau khi hoàn thành toàn bộ p2: `api/app.py` khởi tạo RAG components lúc startup, `/api/chat` dùng hybrid retrieval + reranker, frontend vẫn gọi `/api/chat/openai`.

## Nhiệm Vụ Thư Mục Gốc

Thư mục gốc chứa cấu hình project Python, file khóa dependency, tài liệu tổng quan, tài liệu tham khảo CodeGraph, cấu hình Docker Compose cho Qdrant, backend API và frontend Next.js của dự án.

CodeGraph đã được init local cho repo này bằng CLI `1.5.0`. Thư mục `.codegraph/` là index SQLite local, được ignore trong `.gitignore` và không nên commit.

Trạng thái kiểm tra gần nhất ngày 2026-08-01 22:04 +07: `codegraph status .` báo `Index is up to date`, index có 64 files, 509 nodes, 854 edges, backend `node:sqlite` full WAL và journal `wal`.

Theo tài liệu CodeGraph, auto-sync được bật mặc định sau khi init: CodeGraph watch project và cập nhật graph khi file thay đổi. Nếu cần kiểm tra thủ công, dùng `codegraph status .`; nếu nghi ngờ index lệch, dùng `codegraph sync`.

## Các File Hiện Có Ở Thư Mục Gốc

### `README.md`

File này mô tả nhiệm vụ thư mục gốc và trạng thái hiện tại của các file chính ở thư mục gốc.

### `.gitignore`

File này khai báo các file/thư mục không đưa vào Git, gồm Python cache, virtual environment, secret `.env`, test cache, dữ liệu local, log, transcript và `.codegraph/`.

### `README_codegraph.md`

File này là tài liệu tham khảo về CodeGraph.

Trong dự án hiện tại, file này được dùng để hiểu cách cài đặt, init, auto-sync và sử dụng CodeGraph cho coding agent. Đây không phải mã nguồn của chatbot.

### `README_docker.md`

File này hướng dẫn chạy Qdrant bằng Docker Compose, kiểm tra trạng thái container, mở dashboard Qdrant, dừng container và bật lại service sau khi tắt máy.

### `RUN_GUIDE.md`

File này là hướng dẫn chạy thủ công cho dự án hiện tại, gồm Qdrant, ingestion pipeline, backend FastAPI, health check, API chat và frontend.

### `api/`

Thư mục này chứa FastAPI backend của chatbot, gồm route chat legacy và route chat OpenRouter. README chi tiết nằm ở `api/README_api.md`.

### `frontend/`

Thư mục này chứa frontend Next.js của chatbot. Frontend hiện gọi endpoint OpenRouter `POST /api/chat/openai`. README chi tiết nằm ở `frontend/README_frontend.md`.

### `tests/`

Thư mục này chứa automated tests cho luồng OpenRouter mới. README chi tiết nằm ở `tests/README_tests.md`.

### `scoring/`

Thư mục này chứa code tính điểm BM25 cho hybrid retrieval. README chi tiết nằm ở `scoring/README_scoring.md`.

### `reranking/`

Thư mục này chứa code rerank document bằng CrossEncoder trước khi build context cho LLM. README chi tiết nằm ở `reranking/README_reranking.md`.

### `docker-compose.yml`

File này khai báo service `qdrant` dùng image `qdrant/qdrant:latest`, expose port `6333` và `6334`, mount dữ liệu local vào `qdrant_storage/`, và dùng network `chatbot-network`.

Tính tới sau buổi 5, người dùng đã chạy Qdrant container thành công và pipeline ingestion đã upsert 450 points vào collection `nmk_chatbot_collection`.

### `qdrant_storage/`

Thư mục này được Docker tạo khi chạy Qdrant.

Đây là dữ liệu local của vector database. Không xóa thư mục này nếu muốn giữ collection và point đã upsert. Sau cập nhật `p2/10`, pipeline upsert hybrid points dense+sparse và đã chạy thành công: collection `nmk_chatbot_collection` hiện có schema hybrid và chứa 450 points.

### `brainstorming.md`

File này tồn tại ở thư mục gốc. Nội dung file không thuộc phần triển khai RAG chính được kiểm tra trong lần cập nhật này.

### `pyproject.toml`

File này khai báo project Python `llm-rag`, yêu cầu Python `>=3.12`, dependency runtime và dependency dev.

Dependency hiện có bao gồm FastAPI, Uvicorn, Qdrant client, SentenceTransformer, Ollama, OpenAI Python SDK, OpenAI Agents SDK, BeautifulSoup, PyYAML và python-dotenv.

### `uv.lock`

File này là lockfile dependency do `uv` quản lý.

## Nhiệm Vụ Các File Mã Nguồn

Thư mục gốc hiện không còn file mã nguồn Python trực tiếp. Luồng backend hiện nằm trong thư mục `api`.

## Lệnh Chạy Dự Án Bằng `uv`

Chạy Qdrant local từ thư mục gốc:

```bash
docker compose up -d qdrant
```

Dừng và xóa container/network do Compose tạo:

```bash
docker compose down
```

Nếu cần nạp lại dữ liệu vào Qdrant:

```bash
uv run python -m ingestion.pipeline
```

Sau cập nhật `p2/10`, pipeline build/upsert hybrid points và đã chạy thành công. Nếu chạy lại khi collection đang giữ schema cũ dense-only, xoá collection đó trước để pipeline tạo lại collection với named vector `dense` và sparse vector `sparse`.

Pipeline hiện không còn tạo chunk từ `heroSlides.json`. File `data/processed/heroSlides.json` vẫn tồn tại như dữ liệu processed, nhưng `ingestion/chunking/heroSlides.py` đã bị xoá khỏi code hiện tại để giảm nhiễu retrieval.

`data/raw` hiện có hai file export giống hệt nhau theo checksum:

```text
database_export_2026-01-14T02-32-14.json
database_export_2026-01-23T02-02-46.json
```

Theo xác nhận của người dùng, các lần làm việc tiếp theo sẽ dùng file `database_export_2026-01-23T02-02-46.json`. Trạng thái code hiện tại: `ingestion/load_data.py` vẫn đang đọc trực tiếp file ngày `2026-01-14`; chưa có thay đổi code trong phiên cập nhật tài liệu này.

Chạy backend FastAPI:

```bash
uv run python -m api.app
```

Backend mặc định chạy tại:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/health
```

API chat:

```text
http://localhost:8000/api/chat
```

API chat OpenRouter:

```text
http://localhost:8000/api/chat/openai
```

Chạy frontend trong terminal riêng:

```bash
cd frontend
npm run dev
```

Frontend mặc định chạy tại:

```text
http://localhost:3000
```

Trạng thái hiện tại: `frontend/node_modules/` tồn tại local tại thời điểm kiểm tra này và được `frontend/.gitignore` ignore.

## Lưu Ý Chạy Hiện Tại

`llm/generator.py` hiện được giữ nguyên làm legacy Ollama generator và chỉ hỗ trợ provider `ollama`.

Luồng OpenRouter mới nằm trong `llm/generator_openai.py` và được gọi bởi endpoint `POST /api/chat/openai`.

`embedding/sparse_embedder.py` hiện đã có code sparse embedding theo `tai_lieu/p2/4.txt`, gồm `tokenize()` và class `SparseEmbedder`.

`core/startup.py` hiện đã có code khởi tạo sparse embedder, BM25 và CrossEncoder reranker từ corpus trong Qdrant. `api/app.py` gọi `initialize_rag_components()` trong lifespan startup, `api/health.py` đọc trạng thái qua `get_initialization_status()`, và `api/routes/chat.py` lấy BM25/reranker qua `get_bm25()` cùng `get_reranker()`.

`vectorstore/hybrid_index.py` hiện đã có code build point có named vector `dense` và `sparse`. `vectorstore/upsert.py` hiện đã fit `SparseEmbedder`, gọi `init_sparse_embedder(...)`, build hybrid points và upsert vào Qdrant. `vectorstore/qdrant.py` hiện tạo collection hybrid khi collection chưa tồn tại; collection cũ dense-only không được tự migrate.

`scoring/bm25.py` hiện đã có class `BM25` để tính keyword relevance giữa query và document. `retrieval/hybrid_retriever.py` hiện đã có hàm `hybrid_retrieve(query, bm25)` để trộn dense score và BM25 score theo `dense_weight`/`bm25_weight` trong settings. Endpoint `POST /api/chat` hiện đã gọi luồng hybrid này.

`reranking` hiện đã có `BaseReranker`, `CrossEncoderModel` và `CrossEncoderReranker` để chấm điểm lại document theo cặp query/document. Endpoint `POST /api/chat` hiện gọi reranker lấy từ `core/startup.py` nếu component này đã khởi tạo thành công. `retrieval/context_builder.py` đã có `ContextBuilder` và cả hai route chat (`/api/chat`, `/api/chat/openai`) hiện đều dùng class này để build context.

Frontend hiện gọi endpoint OpenRouter mới qua SSE streaming (`sendMessageStream` dùng `fetch`) và render câu trả lời Markdown live bằng `react-markdown` + `remark-gfm`. Nếu muốn đổi frontend về endpoint legacy `POST /api/chat` (trả JSON một lần), xem hướng dẫn trong `frontend/README_frontend.md` hoặc `frontend/lib/README_lib.md`.

`api/app.py` hiện chạy Uvicorn với `host="0.0.0.0"`, port `8000` và `reload=False` khi dùng `uv run python -m api.app`.

Lưu ý tích hợp hiện tại: `config/settings.yaml` đang đặt `llm.provider: openrouter`. Endpoint `POST /api/chat` đã dùng hybrid retrieval + reranker + `ContextBuilder` nhưng vẫn gọi legacy `llm/generator.py`, file này chỉ hỗ trợ provider `ollama`. Endpoint `POST /api/chat/openai` dùng OpenRouter qua OpenAI Agents SDK, dùng hybrid retrieval + BM25 + reranker + `ContextBuilder` giống luồng v2, và trả SSE stream `text/event-stream` thay vì JSON một lần. `retrieval/retriever.py` (dense-only) được giữ làm legacy nhưng không còn route nào gọi. Frontend hiện gọi `POST /api/chat/openai` qua `fetch` streaming và render Markdown live.
