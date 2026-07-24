# README_ingestion

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra mã nguồn hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.

## Nhiệm Vụ Của Thư Mục

Thư mục `ingestion` chứa mã xử lý dữ liệu đầu vào.

Tính tới thời điểm hiện tại, phần đã có mã nguồn chính là đọc file JSON gốc và tách dữ liệu theo từng bảng.

## Các File Và Thư Mục Hiện Có

### `load_data.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `json`, `logging`, `Path` và `sys`.
- Xác định `PROJECT_ROOT`.
- Thêm project root vào `sys.path` nếu chưa có.
- Import `load_settings` từ `core.settings_loader`.
- Gọi `load_settings()` để lấy cấu hình.
- Tạo logger tên `ingestion`.
- Định nghĩa hàm `load_data()`.
- Nếu chạy trực tiếp file này, gọi `load_data()`.

Hàm `load_data()` hiện đang làm các việc sau:

- Đọc file `data/raw/database_export_2026-01-14T02-32-14.json`.
- Nếu dữ liệu rỗng thì log lỗi và dừng.
- Lấy object `tables`.
- Nếu không có `tables` thì log warning và dừng.
- Duyệt từng cặp `table_name`, `table_data`.
- Nếu `table_data` rỗng thì log warning và bỏ qua.
- Tạo đường dẫn output `data/processed/<table_name>.json`.
- Ghi dữ liệu bảng ra file JSON.
- Dùng `ensure_ascii=False` để giữ tiếng Việt.
- Dùng `indent=4` để file JSON dễ đọc hơn.
- Log thông tin sau khi ghi xong từng bảng.

### `pipeline.py`

File này hiện có trong thư mục nhưng chưa có nội dung.

Trạng thái hiện tại:

- File tồn tại.
- File đang rỗng.
- Chưa có dòng mã nguồn nào trong file.

### `chunking/`

Thư mục con này chứa mã chunking.

Hiện tại trong thư mục `chunking` có file `architectureTypes.py` đã có mã nguồn.

## Cách Hoạt Động Hiện Tại

Luồng ingestion hiện có:

1. Gọi `load_settings()` để đọc cấu hình.
2. Đọc file JSON gốc từ `data/raw`.
3. Lấy object `tables`.
4. Bỏ qua bảng rỗng.
5. Ghi từng bảng có dữ liệu sang `data/processed`.

## Ghi Chú Kỹ Thuật

File `load_data.py` hiện đang viết trực tiếp tên file JSON gốc trong mã nguồn.

Logger đang dùng tên `ingestion`.

Dữ liệu được đọc và ghi bằng UTF-8.

Thư mục `__pycache__` có thể xuất hiện khi chạy Python, nhưng đó là file sinh tự động và không thuộc phạm vi tài liệu này.
