# README_chunking

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra mã nguồn hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.

## Nhiệm Vụ Của Thư Mục

Thư mục `ingestion/chunking` chứa mã chuyển dữ liệu đã xử lý thành chunk.

Tính tới thời điểm hiện tại, thư mục này mới có mã chunking cho file `architectureTypes.json`.

## File Hiện Có

### `architectureTypes.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `json`, `logging`, `Path` và `datetime`.
- Import `load_settings` từ `core.settings_loader`.
- Import `make_metadata` từ `ingestion.helpers.make_metadata`.
- Gọi `load_settings()` để lấy cấu hình.
- Tạo logger tên `ingestion`.
- Định nghĩa hàm `chunk_architecture_types()`.

Hàm `chunk_architecture_types()` hiện đang làm các việc sau:

- Tạo đường dẫn tới `data/processed/architectureTypes.json`.
- Kiểm tra file có tồn tại không.
- Đọc file JSON bằng UTF-8.
- Bắt lỗi `json.JSONDecodeError` nếu JSON không hợp lệ.
- Nếu dữ liệu đọc được là dictionary thì chuyển thành list chứa một dictionary.
- Kiểm tra dữ liệu có phải list không.
- Kiểm tra list có rỗng không.
- Duyệt từng phần tử trong list.
- Bỏ qua phần tử không phải dictionary.
- Lấy các field `id`, `slug`, `name`, `description`.
- Tạo `base_metadata`.
- Nếu có cả `name` và `description`, tạo text tiếng Việt.
- Gọi `make_metadata(...)` để tạo metadata cuối cùng.
- Thêm dictionary gồm `text` và `metadata` vào danh sách `chunks`.
- Trả về danh sách `chunks`.

Các field trong `base_metadata` hiện có:

- `type`
- `architecture_type_id`
- `architecture_type_name`
- `architecture_type_slug`
- `source`
- `created_at`
- `language`

Text chunk hiện được tạo từ:

- Tên phong cách kiến trúc.
- Mô tả phong cách kiến trúc.

## Cách Hoạt Động Hiện Tại

File này đọc dữ liệu từ:

```text
data/processed/architectureTypes.json
```

Kết quả trả về của hàm là list các dictionary. Mỗi dictionary có hai key:

- `text`
- `metadata`

## Ghi Chú Kỹ Thuật

Mã nguồn hiện import `ingestion.helpers.make_metadata`. Trong cây thư mục hiện tại, tôi không thấy thư mục `ingestion/helpers` trong lần kiểm tra này.

Trong dữ liệu mẫu đã kiểm tra, nhiều bản ghi `architectureTypes.json` có `description` là `null`. Mã hiện tại chỉ tạo chunk khi có cả `name` và `description`.

Timestamp `created_at` trong metadata được tạo bằng `datetime.utcnow().isoformat()`.
