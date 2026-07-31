# README_config

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra mã nguồn hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 21:24 +07 - Bổ sung mô tả nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-30 12:20 +07 - Cập nhật mô tả cấu hình `dense_weight`, `bm25_weight` và logger `scoring` liên quan tới BM25/hybrid retrieval.
- 2026-07-31 17:07 +07 - Cập nhật mô tả chi tiết cấu hình `reranking.model`, `reranking.device`, `reranking.top_k` và logger `reranking`.

## Nhiệm Vụ Của Thư Mục

Thư mục `config` chứa các file cấu hình YAML của dự án.

Hiện tại thư mục này có hai nhiệm vụ chính:

- Lưu cấu hình tổng thể của ứng dụng và pipeline RAG trong `settings.yaml`.
- Lưu cấu hình logging trong `logging.yaml`.

## Các File Hiện Có

### `README_config.md`

File này mô tả nhiệm vụ của thư mục `config` và nhiệm vụ hiện tại của từng file cấu hình trong thư mục.

### `settings.yaml`

File này chứa cấu hình chính của dự án.

Các nhóm cấu hình hiện có:

- `app`: tên ứng dụng, phiên bản và môi trường chạy.
- `data`: đường dẫn dữ liệu gốc, dữ liệu đã xử lý và schema.
- `chunking`: cấu hình kích thước chunk và overlap.
- `embedding`: tên model embedding, batch size và thiết bị chạy.
- `vector_database`: cấu hình Qdrant.
- `llm`: cấu hình nhà cung cấp, model, base URL, API key, temperature, max tokens và timeout.
- `retrieval`: cấu hình truy xuất dữ liệu.
- `reranking`: cấu hình reranking.

Giá trị hiện tại đáng chú ý:

- `data.raw_dir`: `data/raw`
- `data.processed_dir`: `data/processed`
- `embedding.model`: `intfloat/multilingual-e5-small`
- `embedding.batch_size`: `64`
- `embedding.device`: `cpu`
- `vector_database.type`: `qdrant`
- `vector_database.url`: `http://localhost:6333`
- `vector_database.collection_name`: `nmk_chatbot_collection`
- `vector_database.distance`: `cosine`
- `vector_database.vector_size`: `384`
- `llm.provider`: `openrouter`
- `llm.model_name`: `qwen/qwen3.5-9b`
- `llm.temperature`: `0.2`
- `retrieval.top_k`: `10`
- `retrieval.dense_weight`: `0.6`
- `retrieval.bm25_weight`: `0.4`
- `reranking.model`: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- `reranking.device`: `cpu`
- `reranking.top_k`: `5`

### `logging.yaml`

File này chứa cấu hình logging của dự án.

Các thành phần hiện có:

- `formatters.simple`: định dạng log theo thời gian, level, tên logger và message.
- `handlers.console`: ghi log ra stdout.
- `handlers.file`: ghi log vào `logs/application.log`.
- `loggers`: cấu hình logger theo module.
- `root`: cấu hình logger mặc định.

Các logger đã được khai báo:

- `ingestion`
- `embedding`
- `scoring`
- `vector_database`
- `llm`
- `retrieval`
- `reranking`
- `chat`

Logger `scoring` hiện phục vụ `scoring/bm25.py`. Logger `reranking` hiện phục vụ các module trong `reranking`. Hai key `retrieval.dense_weight` và `retrieval.bm25_weight` hiện được `retrieval/hybrid_retriever.py` dùng để tính `hybrid_score = dense_weight * dense_score + bm25_weight * bm25_score`. Nhóm `reranking` hiện chứa model CrossEncoder, thiết bị chạy và số document cuối cùng sau rerank.

## Cách Hoạt Động Hiện Tại

`core/settings_loader.py` đọc `settings.yaml` và ghi đè một số giá trị bằng biến môi trường nếu có.

`core/logging_setup.py` đọc `logging.yaml`, tạo thư mục `logs` nếu cần và áp dụng cấu hình logging.

Các file trong thư mục này không tự chạy. Chúng được các module trong `core` đọc và chuyển thành cấu hình Python.

## Ghi Chú Kỹ Thuật

Các field API key trong `settings.yaml` đang để `null`. Giá trị thật được kỳ vọng lấy từ biến môi trường.

Tài liệu này không ghi nội dung `.env`.

Comment trong YAML hiện chủ yếu là tiếng Việt không dấu hoặc có dấu lẫn nhau, còn tên key cấu hình dùng tiếng Anh.
