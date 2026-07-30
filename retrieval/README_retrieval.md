# README_retrieval

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Rút gọn nội dung vì file trong thư mục hiện chưa có dòng mã nguồn nào.
- 2026-07-24 21:24 +07 - Bổ sung mô tả trạng thái và nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-24 21:39 +07 - Chuẩn hóa phần mô tả nhiệm vụ các file mã nguồn.
- 2026-07-26 16:54 +07 - Cập nhật trạng thái sau buổi 6: `retriever.py` đã có code truy vấn Qdrant nhưng chưa chạy được nguyên vẹn vì `core/schema.py` vẫn rỗng.
- 2026-07-26 21:02 +07 - Cập nhật trạng thái sau buổi 7: `core/schema.py` đã có `RetrievedDocument`, nên module retrieval import được.
- 2026-07-30 10:54 +07 - Cập nhật trạng thái sau `tai_lieu/p2/4.txt`: repo đã có sparse embedder, nhưng retrieval hiện vẫn truy vấn dense vector từ Qdrant.

## Nhiệm Vụ Của Thư Mục

Thư mục `retrieval` chứa mã truy xuất tài liệu liên quan từ vector store.

Tính tới sau buổi 7, thư mục này đã có code embedding query, truy vấn collection Qdrant và chuẩn hóa kết quả truy vấn thành document. `core/schema.py` đã định nghĩa `RetrievedDocument`, nên module retrieval hiện import được.

Sau `tai_lieu/p2/4.txt`, repo đã có `embedding/sparse_embedder.py`, nhưng `retrieval/retriever.py` hiện chưa import hoặc dùng sparse embedding. Luồng retrieval hiện vẫn là dense-only.

## File Tài Liệu Trong Thư Mục

### `README_retrieval.md`

File này mô tả nhiệm vụ của thư mục `retrieval`, trạng thái hiện tại của từng file mã nguồn và trạng thái chạy của luồng retrieval.

## Nhiệm Vụ Các File Mã Nguồn

### `retriever.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `logging`.
- Import `QdrantClient`, `ScoredPoint` và `ResponseHandlingException` từ `qdrant_client`.
- Import `load_settings` từ `core.settings_loader`.
- Import `RetrievedDocument` từ `core.schema`.
- Import `get_qdrant_client` từ `vectorstore.qdrant`.
- Import `embed_texts` từ `embedding.embedder`.
- Đọc cấu hình `retrieval` và tên collection Qdrant từ settings.
- Định nghĩa hàm `retrieve(query: str) -> list[RetrievedDocument]`.

Hàm `retrieve()` hiện đang làm các việc sau:

- Kiểm tra query rỗng hoặc chỉ có khoảng trắng; nếu rỗng thì log warning và trả về list rỗng.
- Lấy Qdrant client bằng `get_qdrant_client()`.
- Gọi `embed_texts([query])` để chuyển query thành dense vector.
- Lấy vector đầu tiên vì input chỉ có một query.
- Gọi `client.query_points(...)` với `collection_name`, query vector, `limit`, `with_payload=True` và `score_threshold`.
- Lấy `response.points`.
- Duyệt từng `ScoredPoint`, lấy payload, tách `text` ra khỏi metadata.
- Tạo `RetrievedDocument` với `id`, `score`, `text` và `metadata`.
- Log số lượng document truy xuất được và trả về list document.
- Nếu Qdrant lỗi kết nối kiểu `ResponseHandlingException`, hàm raise `ConnectionError`.
- Với lỗi khác, hàm log lỗi kèm traceback và trả về list rỗng.

Vai trò và luồng hoạt động:

- `retriever.py` chịu trách nhiệm lấy câu hỏi người dùng, embedding câu hỏi, tìm các point liên quan trong Qdrant và trả về danh sách tài liệu có thể dùng làm context cho LLM.
- Input chính là `query: str`.
- Output dự kiến là `list[RetrievedDocument]`, mỗi document gồm `id`, `score`, `text` và `metadata`.
- Trạng thái chạy hiện tại: module import được sau khi `core/schema.py` có `RetrievedDocument`. Luồng truy vấn thật vẫn cần Qdrant đang chạy, collection đã có dữ liệu và embedding model load được. Module này chưa dùng `embedding.sparse_embedder`.

### `__init__.py`

File này hiện đang rỗng.

File đánh dấu `retrieval` là Python package.

## Cách Hoạt Động Hiện Tại

Luồng retrieval theo code hiện tại:

1. Nhận query dạng text.
2. Chuyển query thành dense embedding bằng `embedding.embedder.embed_texts`.
3. Truy vấn Qdrant collection `nmk_chatbot_collection`.
4. Lấy payload gồm `text` và metadata từ các point đạt ngưỡng score.
5. Chuẩn hóa kết quả về schema `RetrievedDocument`.

Luồng này hiện không còn dừng ở bước import schema. Khi chạy thật, kết quả phụ thuộc trạng thái Qdrant local và collection `nmk_chatbot_collection`.

Sparse embedding chưa được dùng trong bước truy vấn hiện tại.

## Ghi Chú Kỹ Thuật

Cấu hình retrieval hiện lấy từ `config/settings.yaml`:

- `retrieval.top_k`: `10`
- `retrieval.score_threshold`: `0.0`

Qdrant collection hiện lấy từ `vector_database.collection_name`, đang là `nmk_chatbot_collection`.
