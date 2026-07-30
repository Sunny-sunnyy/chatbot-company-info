# README_retrieval

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Rút gọn nội dung vì file trong thư mục hiện chưa có dòng mã nguồn nào.
- 2026-07-24 21:24 +07 - Bổ sung mô tả trạng thái và nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-24 21:39 +07 - Chuẩn hóa phần mô tả nhiệm vụ các file mã nguồn.
- 2026-07-26 16:54 +07 - Cập nhật trạng thái sau buổi 6: `retriever.py` đã có code truy vấn Qdrant nhưng chưa chạy được nguyên vẹn vì `core/schema.py` vẫn rỗng.
- 2026-07-26 21:02 +07 - Cập nhật trạng thái sau buổi 7: `core/schema.py` đã có `RetrievedDocument`, nên module retrieval import được.
- 2026-07-30 10:54 +07 - Cập nhật trạng thái sau `tai_lieu/p2/4.txt`: repo đã có sparse embedder, nhưng retrieval hiện vẫn truy vấn dense vector từ Qdrant.
- 2026-07-30 12:20 +07 - Cập nhật trạng thái sau `tai_lieu/p2/6.txt` và `tai_lieu/p2/7.txt`: bổ sung `hybrid_retriever.py`, lý thuyết BM25/hybrid retrieval, cách triển khai và ví dụ trong dự án.

## Nhiệm Vụ Của Thư Mục

Thư mục `retrieval` chứa mã truy xuất tài liệu liên quan từ vector store.

Tính tới sau buổi 7, thư mục này đã có code embedding query, truy vấn collection Qdrant và chuẩn hóa kết quả truy vấn thành document. `core/schema.py` đã định nghĩa `RetrievedDocument`, nên module retrieval hiện import được.

Sau `tai_lieu/p2/7.txt`, repo đã có thêm `retrieval/hybrid_retriever.py` để kết hợp dense retrieval với BM25 score. Luồng API hiện tại vẫn chưa gọi hybrid retriever; route chat hiện vẫn dùng `retrieval/retriever.py`.

## Lý Thuyết BM25 Và Hybrid Retrieval

Dense retrieval và BM25 giải quyết hai phần khác nhau của truy xuất:

- Dense retrieval: chuyển query thành vector ngữ nghĩa và tìm document gần nghĩa trong Qdrant. Cách này tốt khi người dùng hỏi khác từ nhưng cùng ý.
- BM25: tính mức liên quan keyword giữa query và document. Cách này tốt khi query có từ khóa quan trọng như địa điểm, diện tích, con số, tên loại công trình.
- Hybrid retrieval: lấy kết quả dense trước, sau đó cộng thêm BM25 score để rerank theo cả ngữ nghĩa và keyword.

Trong code hiện tại, công thức trộn score nằm trong `hybrid_retriever.py`:

```python
hybrid_score = DENSE_WEIGHT * dense_score + BM25_WEIGHT * bm25_score
```

Giá trị mặc định lấy từ `config/settings.yaml`:

- `dense_weight`: `0.6`
- `bm25_weight`: `0.4`

Ví dụ trong dự án:

- Query: `Dự án biệt thự ở Bình Phước diện tích 520m2`.
- Dense retrieval có thể tìm các chunk liên quan tới biệt thự hoặc dự án nhà ở dù không trùng toàn bộ keyword.
- BM25 tăng điểm cho chunk thật sự chứa `Bình Phước` và `520m2`.
- Hybrid retriever trả về document có `score` cuối cùng, đồng thời lưu `dense_score` và `bm25_score` trong metadata để debug.

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

### `hybrid_retriever.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `logging` và `List`.
- Import `QdrantClient`, `ScoredPoint` và `ResponseHandlingException`.
- Import `load_settings`, `RetrievedDocument`, `get_qdrant_client`, `embed_texts` và `BM25`.
- Đọc `collection_name`, `top_k`, `score_threshold`, `dense_weight` và `bm25_weight` từ settings.
- Định nghĩa hàm `hybrid_retrieve(query: str, bm25: BM25) -> List[RetrievedDocument]`.

Vai trò và luồng hoạt động:

- `hybrid_retrieve(query, bm25)` nhận query của người dùng và một object `BM25` đã được chuẩn bị sẵn.
- Hàm kiểm tra query rỗng.
- Hàm tạo dense embedding cho query bằng `embed_texts([query])`.
- Hàm truy vấn Qdrant bằng `client.query_points(...)` với `using="dense"` và `limit=TOP_K * 3` để lấy dư document trước khi rerank.
- Với từng point trả về, hàm lấy `payload["text"]`, tính `bm25.score(query, text)`, rồi tính hybrid score.
- Hàm tạo `RetrievedDocument` với `score` là hybrid score và metadata có thêm `dense_score`, `bm25_score`.
- Hàm sort document theo hybrid score giảm dần và trả về `TOP_K` document đầu.

Input/output:

- Input chính: `query: str` và `bm25: BM25`.
- Output chính: `list[RetrievedDocument]`.
- Mỗi `RetrievedDocument.metadata` có thêm `dense_score` và `bm25_score` để xem document mạnh vì ngữ nghĩa hay keyword.

Ví dụ áp dụng:

- Dense score của một chunk dự án là `0.72`.
- BM25 score giữa query `Bình Phước 520m2` và chunk là `1.8`.
- Với `dense_weight=0.6`, `bm25_weight=0.4`, score cuối là `0.6 * 0.72 + 0.4 * 1.8 = 1.152`.
- Chunk này có thể vượt một chunk khác chỉ gần nghĩa nhưng không chứa keyword địa điểm/diện tích.

Trạng thái hiện tại:

- File đã có code hybrid retrieval.
- File phụ thuộc Qdrant collection có named vector `dense`, vì query gọi `using="dense"`.
- Pipeline/upsert hiện chưa tạo collection/point hybrid tương ứng.
- API route hiện chưa gọi `hybrid_retrieve()`, nên luồng chat đang chạy chưa dùng hybrid retriever.

### `__init__.py`

File này hiện đang rỗng.

File đánh dấu `retrieval` là Python package.

## Cách Hoạt Động Hiện Tại

Luồng retrieval dense-only theo code hiện tại:

1. Nhận query dạng text.
2. Chuyển query thành dense embedding bằng `embedding.embedder.embed_texts`.
3. Truy vấn Qdrant collection `nmk_chatbot_collection`.
4. Lấy payload gồm `text` và metadata từ các point đạt ngưỡng score.
5. Chuẩn hóa kết quả về schema `RetrievedDocument`.

Luồng này hiện không còn dừng ở bước import schema. Khi chạy thật, kết quả phụ thuộc trạng thái Qdrant local và collection `nmk_chatbot_collection`.

Luồng hybrid retrieval đã có code riêng trong `hybrid_retriever.py`, nhưng chưa được nối vào API.

## Ghi Chú Kỹ Thuật

Cấu hình retrieval hiện lấy từ `config/settings.yaml`:

- `retrieval.top_k`: `10`
- `retrieval.score_threshold`: `0.0`
- `retrieval.dense_weight`: `0.6`
- `retrieval.bm25_weight`: `0.4`

Qdrant collection hiện lấy từ `vector_database.collection_name`, đang là `nmk_chatbot_collection`.
