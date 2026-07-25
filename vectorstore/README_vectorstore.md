# README_vectorstore

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Rút gọn nội dung vì các file trong thư mục hiện chưa có dòng mã nguồn nào.
- 2026-07-24 21:24 +07 - Bổ sung mô tả trạng thái và nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-24 21:39 +07 - Chuẩn hóa phần mô tả nhiệm vụ các file mã nguồn.
- 2026-07-25 18:42 +07 - Cập nhật theo mã nguồn hiện tại sau buổi 4: `qdrant.py`, `index.py` và `upsert.py` đã có code, nhưng luồng import/upsert hiện chưa chạy được nguyên vẹn.

## Nhiệm Vụ Của Thư Mục

Thư mục `vectorstore` chứa mã chuẩn bị kết nối Qdrant, tạo collection và chuyển chunk thành point để lưu vào vector store.

Tính tới thời điểm kiểm tra này, thư mục đã có code ở cả ba file Python, nhưng chưa xác nhận chạy được end-to-end vì còn lỗi import trong môi trường hiện tại.

## File Tài Liệu Trong Thư Mục

### `README_vectorstore.md`

File này mô tả nhiệm vụ của thư mục `vectorstore`, trạng thái từng file mã nguồn và các điểm chưa chạy được theo mã nguồn hiện tại.

## Nhiệm Vụ Các File Mã Nguồn

### `qdrant.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `QdrantClient` từ `qdrant_client`.
- Import `VectorParams`, `Distance`, `SparseVectorParams` và `SparseIndexParams`.
- Đọc cấu hình `vector_database` từ `core.settings_loader.load_settings()`.
- Lấy `collection_name`, `vector_size`, `distance` và `timeout` từ settings.
- Dùng biến module `_client` để cache Qdrant client.
- Định nghĩa hàm `get_qdrant_client()`.
- Định nghĩa hàm `ensure_collection(client)`.

Hàm `get_qdrant_client()` hiện kết nối Qdrant bằng `url` nếu settings có `vector_database.url`, nếu không thì kết nối bằng `host` và `port`. Sau khi tạo client, hàm gọi `get_collections()` để kiểm tra kết nối.

Hàm `ensure_collection(client)` hiện lấy danh sách collection hiện có. Nếu collection cấu hình đã tồn tại thì log và dừng. Nếu chưa tồn tại, hàm gọi `recreate_collection()` để tạo collection có vector dense tên `dense` và sparse vector tên `sparse`.

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

### `upsert.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `QdrantClient`.
- Import `load_settings` từ `core.settings_loader`.
- Import `get_qdrant_client` và `ensure_collection` từ `vectorstore.qdrant`.
- Import `build_hybrid_qdrant_points` và `init_sparse_embedder` từ `vectorstore.hybrid_index`.
- Import `SparseEmbedder` từ `embedding.sparse_embedder`.
- Định nghĩa hàm `upsert_chunks(chunks: list[dict])`.

Hàm `upsert_chunks()` hiện kiểm tra chunks rỗng, lấy Qdrant client, đảm bảo collection tồn tại, fit sparse embedder bằng corpus text, build hybrid points và gọi `client.upsert(...)`.

## Trạng Thái Chạy Hiện Tại

Luồng `vectorstore` hiện chưa import được nguyên vẹn trong môi trường `uv run` hiện tại.

Các vấn đề đã xác minh:

- `import vectorstore.qdrant` đang trỏ tới package `vectorstore` trong `.venv/site-packages`, không trỏ tới thư mục local `vectorstore` của repo. Nguyên nhân quan sát được là `pyproject.toml` đang có dependency tên `vectorstore`, trong khi thư mục local cũng tên `vectorstore`.
- `vectorstore/upsert.py` đang import `vectorstore.hybrid_index`, nhưng file `vectorstore/hybrid_index.py` hiện không tồn tại trong repo.
- `vectorstore/upsert.py` đang import `embedding.sparse_embedder`, nhưng file `embedding/sparse_embedder.py` hiện không tồn tại trong repo.

Vì các lỗi trên, chưa thể xác nhận `upsert_chunks()` chạy end-to-end với Qdrant trong trạng thái hiện tại.

## Ghi Chú Kỹ Thuật

Buổi 4 trong `tai_lieu/4.txt` trình bày các bước embedding, kết nối Qdrant, tạo collection, build point và upsert chunk vào vector store. Mã nguồn hiện tại đã phản ánh một phần nội dung đó ở `embedding` và `vectorstore`, nhưng trạng thái chạy end-to-end vẫn chưa hoàn chỉnh.
