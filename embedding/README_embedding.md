# README_embedding

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Rút gọn nội dung vì các file trong thư mục hiện chưa có dòng mã nguồn nào.
- 2026-07-24 21:24 +07 - Bổ sung mô tả trạng thái và nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-24 21:39 +07 - Chuẩn hóa phần mô tả nhiệm vụ các file mã nguồn.
- 2026-07-25 17:23 +07 - Cập nhật theo mã nguồn hiện tại: `embedder.py` và `batch_embed.py` đã có code, các file cũ `embed_texts.py` và `batch_embed_texts.py` không còn trong thư mục.
- 2026-07-25 18:42 +07 - Đối chiếu với nội dung buổi 4 và xác nhận mã embedding hiện có khớp phần load model, encode text và batch embedding.

## Nhiệm Vụ Của Thư Mục

Thư mục `embedding` chứa mã tạo vector embedding từ text.

Tính tới thời điểm hiện tại, thư mục này có code load model `SentenceTransformer`, tạo embedding cho danh sách text và xử lý embedding theo batch.

Nội dung này khớp với phần embedding trong `tai_lieu/4.txt`: load model một lần, dùng device từ settings, encode text thành vector và xử lý danh sách text theo batch.

## File Tài Liệu Trong Thư Mục

### `README_embedding.md`

File này mô tả trạng thái hiện tại của thư mục `embedding` và nhiệm vụ hiện tại của từng file mã nguồn trong thư mục.

## Nhiệm Vụ Các File Mã Nguồn

### `embedder.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `logging` và `SentenceTransformer`.
- Import `load_settings` từ `core.settings_loader`.
- Đọc cấu hình `embedding` từ settings.
- Lấy tên model từ key `embedding.model`.
- Dùng biến module `_model` để cache model sau lần load đầu tiên.
- Định nghĩa hàm `get_model()`.
- Định nghĩa hàm `embed_texts(texts: list[str])`.

Hàm `get_model()` hiện load `SentenceTransformer` bằng model trong settings và device trong `embedding.device`, mặc định là `cpu` nếu không có cấu hình device.

Hàm `embed_texts()` hiện trả về list rỗng nếu input rỗng. Với input có text, hàm gọi model encode với `normalize_embeddings=True`, `convert_to_tensor=False`, chuyển kết quả sang list và trả về `list[list[float]]`.

### `batch_embed.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `logging`.
- Import `load_settings` từ `core.settings_loader`.
- Import `embed_texts` từ `embedding.embedder`.
- Đọc `embedding.batch_size` từ settings, mặc định là `32` nếu không có cấu hình.
- Định nghĩa hàm `batch_embed_texts(texts: list[str])`.

Hàm `batch_embed_texts()` hiện trả về list rỗng nếu input rỗng. Với input có text, hàm chia danh sách text thành các batch theo `BATCH_SIZE`, gọi `embed_texts()` cho từng batch, gộp toàn bộ embedding vào `all_embeddings` và trả về kết quả.
