# RUN_GUIDE

## Nhật Ký Cập Nhật

- 2026-08-01 20:28 +07 - Cập nhật trạng thái sau khi kiểm tra log chạy thật: pipeline hybrid đã chạy thành công, collection `nmk_chatbot_collection` đã có schema hybrid và chứa 450 points; lỗi `Not existing vector name error: sparse` chỉ xảy ra ở lần chạy đầu với collection cũ dense-only.
- 2026-08-01 17:58 +07 - Viết lại hướng dẫn chạy theo trạng thái repo hiện tại: dùng `uv`, Qdrant hybrid, backend FastAPI và frontend Next.js.

## Mục Đích

File này ghi lệnh chạy thủ công cho dự án RAG chatbot NMK tại thư mục `/home/hieu0606sunny/llm_rag`.

## 1. Chạy Qdrant

Từ thư mục gốc project:

```bash
docker compose up -d qdrant
```

Kiểm tra Qdrant:

```bash
curl http://localhost:6333/health
```

## 2. Nạp Dữ Liệu Vào Qdrant

Chạy ingestion pipeline:

```bash
uv run python -m ingestion.pipeline
```

Pipeline hiện gom 450 chunks từ các module chunking đang dùng, fit `SparseEmbedder`, build point hybrid có named vector `dense` và sparse vector `sparse`, rồi upsert vào collection `nmk_chatbot_collection`.

Nếu gặp lỗi:

```text
Wrong input: Not existing vector name error: sparse
```

nguyên nhân là Qdrant đang giữ collection cũ dense-only. Xóa collection cũ hoặc đổi `vector_database.collection_name`, sau đó chạy lại pipeline để collection được tạo lại đúng schema hybrid.

Trạng thái hiện tại: pipeline hybrid đã chạy thành công; collection `nmk_chatbot_collection` đang có schema hybrid (named vector `dense` + sparse vector `sparse`) và chứa 450 points. Block lỗi phía trên là hướng dẫn khắc phục nếu chạy lại với collection cũ.

## 3. Chạy Backend

Từ thư mục gốc project:

```bash
uv run python -m api.app
```

Backend chạy tại:

```text
http://localhost:8000
```

Lúc startup, `api/app.py` gọi `core/startup.py` để load corpus từ Qdrant, fit sparse embedder, khởi tạo BM25 và CrossEncoder reranker.

## 4. Kiểm Tra Backend

Health check:

```bash
curl http://localhost:8000/health
```

Chat hybrid + reranker:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Thông tin liên hệ của NMK là gì?"}'
```

Chat OpenRouter:

```bash
curl -X POST http://localhost:8000/api/chat/openai \
  -H "Content-Type: application/json" \
  -d '{"query": "Thông tin liên hệ của NMK là gì?"}'
```

## 5. Chạy Frontend

Trong terminal riêng:

```bash
cd frontend
npm run dev
```

Frontend chạy tại:

```text
http://localhost:3000
```

`frontend/lib/api.ts` hiện gọi endpoint:

```text
POST /api/chat/openai
```

## Trạng Thái Luồng Hiện Tại

`POST /api/chat` dùng `hybrid_retrieve()`, BM25 và reranker, nhưng vẫn gọi legacy `llm/generator.py`. File generator legacy này chỉ hỗ trợ provider `ollama`.

`POST /api/chat/openai` dùng `llm/generator_openai.py` và phù hợp với `llm.provider: openrouter` trong `config/settings.yaml`, nhưng route này vẫn dùng dense retriever `retrieval/retriever.py`.

Frontend hiện gọi `POST /api/chat/openai`.
