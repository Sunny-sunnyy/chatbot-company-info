# README_embedding

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Rút gọn nội dung vì các file trong thư mục hiện chưa có dòng mã nguồn nào.
- 2026-07-24 21:24 +07 - Bổ sung mô tả trạng thái và nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-24 21:39 +07 - Chuẩn hóa phần mô tả nhiệm vụ các file mã nguồn.
- 2026-07-25 17:23 +07 - Cập nhật theo mã nguồn hiện tại: `embedder.py` và `batch_embed.py` đã có code, các file cũ `embed_texts.py` và `batch_embed_texts.py` không còn trong thư mục.
- 2026-07-25 18:42 +07 - Đối chiếu với nội dung buổi 4 và xác nhận mã embedding hiện có khớp phần load model, encode text và batch embedding.
- 2026-07-25 20:22 +07 - Bổ sung giải thích vai trò và luồng hoạt động của các file mã nguồn embedding.
- 2026-07-30 10:54 +07 - Cập nhật trạng thái sau `tai_lieu/p2/3.txt` và `tai_lieu/p2/4.txt`: bổ sung `sparse_embedder.py`, ghi rõ sparse embedding chưa được nối vào vector store/retrieval và bổ sung trạng thái `__init__.py`.
- 2026-07-30 12:20 +07 - Cập nhật trạng thái sau `tai_lieu/p2/5.txt`, `tai_lieu/p2/6.txt` và `tai_lieu/p2/7.txt`: `SparseEmbedder` hiện được dùng bởi hybrid index và BM25 scorer, nhưng chưa nằm trong luồng ingestion/API chính.
- 2026-08-01 17:58 +07 - Cập nhật trạng thái sau p2 hoàn chỉnh: `SparseEmbedder` đã nằm trong pipeline hybrid, startup RAG components và luồng `/api/chat`.

## Nhiệm Vụ Của Thư Mục

Thư mục `embedding` chứa mã tạo embedding từ text.

Tính tới thời điểm hiện tại, thư mục này có code load model `SentenceTransformer`, tạo dense embedding cho danh sách text, xử lý dense embedding theo batch và file sparse embedder dựa trên token/TF-IDF.

Nội dung dense embedding khớp với phần embedding trong `tai_lieu/4.txt`: load model một lần, dùng device từ settings, encode text thành vector và xử lý danh sách text theo batch.

Nội dung sparse embedding khớp với `tai_lieu/p2/3.txt` và `tai_lieu/p2/4.txt`: phân tích vì sao dense embedding có thể bỏ lỡ keyword quan trọng, sau đó code sparse embedder với token, vocabulary, document frequency, term frequency và inverse document frequency.

## File Tài Liệu Trong Thư Mục

### `README_embedding.md`

File này mô tả trạng thái hiện tại của thư mục `embedding` và nhiệm vụ hiện tại của từng file mã nguồn trong thư mục.

## Nhiệm Vụ Các File Mã Nguồn

### `embedder.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `logging` và `SentenceTransformer`.
- Import `load_settings` từ `core.settings_loader`.
- Đọc cấu hình `embedding` từ settings.
- Lấy tên model từ key `embedding.model`.
- Dùng biến module `_model` để cache model sau lần load đầu tiên.
- Định nghĩa hàm `get_model()`.
- Định nghĩa hàm `embed_texts(texts: list[str])`.

Hàm `get_model()` hiện load `SentenceTransformer` bằng model trong settings và device trong `embedding.device`, mặc định là `cpu` nếu không có cấu hình device.

Hàm `embed_texts()` hiện trả về list rỗng nếu input rỗng. Với input có text, hàm gọi model encode với `normalize_embeddings=True`, `convert_to_tensor=False`, chuyển kết quả sang list và trả về `list[list[float]]`.

Vai trò và luồng hoạt động:

- `embedder.py` chịu trách nhiệm load model embedding và chuyển text thành dense vector.
- `get_model()` dùng pattern singleton ở cấp module: nếu `_model` đã có thì trả về lại model cũ, nếu chưa có thì load `SentenceTransformer` theo model và device trong settings.
- `embed_texts(texts)` nhận list chuỗi, gọi `get_model()`, encode toàn bộ text với `normalize_embeddings=True`, rồi chuyển kết quả sang list Python để có thể lưu vào Qdrant.
- Input chính là `list[str]`.
- Output chính là `list[list[float]]`, mỗi vector tương ứng với một text đầu vào.

### `batch_embed.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `logging`.
- Import `load_settings` từ `core.settings_loader`.
- Import `embed_texts` từ `embedding.embedder`.
- Đọc `embedding.batch_size` từ settings, mặc định là `32` nếu không có cấu hình.
- Định nghĩa hàm `batch_embed_texts(texts: list[str])`.

Hàm `batch_embed_texts()` hiện trả về list rỗng nếu input rỗng. Với input có text, hàm chia danh sách text thành các batch theo `BATCH_SIZE`, gọi `embed_texts()` cho từng batch, gộp toàn bộ embedding vào `all_embeddings` và trả về kết quả.

Vai trò và luồng hoạt động:

- `batch_embed.py` chịu trách nhiệm chia danh sách text lớn thành nhiều batch nhỏ để tránh xử lý toàn bộ corpus trong một lần gọi model.
- `BATCH_SIZE` được đọc từ `settings["embedding"]["batch_size"]`, mặc định là `32` nếu không có cấu hình.
- `batch_embed_texts(texts)` duyệt danh sách text theo bước nhảy `BATCH_SIZE`, gọi `embed_texts(batch)` cho từng batch, rồi nối kết quả vào `all_embeddings`.
- Input chính là `list[str]`.
- Output chính là `list[list[float]]` đã giữ đúng thứ tự tương ứng với danh sách text đầu vào.

### `sparse_embedder.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `math`, `logging`, `re` và `Counter`.
- Tạo logger tên `embedding`.
- Định nghĩa hàm `tokenize(text: str) -> list[str]`.
- Định nghĩa class `SparseEmbedder`.
- `SparseEmbedder.__init__()` khởi tạo `vocabulary`, `document_frequency` và `num_documents`.
- `SparseEmbedder.__update_vocabulary(tokens)` cập nhật vocabulary và document frequency từ token duy nhất trong từng document.
- `SparseEmbedder.fit(texts)` fit sparse embedder trên danh sách text.
- `SparseEmbedder.__inverse_document_frequency(term)` tính IDF bằng công thức `log((num_documents + 1) / (document_frequency + 1)) + 1`.
- `SparseEmbedder.encode(text)` encode một text thành sparse vector.
- `SparseEmbedder.encode_batch(texts)` encode danh sách text bằng cách gọi `encode()` cho từng text.

Vai trò và luồng hoạt động:

- `sparse_embedder.py` chịu trách nhiệm tạo biểu diễn sparse để giữ keyword quan trọng song song với dense embedding.
- `tokenize(text)` chuyển text về chữ thường, thay ký tự đặc biệt bằng khoảng trắng qua regex, rồi tách token bằng `split()`.
- `fit(texts)` nhận `list[str]`, token hóa từng text, cập nhật `vocabulary` dạng `token -> id`, cập nhật `document_frequency` bằng `set(tokens)` để mỗi token chỉ tính một lần trên mỗi document, và lưu `num_documents`.
- `encode(text)` nhận một chuỗi text, token hóa, tính term frequency bằng `Counter`, bỏ qua token chưa có trong vocabulary, rồi trả dictionary gồm `indices` và `values`.
- Output của `encode(text)` có dạng `{"indices": list[int], "values": list[float]}`.
- `encode_batch(texts)` trả `list[dict[str, list[float]]]`, mỗi phần tử tương ứng với một text đầu vào.
- Trạng thái chạy hiện tại: file tồn tại và được CodeGraph index, nhưng chưa có automated test riêng. File hiện được `vectorstore/upsert.py` fit trên corpus chunk, được `vectorstore/hybrid_index.py` dùng để build sparse vector, được `core/startup.py` fit lại từ corpus trong Qdrant để khởi tạo BM25, và được `scoring/bm25.py` dùng để lấy `tokenize`, `vocabulary`, `document_frequency` và `num_documents`. Endpoint `POST /api/chat` đi qua BM25 trong `retrieval/hybrid_retriever.py`.

Ví dụ áp dụng trong dự án:

- Với query `biệt thự Bình Phước 500 triệu`, dense embedding giúp bắt ý nghĩa gần như thiết kế biệt thự hoặc dự án dân dụng.
- Sparse embedding giữ các keyword như `bình`, `phước`, `500`, `triệu` thành sparse indices/values để các bước hybrid/BM25 có thể tăng điểm cho document thật sự chứa những token này.
- Trong code hiện tại, sparse vector này được chuẩn bị bởi `SparseEmbedder.encode_batch(texts)` khi `vectorstore/hybrid_index.py` được gọi từ `vectorstore/upsert.py`.

### `__init__.py`

File này hiện đang rỗng.

File đánh dấu `embedding` là Python package.
