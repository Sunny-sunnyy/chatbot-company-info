# README_reranking

## Nhật Ký Cập Nhật

- 2026-07-31 17:07 +07 - Tạo README cho thư mục `reranking` sau khi đọc `tai_lieu/p2/9.txt` và đối chiếu với mã nguồn reranking hiện tại.
- 2026-07-31 17:22 +07 - Bổ sung mô tả rõ trách nhiệm của từng file `.py` trong thư mục `reranking`.

## Nhiệm Vụ Của Thư Mục

Thư mục `reranking` chứa code rerank danh sách document đã retrieval trước khi build context cho LLM.

Mục tiêu của reranking là nhận query và các `RetrievedDocument` từ retrieval, chấm điểm lại từng cặp query/document bằng CrossEncoder, sắp xếp document theo độ liên quan mới và trả về các document tốt nhất.

Trạng thái hiện tại: thư mục đã có code reranking, nhưng API route hiện chưa gọi reranker này trong luồng chat.

## File Tài Liệu Trong Thư Mục

### `README_reranking.md`

File này mô tả nhiệm vụ của thư mục `reranking`, trạng thái từng file mã nguồn và trạng thái chạy hiện tại của luồng reranking.

## Nhiệm Vụ Các File Mã Nguồn

### `base.py`

File này đã có mã nguồn.

Trách nhiệm chính của file:

- Định nghĩa interface chung cho các reranker trong dự án.
- Quy định chữ ký method `rerank(query, documents, top_k=None)` mà các class reranker cụ thể phải triển khai.
- Giữ kiểu input/output thống nhất với schema `RetrievedDocument`.
- Không thực hiện reranking thật; file chỉ raise `NotImplementedError` để class con bắt buộc tự cài logic.

Nội dung hiện tại:

- Import `RetrievedDocument` từ `core.schema`.
- Định nghĩa class `BaseReranker`.
- Định nghĩa method `rerank(query, documents, top_k=None)`.

Vai trò và luồng hoạt động:

- `BaseReranker` đóng vai trò interface chung cho các reranker.
- Method `rerank(...)` nhận `query: str`, `documents: list[RetrievedDocument]` và `top_k` tùy chọn.
- Method hiện raise `NotImplementedError`, buộc class con phải tự triển khai logic rerank thật.
- Output kỳ vọng của class con là `list[RetrievedDocument]`.

### `reranker.py`

File này đã có mã nguồn.

Trách nhiệm chính của file:

- Triển khai reranker thật bằng CrossEncoder.
- Nhận query và danh sách `RetrievedDocument` đã được retrieval trước đó.
- Tạo cặp `(query, document_text)` cho từng document.
- Gọi `CrossEncoderModel.score_batch(...)` để chấm điểm độ liên quan của từng cặp query/document.
- Ghi `rerank_score` vào metadata của từng document.
- Sort document theo `rerank_score` giảm dần.
- Cắt kết quả theo `top_k` nếu được truyền vào.
- Trả về list `RetrievedDocument` đã được rerank để bước context builder hoặc LLM dùng tiếp.

Nội dung hiện tại:

- Import `logging`.
- Import `RetrievedDocument` từ `core.schema`.
- Import `BaseReranker` từ `reranking.base`.
- Import `CrossEncoderModel` từ `reranking.models.cross_encoder`.
- Tạo logger tên `reranking`.
- Định nghĩa class `CrossEncoderReranker`.

Vai trò và luồng hoạt động:

- `CrossEncoderReranker` kế thừa `BaseReranker`.
- `__init__(model)` nhận một object `CrossEncoderModel` đã được khởi tạo.
- `rerank(query, documents, top_k=None)` trả list rỗng nếu không có document.
- Hàm tạo các cặp `(query, doc.text)` cho từng document.
- Hàm gọi `self.model.score_batch(pairs)` để lấy score từ CrossEncoder.
- Hàm ghi `rerank_score` vào `doc.metadata` cho từng document.
- Hàm sort document theo `rerank_score` giảm dần.
- Nếu `top_k` có giá trị, hàm cắt list document về `top_k`.
- Output là `list[RetrievedDocument]` đã được rerank.

Trạng thái hiện tại:

- File đã có code reranking bằng CrossEncoder.
- File chưa được API route hoặc frontend gọi.
- Chưa có automated test riêng cho `CrossEncoderReranker`.

### `__init__.py`

File này hiện đang rỗng.

File đánh dấu `reranking` là Python package. File không chứa logic xử lý reranking.

## Thư Mục Con Hiện Có

### `models/`

Thư mục này chứa wrapper model dùng cho reranking.

README chi tiết nằm ở `reranking/models/README_models.md`.

## Cách Hoạt Động Hiện Tại

Luồng reranking dự kiến theo code hiện có:

1. Chuẩn bị query của người dùng.
2. Nhận list `RetrievedDocument` từ retrieval hoặc hybrid retrieval.
3. Khởi tạo `CrossEncoderModel` bằng model name và device từ cấu hình reranking.
4. Tạo `CrossEncoderReranker(model)`.
5. Gọi `rerank(query, documents, top_k=...)`.
6. Nhận lại document đã sort theo `rerank_score`.

Luồng này hiện mới có ở mức module mã nguồn. API route hiện vẫn chưa gọi reranker.

## Ghi Chú Kỹ Thuật

Cấu hình reranking hiện nằm trong `config/settings.yaml`:

- `reranking.model`: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- `reranking.device`: `cpu`
- `reranking.top_k`: `5`

Logger `reranking` đã được khai báo trong `config/logging.yaml`.
