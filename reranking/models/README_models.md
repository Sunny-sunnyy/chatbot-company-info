# README_models

## Nhật Ký Cập Nhật

- 2026-07-31 17:07 +07 - Tạo README cho thư mục `reranking/models` sau khi đọc `tai_lieu/p2/9.txt` và đối chiếu với mã nguồn CrossEncoder hiện tại.
- 2026-07-31 17:22 +07 - Bổ sung mô tả rõ trách nhiệm của từng file `.py` trong thư mục `reranking/models`.

## Nhiệm Vụ Của Thư Mục

Thư mục `reranking/models` chứa wrapper model phục vụ bước reranking.

Hiện tại thư mục này có code load CrossEncoder từ `sentence_transformers` và chấm điểm theo batch cho các cặp query/document.

## File Tài Liệu Trong Thư Mục

### `README_models.md`

File này mô tả nhiệm vụ của thư mục `reranking/models` và trạng thái từng file mã nguồn trong thư mục.

## Nhiệm Vụ Các File Mã Nguồn

### `cross_encoder.py`

File này đã có mã nguồn.

Trách nhiệm chính của file:

- Bọc `sentence_transformers.CrossEncoder` thành một class nhỏ dùng riêng cho reranking.
- Load CrossEncoder model theo `model_name` và `device` được truyền vào.
- Nhận danh sách cặp `(query, document_text)`.
- Gọi model để dự đoán score liên quan cho từng cặp query/document.
- Chuyển kết quả model về `list[float]` để `CrossEncoderReranker` có thể gắn score vào metadata document.
- Tách phần model inference khỏi logic sort/cắt top document trong `reranking/reranker.py`.

Nội dung hiện tại:

- Import `logging`.
- Import `CrossEncoder` từ `sentence_transformers`.
- Tạo logger tên `reranking`.
- Định nghĩa class `CrossEncoderModel`.

Vai trò và luồng hoạt động:

- `CrossEncoderModel` là wrapper mỏng quanh `sentence_transformers.CrossEncoder`.
- `__init__(model_name, device="cpu")` load CrossEncoder theo tên model và thiết bị truyền vào.
- `score_batch(pairs)` nhận list cặp `(query, document_text)`.
- Hàm gọi `self.model.predict(pairs).tolist()` để trả list score dạng `list[float]`.
- Output của file này được `reranking/reranker.py` dùng để gắn `rerank_score` vào metadata document.

Input/output:

- Input của `__init__`: `model_name: str`, `device: str`.
- Input của `score_batch`: `list[tuple[str, str]]`.
- Output của `score_batch`: `list[float]`.

Trạng thái hiện tại:

- File đã có code load và gọi CrossEncoder.
- File chưa có automated test riêng.
- File chỉ load model thật khi khởi tạo `CrossEncoderModel`, không phải khi import module.

### `__init__.py`

File này hiện đang rỗng.

File đánh dấu `reranking/models` là Python package. File không chứa logic load model hoặc scoring.

## Cách Hoạt Động Hiện Tại

`reranking/reranker.py` import `CrossEncoderModel` từ file này, tạo cặp query/document, rồi gọi `score_batch(...)` để lấy rerank score.

Code hiện tại chưa nối wrapper model này vào API route.
