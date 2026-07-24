# README_raw

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra dữ liệu hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 21:24 +07 - Bổ sung mô tả nhiệm vụ hiện tại của từng file trong thư mục.

## Nhiệm Vụ Của Thư Mục

Thư mục `data/raw` chứa dữ liệu gốc chưa tách bảng.

Tính tới thời điểm hiện tại, đây là nơi lưu file JSON export ban đầu để `ingestion/load_data.py` đọc vào.

## File Hiện Có

### `README_raw.md`

File này mô tả nhiệm vụ của thư mục `data/raw` và nhiệm vụ hiện tại của file dữ liệu gốc trong thư mục.

### `database_export_2026-01-14T02-32-14.json`

Đây là file JSON gốc hiện tại.

Cấu trúc cấp cao quan sát được:

- `exportDate`: thời gian export dữ liệu.
- `database`: loại database nguồn, hiện là `postgres`.
- `tables`: object chứa dữ liệu theo từng bảng.

Các bảng trong `tables`:

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

## Cách Hoạt Động Hiện Tại

`ingestion/load_data.py` đang đọc trực tiếp file:

```text
data/raw/database_export_2026-01-14T02-32-14.json
```

Mã nguồn lấy dữ liệu từ object `tables` trong file này và ghi các bảng không rỗng sang `data/processed`.

## Ghi Chú Kỹ Thuật

File này là dữ liệu đầu vào gốc của dự án.

Dữ liệu có tiếng Việt nên cần đọc bằng encoding UTF-8.

Tên file JSON gốc hiện đang được viết trực tiếp trong `ingestion/load_data.py`.
