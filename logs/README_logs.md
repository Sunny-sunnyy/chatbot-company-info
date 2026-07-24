# README_logs

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 21:24 +07 - Bổ sung mô tả nhiệm vụ hiện tại của từng file trong thư mục.

## Nhiệm Vụ Của Thư Mục

Thư mục `logs` chứa file log được tạo khi ứng dụng chạy.

## File Hiện Có

### `README_logs.md`

File này mô tả nhiệm vụ của thư mục `logs` và trạng thái hiện tại của file log trong thư mục.

### `application.log`

Trạng thái hiện tại:

- File tồn tại.
- File đang rỗng.
- File này là đường dẫn được khai báo trong `config/logging.yaml`.

Nhiệm vụ hiện tại của file:

- Lưu log khi cấu hình logging ghi ra file.
- Tính tới thời điểm cập nhật này, file chưa có nội dung log.

## Cách Hoạt Động Hiện Tại

`config/logging.yaml` khai báo `FileHandler` ghi log vào:

```text
logs/application.log
```

`core/logging_setup.py` tạo thư mục `logs` nếu cần và áp dụng cấu hình logging từ YAML.

## Ghi Chú Kỹ Thuật

Đây là thư mục chứa file sinh ra khi chạy ứng dụng, không chứa mã nguồn Python.

Log format hiện được khai báo trong `config/logging.yaml`.
