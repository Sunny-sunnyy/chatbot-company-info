# README_helpers

## Nhật Ký Cập Nhật

- 2026-07-25 18:42 +07 - Tạo README cho thư mục `ingestion/helpers` sau khi kiểm tra mã nguồn hiện tại.
- 2026-07-25 20:22 +07 - Bổ sung giải thích vai trò và luồng hoạt động của các helper mã nguồn.

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

Vai trò và luồng hoạt động:

- `make_metadata.py` chịu trách nhiệm chuẩn hóa metadata cho các chunk trước khi đưa sang bước embedding/vector store.
- `make_metadata(base, **extra)` nhận metadata nền từ file chunking, tự sinh `chunk_id` bằng `uuid.uuid4()`, rồi merge thêm các field phụ như `chunk_type`, `priority` hoặc `part_index`.
- Output là một dictionary metadata mới, giúp mỗi chunk có định danh riêng để dùng làm `id` hoặc payload trong vector store.

### `split_paragraphs.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `logging`.
- Tạo logger tên `ingestion`.
- Định nghĩa hàm `split_paragraphs(text, max_len=400)`.

Hàm `split_paragraphs()` hiện trả về list rỗng nếu input rỗng. Với text có nội dung, hàm chia text theo dấu `. `, gom câu vào buffer tối đa `max_len`, cắt cứng theo `max_len` khi câu quá dài và trả về danh sách đoạn text.

Vai trò và luồng hoạt động:

- `split_paragraphs.py` chịu trách nhiệm chia text dài thành các đoạn nhỏ hơn để các module chunking không tạo chunk quá dài.
- `split_paragraphs(text, max_len=400)` nhận một chuỗi text và giới hạn độ dài đoạn.
- Hàm tách text theo câu, ghép câu vào buffer nếu còn trong giới hạn, và cắt câu quá dài theo `max_len` khi không tìm được dấu ngắt phù hợp.
- Output là list các đoạn text, đang được dùng bởi `news.py` và `projects.py`.
