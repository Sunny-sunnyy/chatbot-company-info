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
- 2026-07-30 12:20 +07 - Cập nhật trạng thái sau `tai_lieu/p2/5.txt`: `hybrid_index.py` đã có code build dense+sparse point; bổ sung lý thuyết, cách triển khai và ví dụ áp dụng hybrid index trong dự án.
- 2026-07-31 15:45 +07 - Bổ sung mô tả rõ trách nhiệm của `hybrid_index.py` trong luồng chuẩn bị point hybrid dense+sparse cho Qdrant.
- 2026-08-01 16:51 +07 - Cập nhật trạng thái sau khi đọc `tai_lieu/p2/10.txt`: `qdrant.py` tạo collection hybrid khi collection chưa tồn tại và `upsert.py` đã chuyển sang build/upsert hybrid points.
- 2026-08-01 17:58 +07 - Cập nhật trạng thái sau p2 hoàn chỉnh: ghi rõ lỗi `Not existing vector name error: sparse` xảy ra khi upsert hybrid vào collection Qdrant cũ dense-only.

## Nhiệm Vụ Của Thư Mục

Thư mục `vectorstore` chứa mã kết nối Qdrant, đảm bảo collection tồn tại, chuyển chunk thành Qdrant point và upsert point vào vector store.

Tính tới thời điểm kiểm tra này, luồng vector store chính trong `upsert.py` đã chuyển sang hybrid dense+sparse. `vectorstore/index.py` vẫn còn là builder dense-only cũ, nhưng `vectorstore/upsert.py` hiện không gọi file này.

`vectorstore/qdrant.py` tạo collection có named vector `dense` và sparse vector `sparse` khi collection chưa tồn tại. Nếu collection `nmk_chatbot_collection` đã tồn tại từ luồng dense-only cũ, code hiện chỉ log rồi trả về, không tự migrate schema.

## Lý Thuyết Hybrid Index

Hybrid index trong dự án này là cách lưu cùng một chunk dưới hai biểu diễn:

- Dense vector: vector ngữ nghĩa từ `SentenceTransformer`, phù hợp với câu hỏi diễn đạt gần nghĩa nhưng không trùng từ.
- Sparse vector: vector keyword từ `SparseEmbedder`, phù hợp với câu hỏi có token quan trọng như địa danh, con số, diện tích, loại công trình hoặc mức đầu tư.

Ví dụ trong dự án:

- Chunk dự án có text chứa `Biệt thự hiện đại tại Bình Phước, mức đầu tư 500 triệu`.
- Dense vector giúp truy vấn `mẫu nhà sang trọng ở tỉnh miền Đông` vẫn có cơ hội tìm được document gần nghĩa.
- Sparse vector giúp truy vấn `Bình Phước 500 triệu` không bị mất hai keyword quan trọng `bình/phước` và `500/triệu`.

Hybrid index không thay thế dense index; nó lưu thêm sparse vector song song để bước retrieval sau này có thể kết hợp dense score và keyword score.

## File Tài Liệu Trong Thư Mục

### `README_vectorstore.md`

File này mô tả nhiệm vụ của thư mục `vectorstore`, trạng thái từng file mã nguồn và trạng thái chạy hiện tại của luồng upsert vào Qdrant.

## Nhiệm Vụ Các File Mã Nguồn

### `qdrant.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `QdrantClient` từ `qdrant_client`.
- Import `VectorParams`, `Distance`, `SparseVectorParams` và `SparseIndexParams` từ `qdrant_client.models`.
- Đọc cấu hình `vector_database` từ `core.settings_loader.load_settings()`.
- Lấy `collection_name`, `vector_size`, `distance` và `timeout` từ settings.
- Dùng biến module `_client` để cache Qdrant client.
- Định nghĩa hàm `get_qdrant_client()`.
- Định nghĩa hàm `ensure_collection(client)`.

Hàm `get_qdrant_client()` hiện kết nối Qdrant bằng `url` nếu settings có `vector_database.url`, nếu không thì kết nối bằng `host` và `port`. Sau khi tạo client, hàm gọi `get_collections()` để kiểm tra kết nối.

Hàm `ensure_collection(client)` hiện lấy danh sách collection đang có trong Qdrant. Nếu collection cấu hình đã tồn tại thì log và dừng. Nếu chưa tồn tại, hàm gọi `recreate_collection()` để tạo collection hybrid gồm named vector `dense` và sparse vector `sparse`.

Vai trò và luồng hoạt động:

- `qdrant.py` chịu trách nhiệm quản lý kết nối tới Qdrant và đảm bảo collection lưu trữ tồn tại.
- `get_qdrant_client()` dùng pattern singleton ở cấp module: nếu `_client` đã có thì trả về lại client cũ, tránh tạo kết nối mới ở mỗi lần gọi.
- Khi chưa có `_client`, hàm đọc cấu hình Qdrant từ settings, ưu tiên kết nối bằng `url`; nếu không có `url` thì dùng `host` và `port`.
- Sau khi tạo client, hàm gọi `_client.get_collections()` để kiểm tra kết nối thật với Qdrant.
- `ensure_collection(client)` kiểm tra collection theo `COLLECTION_NAME`. Nếu chưa có, hàm tạo collection hybrid với `vectors_config={"dense": VectorParams(...)}` và `sparse_vectors_config={"sparse": SparseVectorParams(...)}`.
- Input chính là cấu hình `vector_database` trong `config/settings.yaml` và Qdrant service đang chạy.
- Output chính là một `QdrantClient` đã kết nối và collection `nmk_chatbot_collection` đã sẵn sàng nếu Qdrant chạy được.
- Trạng thái chạy cần lưu ý: collection cũ dense-only không được tự xoá hoặc tự migrate. Trước khi upsert hybrid point, cần đảm bảo collection hiện có đúng schema hybrid hoặc xoá collection cũ để pipeline tạo lại.

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

Trạng thái hiện tại:

- File vẫn tồn tại để build dense-only points.
- File hiện không được `vectorstore/upsert.py` gọi trong luồng pipeline sau cập nhật `p2/10`.

### `upsert.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `logging`.
- Import `QdrantClient` từ `qdrant_client`.
- Import `load_settings` từ `core.settings_loader`.
- Import `get_qdrant_client` và `ensure_collection` từ `vectorstore.qdrant`.
- Import `build_hybrid_qdrant_points` và `init_sparse_embedder` từ `vectorstore.hybrid_index`.
- Import `SparseEmbedder` từ `embedding.sparse_embedder`.
- Định nghĩa hàm `upsert_chunks(chunks: list[dict])`.

Hàm `upsert_chunks()` hiện kiểm tra chunks rỗng, lấy Qdrant client, đảm bảo collection tồn tại, fit sparse embedder trên corpus chunk, build hybrid point từ chunks và gọi `client.upsert(...)` để ghi point vào collection cấu hình.

Vai trò và luồng hoạt động:

- `upsert.py` chịu trách nhiệm điều phối bước ghi chunk đã xử lý vào Qdrant.
- `upsert_chunks(chunks)` lấy Qdrant client qua `get_qdrant_client()`, gọi `ensure_collection(client)`, tạo `texts = [chunk["text"] for chunk in chunks]`, khởi tạo `SparseEmbedder()`, fit sparse embedder trên `texts`, gọi `init_sparse_embedder(sparse_embedder)`, rồi gọi `build_hybrid_qdrant_points(chunks)`.
- Nếu không build được point nào, hàm log warning và trả về list rỗng.
- Nếu có point, hàm gọi `client.upsert(collection_name=COLLECTION_NAME, points=points)`.
- Input chính là list chunk có key `text` và `metadata`.
- Output trực tiếp của hàm không trả về dữ liệu khi upsert thành công; trạng thái được ghi qua log.
- Trạng thái hiện tại: file đã chuyển sang upsert hybrid points. Khi chạy thật, Qdrant phải có collection schema tương thích với named vector `dense` và sparse vector `sparse`.

### `hybrid_index.py`

File này đã có mã nguồn.

Trách nhiệm chính của file:

- Chuẩn bị Qdrant point theo hướng hybrid, tức mỗi chunk có cả dense vector và sparse vector.
- Nhận `SparseEmbedder` đã được fit trước đó qua `init_sparse_embedder(...)` để dùng cùng một vocabulary/document frequency cho toàn bộ batch chunk.
- Tạo dense embedding từ text bằng `embedding.embedder.embed_texts(...)`.
- Tạo sparse vector từ text bằng `SparseEmbedder.encode_batch(...)`.
- Ghép `id`, `payload`, named vector `dense` và named vector `sparse` thành `PointStruct` phù hợp với Qdrant collection kiểu hybrid.
- Giữ phần build point hybrid tách riêng khỏi luồng dense-only trong `vectorstore/index.py`.

Nội dung hiện tại:

- Import `logging` và `uuid`.
- Import `PointStruct` và `SparseVector` từ `qdrant_client.models`.
- Import `embed_texts` từ `embedding.embedder`.
- Import `SparseEmbedder` từ `embedding.sparse_embedder`.
- Tạo logger tên `vector_database`.
- Khai báo biến module `_sparse_embedder`.
- Định nghĩa hàm `init_sparse_embedder(embedder)`.
- Định nghĩa hàm `build_hybrid_qdrant_points(chunks)`.

Vai trò và luồng hoạt động:

- `init_sparse_embedder(embedder)` nhận một `SparseEmbedder` đã fit vocabulary/document frequency và lưu vào biến module `_sparse_embedder`.
- `build_hybrid_qdrant_points(chunks)` nhận list chunk có key `text` và `metadata`.
- Hàm lấy toàn bộ `text`, tạo dense embedding bằng `embed_texts(texts)`, tạo sparse embedding bằng `_sparse_embedder.encode_batch(texts)`.
- Với mỗi chunk, hàm tạo `PointStruct` có `id`, `payload` và `vector` gồm hai named vectors:
  - `dense`: dense vector từ `SentenceTransformer`.
  - `sparse`: `SparseVector(indices=..., values=...)` từ sparse embedder.
- Output là `list[PointStruct]` để có thể truyền cho Qdrant upsert khi collection hỗ trợ named vectors.

Ví dụ triển khai trong dự án:

1. Chunk text: `Dự án biệt thự tại Bình Phước có diện tích 520m2`.
2. Dense vector được tạo bằng `embed_texts([text])`.
3. Sparse vector có thể chứa token ids cho `dự`, `án`, `biệt`, `thự`, `bình`, `phước`, `520m2` cùng weight tương ứng.
4. Qdrant point dự kiến có dạng logic:

```python
{
    "id": "<chunk_id>",
    "vector": {
        "dense": [...],
        "sparse": {"indices": [...], "values": [...]},
    },
    "payload": {"text": "...", "...metadata": "..."},
}
```

Trạng thái hiện tại:

- File đã có code build hybrid point.
- File yêu cầu gọi `init_sparse_embedder(...)` trước khi build point; nếu chưa gọi sẽ raise `RuntimeError`.
- File hiện được `vectorstore/upsert.py` gọi trong luồng pipeline.
- `vectorstore/qdrant.py` hiện tạo collection hybrid khi collection chưa tồn tại.

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

Sau cập nhật `p2/10`, người dùng đã chạy pipeline hybrid và gặp lỗi Qdrant:

```text
Wrong input: Not existing vector name error: sparse
```

Theo code hiện tại, nguyên nhân là collection `nmk_chatbot_collection` đã tồn tại từ luồng dense-only cũ nên `ensure_collection()` chỉ log rồi return, không tạo lại schema có sparse vector. `upsert.py` sau đó gửi point có vector `sparse` vào collection không có vector name này, nên Qdrant trả `400 Bad Request`.

Kiểm tra tĩnh trước đó đã pass:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile core/startup.py vectorstore/qdrant.py vectorstore/upsert.py vectorstore/hybrid_index.py ingestion/pipeline.py retrieval/hybrid_retriever.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import importlib; importlib.import_module('ingestion.pipeline'); print('ingestion.pipeline import ok')"
```

Để upsert thật thành công với code hiện tại, collection trong Qdrant phải có named vector `dense` và sparse vector `sparse`. Nếu còn collection dense-only cũ, cần xoá collection cũ hoặc dùng collection name mới trước khi chạy lại pipeline.

## Ghi Chú Kỹ Thuật

Luồng đang chạy qua pipeline hiện tại là hybrid dense+sparse. Collection mới được tạo bằng named vector `dense` và sparse vector `sparse`, còn point được build bằng `PointStruct` trong `vectorstore/hybrid_index.py`.

Nếu Qdrant vẫn còn collection cũ dense-only từ lần chạy trước, `ensure_collection()` không tự migrate collection đó. Khi đó cần xoá collection cũ rồi chạy lại pipeline để tạo collection hybrid và upsert lại dữ liệu.

Qdrant đang được cấu hình trong `config/settings.yaml` với:

- `vector_database.url`: `http://localhost:6333`
- `vector_database.collection_name`: `nmk_chatbot_collection`
- `vector_database.distance`: `cosine`
- `vector_database.vector_size`: `384`

Qdrant service được chạy bằng Docker Compose ở thư mục gốc dự án. Dữ liệu Qdrant local hiện được mount vào `qdrant_storage/` theo cấu hình trong `docker-compose.yml`.
