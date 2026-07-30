# README_vectorstore

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Rút gọn nội dung vì các file trong thư mục hiện chưa có dòng mã nguồn nào.
- 2026-07-24 21:24 +07 - Bổ sung mô tả trạng thái và nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-24 21:39 +07 - Chuẩn hóa phần mô tả nhiệm vụ các file mã nguồn.
- 2026-07-25 18:42 +07 - Cập nhật theo mã nguồn hiện tại sau buổi 4: `qdrant.py`, `index.py` và `upsert.py` đã có code, nhưng luồng import/upsert hiện chưa chạy được nguyên vẹn.
- 2026-07-25 20:22 +07 - Bổ sung giải thích vai trò và luồng hoạt động của các file mã nguồn vector store.
- 2026-07-26 12:23 +07 - Cập nhật trạng thái sau buổi 5: `qdrant.py` và `upsert.py` chuyển về dense-only, pipeline đã upsert 450 chunks vào Qdrant theo kết quả chạy thực tế của người dùng.
- 2026-07-30 10:54 +07 - Cập nhật trạng thái sau `tai_lieu/p2/4.txt`: repo đã có `embedding/sparse_embedder.py`, nhưng vector store hiện vẫn dense-only; bổ sung trạng thái `hybrid_index.py` đang rỗng.

## Nhiệm Vụ Của Thư Mục

Thư mục `vectorstore` chứa mã kết nối Qdrant, đảm bảo collection tồn tại, chuyển chunk thành Qdrant point và upsert point vào vector store.

Tính tới thời điểm kiểm tra này, luồng vector store hiện đang dùng dense vector đơn thuần, chưa dùng hybrid search hoặc sparse vector. Repo đã có `embedding/sparse_embedder.py`, nhưng file này chưa được import hoặc dùng trong các file mã nguồn đang chạy của thư mục `vectorstore`.

## File Tài Liệu Trong Thư Mục

### `README_vectorstore.md`

File này mô tả nhiệm vụ của thư mục `vectorstore`, trạng thái từng file mã nguồn và trạng thái chạy hiện tại của luồng upsert vào Qdrant.

## Nhiệm Vụ Các File Mã Nguồn

### `qdrant.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `QdrantClient` từ `qdrant_client`.
- Import `Distance` và `VectorParams` từ `qdrant_client.models`.
- Đọc cấu hình `vector_database` từ `core.settings_loader.load_settings()`.
- Lấy `collection_name`, `vector_size`, `distance` và `timeout` từ settings.
- Dùng biến module `_client` để cache Qdrant client.
- Định nghĩa hàm `get_qdrant_client()`.
- Định nghĩa hàm `ensure_collection(client)`.

Hàm `get_qdrant_client()` hiện kết nối Qdrant bằng `url` nếu settings có `vector_database.url`, nếu không thì kết nối bằng `host` và `port`. Sau khi tạo client, hàm gọi `get_collections()` để kiểm tra kết nối.

Hàm `ensure_collection(client)` hiện lấy danh sách collection đang có trong Qdrant. Nếu collection cấu hình đã tồn tại thì log và dừng. Nếu chưa tồn tại, hàm gọi `recreate_collection()` để tạo collection dense-only bằng `VectorParams(size=VECTOR_SIZE, distance=Distance[DISTANCE.upper()])`.

Vai trò và luồng hoạt động:

- `qdrant.py` chịu trách nhiệm quản lý kết nối tới Qdrant và đảm bảo collection lưu trữ tồn tại.
- `get_qdrant_client()` dùng pattern singleton ở cấp module: nếu `_client` đã có thì trả về lại client cũ, tránh tạo kết nối mới ở mỗi lần gọi.
- Khi chưa có `_client`, hàm đọc cấu hình Qdrant từ settings, ưu tiên kết nối bằng `url`; nếu không có `url` thì dùng `host` và `port`.
- Sau khi tạo client, hàm gọi `_client.get_collections()` để kiểm tra kết nối thật với Qdrant.
- `ensure_collection(client)` kiểm tra collection theo `COLLECTION_NAME`. Nếu chưa có, hàm tạo collection dense-only, không tạo sparse vector.
- Input chính là cấu hình `vector_database` trong `config/settings.yaml` và Qdrant service đang chạy.
- Output chính là một `QdrantClient` đã kết nối và collection `nmk_chatbot_collection` đã sẵn sàng nếu Qdrant chạy được.

### `index.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `logging` và `uuid`.
- Import `embed_texts` từ `embedding.embedder`.
- Tạo logger tên `embedding`.
- Định nghĩa hàm `build_qdrant_points(chunks: list[dict])`.

Hàm `build_qdrant_points()` hiện kiểm tra input rỗng, lấy `text` từ từng chunk, gọi `embed_texts(texts)` để tạo dense embedding, rồi build danh sách point dạng dictionary gồm:

- `id`: lấy từ `metadata.chunk_id` nếu có, nếu không thì tạo UUID mới.
- `vector`: embedding vector.
- `payload`: chứa `text` và metadata của chunk.

Vai trò và luồng hoạt động:

- `index.py` chịu trách nhiệm chuyển danh sách chunk văn bản thành point dense-only mà Qdrant có thể lưu.
- `build_qdrant_points(chunks)` lấy toàn bộ `chunk["text"]`, gọi `embed_texts(texts)` để biến text thành dense embedding.
- Vòng lặp `zip(chunks, embeddings)` ghép từng chunk với vector tương ứng, giữ đúng quan hệ một text một vector.
- Mỗi point là dictionary gồm `id`, `vector` và `payload`.
- `payload` chứa nội dung gốc trong key `text` và bung toàn bộ metadata bằng `**chunk.get("metadata", {})`.
- Input chính là `list[dict]` chunk từ `ingestion/pipeline.py`.
- Output chính là `list[dict]` point để truyền cho `client.upsert(...)`.

### `upsert.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `logging`.
- Import `QdrantClient` từ `qdrant_client`.
- Import `load_settings` từ `core.settings_loader`.
- Import `get_qdrant_client` và `ensure_collection` từ `vectorstore.qdrant`.
- Import `build_qdrant_points` từ `vectorstore.index`.
- Định nghĩa hàm `upsert_chunks(chunks: list[dict])`.

Hàm `upsert_chunks()` hiện kiểm tra chunks rỗng, lấy Qdrant client, đảm bảo collection tồn tại, build dense-only point từ chunks và gọi `client.upsert(...)` để ghi point vào collection cấu hình.

Vai trò và luồng hoạt động:

- `upsert.py` chịu trách nhiệm điều phối bước ghi chunk đã xử lý vào Qdrant.
- `upsert_chunks(chunks)` lấy Qdrant client qua `get_qdrant_client()`, gọi `ensure_collection(client)`, rồi gọi `build_qdrant_points(chunks)`.
- Nếu không build được point nào, hàm log warning và trả về list rỗng.
- Nếu có point, hàm gọi `client.upsert(collection_name=COLLECTION_NAME, points=points)`.
- Input chính là list chunk có key `text` và `metadata`.
- Output trực tiếp của hàm không trả về dữ liệu khi upsert thành công; trạng thái được ghi qua log.
- Trạng thái hiện tại: file này không import `vectorstore.hybrid_index` hoặc `embedding.sparse_embedder`; sparse embedding chưa được build thành Qdrant point.

### `hybrid_index.py`

File này hiện đang rỗng và chưa được phát triển.

File chưa có import, hàm, class hoặc luồng xử lý. Không có code nào trong thư mục `vectorstore` đang gọi file này.

## Trạng Thái Chạy Hiện Tại

Sau buổi 5, người dùng đã bật Qdrant bằng Docker Compose, chạy:

```bash
uv run python -m ingestion.pipeline
```

Kết quả chạy thực tế đã ghi nhận:

- Kết nối Qdrant qua URL thành công.
- Collection `nmk_chatbot_collection` được tạo thành công.
- Embedding model `intfloat/multilingual-e5-small` được load.
- `build_qdrant_points()` build 450 Qdrant points.
- `upsert_chunks()` upsert 450 points vào collection `nmk_chatbot_collection`.
- `run_ingestion_pipeline()` log đã upsert 450 chunks vào vector store.

Trong quá trình chunking có nhiều warning `Empty text provided to split_paragraphs`. Các warning này phản ánh một số bản ghi có nội dung rỗng hoặc thiếu text để chia đoạn, nhưng luồng ingestion vẫn hoàn tất và upsert thành công.

## Ghi Chú Kỹ Thuật

Luồng hiện tại là dense-only. Collection được tạo bằng unnamed dense vector theo cấu trúc point từ `vectorstore/index.py`.

Qdrant đang được cấu hình trong `config/settings.yaml` với:

- `vector_database.url`: `http://localhost:6333`
- `vector_database.collection_name`: `nmk_chatbot_collection`
- `vector_database.distance`: `cosine`
- `vector_database.vector_size`: `384`

Qdrant service được chạy bằng Docker Compose ở thư mục gốc dự án. Dữ liệu Qdrant local hiện được mount vào `qdrant_storage/` theo cấu hình trong `docker-compose.yml`.
