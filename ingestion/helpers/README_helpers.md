# README_helpers

## Nhật Ký Cập Nhật

- 2026-07-25 18:42 +07 - Tạo README cho thư mục `ingestion/helpers` sau khi kiểm tra mã nguồn hiện tại.

## Nhiệm Vụ Của Thư Mục

Thư mục `ingestion/helpers` chứa helper dùng chung cho các module chunking trong `ingestion/chunking`.

## File Tài Liệu Trong Thư Mục

### `README_helpers.md`

File này mô tả nhiệm vụ của thư mục `ingestion/helpers` và nhiệm vụ hiện tại của từng file mã nguồn trong thư mục.

## Nhiệm Vụ Các File Mã Nguồn

### `make_metadata.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `uuid`.
- Định nghĩa hàm `make_metadata(base, **extra)`.

Hàm `make_metadata()` hiện merge dictionary `base` với các field bổ sung trong `extra`, đồng thời thêm `chunk_id` dạng UUID string.

### `split_paragraphs.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `logging`.
- Tạo logger tên `ingestion`.
- Định nghĩa hàm `split_paragraphs(text, max_len=400)`.

Hàm `split_paragraphs()` hiện trả về list rỗng nếu input rỗng. Với text có nội dung, hàm chia text theo dấu `. `, gom câu vào buffer tối đa `max_len`, cắt cứng theo `max_len` khi câu quá dài và trả về danh sách đoạn text.
