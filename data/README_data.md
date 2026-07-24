# README_data

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra dữ liệu hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 21:24 +07 - Bổ sung mô tả nhiệm vụ hiện tại của từng file trong thư mục.

## Nhiệm Vụ Của Thư Mục

Thư mục `data` chứa dữ liệu của dự án.

Tính tới thời điểm hiện tại, thư mục này có hai nhóm dữ liệu:

- Dữ liệu gốc trong `data/raw`.
- Dữ liệu đã được tách theo bảng trong `data/processed`.

## File Hiện Có Trong Thư Mục Này

### `README_data.md`

File này mô tả nhiệm vụ của thư mục `data`, các thư mục con chứa dữ liệu, trạng thái dữ liệu hiện tại và cách dữ liệu được tạo bởi ingestion.

## Các Thư Mục Con Hiện Có

### `raw`

Thư mục `data/raw` chứa file JSON gốc.

File hiện có:

- `database_export_2026-01-14T02-32-14.json`

File này là đầu vào của `ingestion/load_data.py`.

### `processed`

Thư mục `data/processed` chứa các file JSON đã được tách từ file gốc.

Các file hiện có:

- `architectureTypes.json`
- `companyInfo.json`
- `heroSlides.json`
- `interiorStyles.json`
- `news.json`
- `newsCategories.json`
- `projectCategories.json`
- `projects.json`

Các file này được tạo từ các bảng không rỗng trong file JSON gốc.

## Cách Hoạt Động Hiện Tại

Luồng xử lý dữ liệu hiện tại:

1. `ingestion/load_data.py` đọc file JSON trong `data/raw`.
2. Mã nguồn lấy object `tables`.
3. Mã nguồn bỏ qua bảng không có dữ liệu.
4. Mã nguồn ghi từng bảng có dữ liệu thành file riêng trong `data/processed`.

## Trạng Thái Dữ Liệu Hiện Tại

File JSON gốc có 10 bảng:

- `settings`: 0 bản ghi
- `companyInfo`: 1 bản ghi
- `heroSlides`: 10 bản ghi
- `interiorStyles`: 10 bản ghi
- `architectureTypes`: 15 bản ghi
- `projectCategories`: 12 bản ghi
- `projects`: 49 bản ghi
- `newsCategories`: 4 bản ghi
- `news`: 17 bản ghi
- `users`: 0 bản ghi

Chỉ các bảng có dữ liệu mới có file trong `data/processed`.

## Ghi Chú Kỹ Thuật

Dữ liệu có nội dung tiếng Việt, nên mã đọc/ghi JSON cần dùng UTF-8.

Trong `config/settings.yaml`, đường dẫn dữ liệu hiện được cấu hình như sau:

- `data.raw_dir`: `data/raw`
- `data.processed_dir`: `data/processed`
- `data.schema_dir`: `data/schemas`

Thư mục `data/schemas` chưa tồn tại trong cây thư mục hiện tại.
