# README_backend

## Nhật Ký Cập Nhật

- 2026-08-04 19:44 +07 - Tạo README cho thư mục `backend` sau refactor layout: backend trở thành runtime root chứa các package Python, data, logs và tests; frontend, `.env`, Docker Compose và `qdrant_storage/` vẫn ở root.

## Nhiệm Vụ Của Thư Mục

Thư mục `backend` là runtime root cho toàn bộ Python backend của dự án RAG chatbot NMK.

Khi chạy backend, ingestion hoặc tests, working directory chuẩn là `backend/`.

## Các Thư Mục Con

- `api/`: FastAPI app, health endpoint và chat routes.
- `config/`: YAML settings và logging config.
- `core/`: settings loader, logging setup, schema và startup components.
- `data/`: raw và processed JSON data.
- `embedding/`: dense embedding, batch embedding và sparse embedder.
- `ingestion/`: load data, chunking pipeline và helpers.
- `llm/`: prompt, legacy Ollama generator và OpenRouter streaming generator.
- `logs/`: application log file.
- `reranking/`: CrossEncoder reranker.
- `retrieval/`: legacy dense retriever, hybrid retriever và context builder.
- `scoring/`: BM25 scorer.
- `vectorstore/`: Qdrant client, point builders và upsert.
- `tests/`: pytest tests cho backend.

## Lệnh Chạy

```bash
cd backend
uv run python -m api.app
uv run python -m ingestion.pipeline
uv run pytest tests/ -q
```

## Thành Phần Vẫn Ở Root

- `.env`: file secret/config local, được `core/settings_loader.py` load từ root. Không đọc hoặc ghi nội dung file này vào tài liệu.
- `docker-compose.yml`: Docker Compose cho Qdrant.
- `qdrant_storage/`: dữ liệu local của Qdrant do Docker mount.
- `frontend/`: Next.js frontend.
- `report/` và `tai_lieu/`: tài liệu trạng thái và học tập.
