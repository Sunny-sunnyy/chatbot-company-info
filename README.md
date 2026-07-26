# Chatbot thông tin công ty

## Nhật Ký Cập Nhật

- 2026-07-24 21:39 +07 - Bổ sung mô tả nhiệm vụ file mã nguồn ở thư mục gốc.
- 2026-07-25 17:34 +07 - Bổ sung trạng thái CodeGraph, `.gitignore` và các file tài liệu/cấu hình ở thư mục gốc.
- 2026-07-25 20:22 +07 - Bổ sung chuẩn mô tả vai trò file mã nguồn; tại thời điểm đó `chat.py` vẫn rỗng và chưa có luồng xử lý.
- 2026-07-26 12:23 +07 - Bổ sung mô tả `docker-compose.yml`, `README_docker.md` và trạng thái Qdrant local sau buổi 5.
- 2026-07-26 16:54 +07 - Cập nhật trạng thái sau buổi 6: tại thời điểm đó `chat.py` vẫn rỗng, còn retrieval và LLM đã có code trong các folder riêng.
- 2026-07-26 21:02 +07 - Cập nhật trạng thái sau buổi 7: bổ sung mô tả `api`, `frontend`, `core/schema.py` và lệnh chạy dự án bằng `uv`.
- 2026-07-26 21:16 +07 - Cập nhật trạng thái sau khi xoá `chat.py` ở thư mục gốc; luồng chat hiện nằm trong `api/routes/chat.py`.

## Nhiệm Vụ Thư Mục Gốc

Thư mục gốc chứa cấu hình project Python, file khóa dependency, tài liệu tổng quan, tài liệu tham khảo CodeGraph, cấu hình Docker Compose cho Qdrant, backend API, frontend Next.js và entrypoint cấp cao của dự án.

CodeGraph đã được init local cho repo này bằng CLI `1.5.0`. Thư mục `.codegraph/` là index SQLite local, được ignore trong `.gitignore` và không nên commit.

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

### `api/`

Thư mục này chứa FastAPI backend của chatbot. README chi tiết nằm ở `api/README_api.md`.

### `frontend/`

Thư mục này chứa frontend Next.js của chatbot. README chi tiết nằm ở `frontend/README_frontend.md`.

### `docker-compose.yml`

File này khai báo service `qdrant` dùng image `qdrant/qdrant:latest`, expose port `6333` và `6334`, mount dữ liệu local vào `qdrant_storage/`, và dùng network `chatbot-network`.

Tính tới sau buổi 5, người dùng đã chạy Qdrant container thành công và pipeline ingestion đã upsert 450 points vào collection `nmk_chatbot_collection`.

### `qdrant_storage/`

Thư mục này được Docker tạo khi chạy Qdrant.

Đây là dữ liệu local của vector database. Không xóa thư mục này nếu muốn giữ collection và point đã upsert.

### `brainstorming.md`

File này tồn tại ở thư mục gốc. Nội dung file không thuộc phần triển khai RAG chính được kiểm tra trong lần cập nhật này.

### `pyproject.toml`

File này khai báo project Python `llm-rag`, yêu cầu Python `>=3.12`, dependency runtime và dependency dev.

Dependency hiện có bao gồm FastAPI, Uvicorn, Qdrant client, SentenceTransformer, Ollama, BeautifulSoup, PyYAML và python-dotenv.

### `uv.lock`

File này là lockfile dependency do `uv` quản lý.

## Nhiệm Vụ Các File Mã Nguồn

Thư mục gốc hiện không còn file mã nguồn Python trực tiếp. Luồng backend hiện nằm trong thư mục `api`.

## Lệnh Chạy Dự Án Bằng `uv`

Chạy Qdrant local từ thư mục gốc:

```bash
docker compose up -d qdrant
```

Nếu cần nạp lại dữ liệu vào Qdrant:

```bash
uv run python -m ingestion.pipeline
```

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

`llm/generator.py` hiện chỉ hỗ trợ provider `ollama`, trong khi `config/settings.yaml` đang cấu hình `llm.provider` là `openrouter`. Vì vậy backend có thể import được, nhưng luồng sinh câu trả lời thật chưa khớp provider cho tới khi `llm/generator.py` được sửa ở bước riêng.
