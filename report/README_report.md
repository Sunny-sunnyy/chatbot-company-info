# README_report

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 20:31 +07 - Bổ sung mô tả file `Agent_session_prompt.md`.

## Nhiệm Vụ Của Thư Mục

Thư mục `report` chứa tài liệu báo cáo trạng thái dự án.

## Các File Hiện Có

### `Project_status.md`

File này ghi trạng thái dự án sau buổi 2.

Nội dung hiện có:

- Mốc học hiện tại.
- Mục tiêu dự án.
- Cấu trúc thư mục hiện tại.
- Phần đã có mã nguồn.
- Trạng thái dữ liệu hiện tại.
- Quyết định kỹ thuật hiện tại.

### `README_report.md`

File này mô tả chính thư mục `report`.

### `Agent_session_prompt.md`

File này chứa prompt có thể copy sang coding agent trong session mới.

Nội dung file hướng dẫn agent đọc đúng tài liệu ngữ cảnh, đọc transcript đúng buổi học được yêu cầu, đối chiếu code với README theo folder, cập nhật `Project_status.md`, cập nhật README khi lệch trạng thái thật, và không bịa đặt chức năng chưa có trong mã nguồn.

## Cách Hoạt Động Hiện Tại

Tài liệu trong thư mục này dùng để giúp người học hoặc coding agent hiểu trạng thái dự án tại một thời điểm cụ thể.

Các file markdown trong dự án đang dùng mục `Nhật Ký Cập Nhật` để ghi thời gian cập nhật theo giờ Việt Nam.

## Ghi Chú Kỹ Thuật

Tài liệu trong thư mục này không chứa secret và không ghi nội dung `.env`.
