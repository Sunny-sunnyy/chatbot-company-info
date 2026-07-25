# README_report

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 20:31 +07 - Bổ sung mô tả file `Agent_session_prompt.md`.
- 2026-07-25 17:23 +07 - Cập nhật mô tả `Project_status.md` theo snapshot hiện tại của repo.
- 2026-07-25 17:37 +07 - Cập nhật mô tả `Agent_session_prompt.md` sau khi bổ sung hướng dẫn sử dụng CodeGraph cho coding agent.
- 2026-07-25 18:42 +07 - Cập nhật mô tả `Project_status.md` sau khi audit trạng thái dự án theo buổi 4.
- 2026-07-25 20:22 +07 - Cập nhật mô tả `Project_status.md` và `Agent_session_prompt.md` sau khi bổ sung chuẩn giải thích vai trò file mã nguồn trong README.

## Nhiệm Vụ Của Thư Mục

Thư mục `report` chứa tài liệu báo cáo trạng thái dự án và prompt hướng dẫn coding agent khi tiếp tục làm việc với repo.

## Các File Hiện Có

### `Project_status.md`

File này ghi snapshot mới nhất của dự án tại thời điểm kiểm tra.

Nội dung hiện có:

- Mốc học hiện tại.
- Mục tiêu dự án.
- Cấu trúc thư mục hiện tại.
- Phần đã có mã nguồn.
- Phần chưa được phát triển.
- Trạng thái chạy hiện tại của pipeline và vector store.
- Trạng thái dữ liệu hiện tại.
- Quyết định kỹ thuật hiện tại.
- Chuẩn README hiện tại cho các folder có file Python thật.

### `README_report.md`

File này mô tả chính thư mục `report` và trạng thái hiện tại của từng file trong thư mục.

### `Agent_session_prompt.md`

File này chứa prompt có thể copy sang coding agent trong session mới.

Nội dung file hướng dẫn agent đọc đúng tài liệu ngữ cảnh, đọc transcript đúng buổi học được yêu cầu, đối chiếu code với README theo folder, cập nhật `Project_status.md`, cập nhật README khi lệch trạng thái thật, không bịa đặt chức năng chưa có trong mã nguồn, giải thích vai trò/hàm/luồng chính của file mã nguồn đã có code, ghi rõ file rỗng là chưa phát triển, và sử dụng CodeGraph đúng cách khi cần hiểu flow hoặc quan hệ symbol trong code.

## Cách Hoạt Động Hiện Tại

Tài liệu trong thư mục này dùng để giúp người học hoặc coding agent hiểu trạng thái dự án tại một thời điểm cụ thể.

Các file markdown trong dự án đang dùng mục `Nhật Ký Cập Nhật` để ghi thời gian cập nhật theo giờ Việt Nam.

## Ghi Chú Kỹ Thuật

Tài liệu trong thư mục này không chứa secret và không ghi nội dung `.env`.
