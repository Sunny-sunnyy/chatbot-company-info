# Chatbot thông tin công ty

## Nhật Ký Cập Nhật

- 2026-07-24 21:39 +07 - Bổ sung mô tả nhiệm vụ file mã nguồn ở thư mục gốc.
- 2026-07-25 17:34 +07 - Bổ sung trạng thái CodeGraph, `.gitignore` và các file tài liệu/cấu hình ở thư mục gốc.
- 2026-07-25 20:22 +07 - Bổ sung chuẩn mô tả vai trò file mã nguồn; `chat.py` hiện vẫn rỗng và chưa có luồng xử lý.

## Nhiệm Vụ Thư Mục Gốc

Thư mục gốc chứa cấu hình project Python, file khóa dependency, tài liệu tổng quan, tài liệu tham khảo CodeGraph và entrypoint cấp cao của dự án.

CodeGraph đã được init local cho repo này bằng CLI `1.5.0`. Thư mục `.codegraph/` là index SQLite local, được ignore trong `.gitignore` và không nên commit.

Theo tài liệu CodeGraph, auto-sync được bật mặc định sau khi init: CodeGraph watch project và cập nhật graph khi file thay đổi. Nếu cần kiểm tra thủ công, dùng `codegraph status .`; nếu nghi ngờ index lệch, dùng `codegraph sync`.

## Các File Hiện Có Ở Thư Mục Gốc

### `README.md`

File này mô tả nhiệm vụ thư mục gốc và trạng thái hiện tại của các file chính ở thư mục gốc.

### `.gitignore`

File này khai báo các file/thư mục không đưa vào Git, gồm Python cache, virtual environment, secret `.env`, test cache, dữ liệu local, log, transcript và `.codegraph/`.

### `README_codegraph.md`

File này là tài liệu tham khảo về CodeGraph.

Trong dự án hiện tại, file này được dùng để hiểu cách cài đặt, init, auto-sync và sử dụng CodeGraph cho coding agent. Đây không phải mã nguồn của chatbot.

### `brainstorming.md`

File này tồn tại ở thư mục gốc và đang có thay đổi trong Git status trước session cập nhật CodeGraph. Nội dung file không thuộc phần triển khai RAG chính được kiểm tra trong lần cập nhật này.

### `pyproject.toml`

File này khai báo project Python `llm-rag`, yêu cầu Python `>=3.12`, dependency runtime và dependency dev.

### `uv.lock`

File này là lockfile dependency do `uv` quản lý.

## Nhiệm Vụ Các File Mã Nguồn

### `chat.py`

File này hiện đang rỗng.

Tính tới thời điểm cập nhật này, file chưa có nhiệm vụ xử lý cụ thể trong mã nguồn.

Vì file chưa có code, README không gán vai trò xử lý hoặc mô tả luồng chat chưa tồn tại.
