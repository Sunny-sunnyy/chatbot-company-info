# README_scoring

## Nhật Ký Cập Nhật

- 2026-07-30 12:20 +07 - Tạo README cho thư mục `scoring` sau khi đọc `tai_lieu/p2/6.txt`, `tai_lieu/p2/7.txt` và đối chiếu với code BM25 hiện tại.
- 2026-07-31 16:09 +07 - Bổ sung mô tả rõ trách nhiệm của `bm25.py` trong luồng tính keyword relevance cho hybrid retrieval.

## Nhiệm Vụ Của Thư Mục

Thư mục `scoring` chứa code tính điểm liên quan giữa query và document.

Tính tới thời điểm hiện tại, thư mục này có code BM25 để hỗ trợ hybrid retrieval. BM25 không thay thế dense retrieval; nó bổ sung keyword relevance score để `retrieval/hybrid_retriever.py` có thể trộn dense score và BM25 score.

## Lý Thuyết BM25 Trong Dự Án

BM25 trả lời câu hỏi: document này liên quan tới query bao nhiêu dựa trên keyword?

Dense embedding trả lời bằng ngữ nghĩa tổng thể. Ví dụ query `nhà phố hiện đại` có thể tìm được document về `thiết kế nhà ở phong cách hiện đại` dù không trùng toàn bộ từ. BM25 bổ sung phần còn thiếu: nếu query có keyword cụ thể như `Bình Phước`, `520m2`, `500 triệu`, BM25 giúp document thật sự chứa các token này được tăng điểm.

BM25 trong code dùng các thành phần chính:

- `document_frequency`: số document chứa một term, lấy từ `SparseEmbedder`.
- `term_frequency`: số lần term của query xuất hiện trong document đang xét.
- `num_documents`: tổng số document đã fit trong `SparseEmbedder`.
- `average_document_length`: độ dài token trung bình của các document hợp lệ.
- `k1`: hệ số điều chỉnh mức tăng điểm khi term lặp lại trong document, mặc định `1.5`.
- `b`: hệ số phạt/thưởng theo độ dài document, mặc định `0.75`.

Ý nghĩa triển khai:

- Term xuất hiện trong ít document có khả năng phân biệt cao hơn, nên IDF cao hơn.
- Term lặp lại trong một document giúp tăng điểm, nhưng `k1` làm mức tăng bão hòa để tránh spam từ khóa.
- Document quá dài bị điều chỉnh bởi `b` vì document dài thường có nhiều cơ hội chứa từ khóa hơn.

Ví dụ trong dự án:

- Query: `biệt thự Bình Phước 520m2`.
- Document A chứa `biệt thự`, `Bình Phước`, `520m2`.
- Document B chỉ chứa `biệt thự hiện đại`.
- Dense retrieval có thể thấy cả A và B gần nghĩa, nhưng BM25 sẽ cho A điểm keyword cao hơn vì trùng các token quan trọng.

## File Tài Liệu Trong Thư Mục

### `README_scoring.md`

File này mô tả nhiệm vụ của thư mục `scoring`, lý thuyết BM25, cách triển khai và trạng thái từng file mã nguồn trong thư mục.

## Nhiệm Vụ Các File Mã Nguồn

### `bm25.py`

File này đã có mã nguồn.

Trách nhiệm chính của file:

- Tính điểm liên quan keyword giữa query và document theo công thức BM25.
- Dùng `SparseEmbedder` đã fit để lấy `vocabulary`, `document_frequency` và `num_documents`.
- Tính độ dài trung bình của tập document để điều chỉnh điểm theo độ dài document.
- Token hóa query và document bằng cùng hàm `tokenize(...)` trong `embedding/sparse_embedder.py`.
- Tính điểm cho từng term trong query dựa trên IDF, term frequency, `k1` và `b`.
- Trả về BM25 score cho một document hoặc danh sách score cho nhiều document.
- Cung cấp điểm keyword để `retrieval/hybrid_retriever.py` trộn với dense score khi rerank kết quả retrieval.

Nội dung hiện tại:

- Import `logging`, `math` và `Counter`.
- Import `tokenize` và `SparseEmbedder` từ `embedding.sparse_embedder`.
- Tạo logger tên `scoring`.
- Định nghĩa class `BM25`.
- `BM25.__init__(sparse_embedder, k1=1.5, b=0.75)` lưu sparse embedder, `k1`, `b`, `num_documents` và `average_document_length`.
- `BM25.compute_average_document_length(documents)` tính độ dài document trung bình theo số token.
- `BM25.score(query, document)` tính BM25 score cho một query/document.
- `BM25.score_batch(query, documents)` tính score cho nhiều document.

Vai trò và luồng hoạt động:

- `BM25` dùng `SparseEmbedder` đã fit sẵn để lấy vocabulary, document frequency và tổng số document.
- `compute_average_document_length(documents)` nhận danh sách document text, token hóa từng document, bỏ qua document rỗng, cộng tổng số token và chia cho số document hợp lệ.
- `score(query, document)` token hóa query và document, duyệt từng term duy nhất trong query, bỏ qua term không có trong vocabulary hoặc không xuất hiện trong document, rồi cộng BM25 score của từng term.
- `score_batch(query, documents)` chỉ là helper gọi `score(query, document)` cho từng document.

Input/output:

- Input của `compute_average_document_length`: `list[str]` document text.
- Output của `compute_average_document_length`: không return dữ liệu; hàm cập nhật `self.average_document_length`.
- Input của `score`: `query: str`, `document: str`.
- Output của `score`: `float`, điểm BM25.
- Input của `score_batch`: `query: str`, `documents: list[str]`.
- Output của `score_batch`: `list[float]`.

Cách áp dụng trong dự án:

1. Fit `SparseEmbedder` trên toàn bộ chunk text.
2. Tạo `BM25(sparse_embedder)`.
3. Gọi `bm25.compute_average_document_length(texts)`.
4. Trong retrieval, với mỗi document candidate từ Qdrant, gọi `bm25.score(query, text)`.
5. Trộn score bằng `hybrid_score = dense_weight * dense_score + bm25_weight * bm25_score`.

Ví dụ cụ thể:

```python
from embedding.sparse_embedder import SparseEmbedder
from scoring.bm25 import BM25

texts = [
    "Dự án biệt thự tại Bình Phước diện tích 520m2",
    "Thiết kế nhà phố hiện đại tại Quận 7",
]

sparse_embedder = SparseEmbedder()
sparse_embedder.fit(texts)

bm25 = BM25(sparse_embedder)
bm25.compute_average_document_length(texts)

score = bm25.score("biệt thự Bình Phước 520m2", texts[0])
```

Trạng thái hiện tại:

- File đã có code BM25.
- File được `retrieval/hybrid_retriever.py` import.
- Chưa có automated test riêng cho `BM25`.
- Chưa có API route đang gọi hybrid retriever, nên BM25 chưa nằm trong luồng chat đang chạy.

### `__init__.py`

File này hiện đang rỗng.

File đánh dấu `scoring` là Python package.
