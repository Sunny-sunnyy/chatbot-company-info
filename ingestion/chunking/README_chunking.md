# README_chunking

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra mã nguồn hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 21:18 +07 - Cập nhật trạng thái sau khi thêm `heroSlides.py` và đối chiếu các file chunking hiện có.
- 2026-07-24 21:24 +07 - Bổ sung mô tả `interiorStyles.py`, `news.py` và nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-24 21:39 +07 - Chuẩn hóa phần mô tả nhiệm vụ các file mã nguồn.
- 2026-07-24 22:06 +07 - Cập nhật theo trạng thái hiện tại: bổ sung `newCategories.py`, `projectCategories.py`, `projects.py` và ghi nhận helper metadata/split đoạn văn.

## Nhiệm Vụ Của Thư Mục

Thư mục `ingestion/chunking` chứa mã chuyển dữ liệu đã xử lý thành chunk.

Tính tới thời điểm hiện tại, thư mục này có mã chunking cho các file processed JSON sau:

- `architectureTypes.json`
- `companyInfo.json`
- `heroSlides.json`
- `interiorStyles.json`
- `newsCategories.json`
- `news.json`
- `projectCategories.json`
- `projects.json`

Các file chunking dùng chung cấu hình từ `core.settings_loader.load_settings()` và logger tên `ingestion`.

## File Tài Liệu Trong Thư Mục

### `README_chunking.md`

File này mô tả nhiệm vụ của thư mục `ingestion/chunking`, trạng thái các file chunking hiện có và cách các file này đọc dữ liệu từ `data/processed`.

## Nhiệm Vụ Các File Mã Nguồn

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

### `companyInfo.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Đọc `data/processed/companyInfo.json`.
- Kiểm tra file tồn tại.
- Đọc JSON bằng UTF-8.
- Chuyển dữ liệu dạng dictionary thành list nếu cần.
- Kiểm tra dữ liệu có phải list không.
- Duyệt từng bản ghi công ty.
- Tạo chunk tổng quan từ tên công ty và slogan.
- Tạo chunk mô tả từ mô tả công ty và tổng số dự án nếu có.
- Tạo chunk thông tin liên hệ từ hotline, email, địa chỉ, giờ làm việc, website và mạng xã hội nếu có.
- Dùng `make_metadata(...)` để tạo metadata cho từng chunk.

### `heroSlides.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Đọc `data/processed/heroSlides.json`.
- Kiểm tra file tồn tại.
- Đọc JSON bằng UTF-8.
- Chuyển dữ liệu dạng dictionary thành list nếu cần.
- Kiểm tra dữ liệu có phải list không.
- Bỏ qua slide không phải dictionary.
- Bỏ qua slide thiếu `title`, `subtitle` hoặc `description`.
- Tạo text tiếng Việt từ `title`, `subtitle` và `description`.
- Tạo metadata trực tiếp gồm `type`, `source`, `slide_index`, `title`, `subtitle`, `description`, `image_url`.
- Trả về danh sách chunk hợp lệ.

### `interiorStyles.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Đọc `data/processed/interiorStyles.json`.
- Kiểm tra file tồn tại.
- Đọc JSON bằng UTF-8.
- Chuyển dữ liệu dạng dictionary thành list nếu cần.
- Kiểm tra dữ liệu có phải list không.
- Bỏ qua item không phải dictionary.
- Lấy các field `id`, `slug`, `name`, `imageUrl`.
- Tạo `base_metadata`.
- Nếu có cả `name` và `imageUrl`, tạo text tiếng Việt.
- Gọi `make_metadata(...)` để tạo metadata cuối cùng.
- Trả về danh sách chunk hợp lệ.

### `news.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Đọc `data/processed/news.json`.
- Kiểm tra file tồn tại.
- Đọc JSON bằng UTF-8.
- Chuyển dữ liệu dạng dictionary thành list nếu cần.
- Kiểm tra dữ liệu có phải list không.
- Bỏ qua item không phải dictionary.
- Dùng `BeautifulSoup` trong hàm `html_to_text()` để chuyển nội dung HTML sang text thuần.
- Dùng `split_paragraphs(...)` để chia nội dung tin tức thành các đoạn nhỏ.
- Lấy các field `id`, `title`, `slug`, `excerpt`, `content`.
- Tạo `base_metadata`.
- Tạo chunk tổng quan từ `title` và `excerpt` nếu có.
- Tạo chunk nội dung đầy đủ từ từng đoạn nội dung đã chia.
- Gọi `make_metadata(...)` để tạo metadata cho từng chunk.
- Trả về danh sách chunk hợp lệ.

### `newCategories.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Đọc `data/processed/newsCategories.json`.
- Kiểm tra file tồn tại.
- Đọc JSON bằng UTF-8.
- Chuyển dữ liệu dạng dictionary thành list nếu cần.
- Kiểm tra dữ liệu có phải list không.
- Bỏ qua category không phải dictionary.
- Lấy các field `id`, `name`, `slug`.
- Bỏ qua category thiếu `name`.
- Tạo `base_metadata` với `type` là `news_category`.
- Tạo text mô tả danh mục tin tức.
- Gọi `make_metadata(...)` để tạo metadata cuối cùng.
- Trả về danh sách chunk hợp lệ.

Tên file hiện tại là `newCategories.py`, còn dữ liệu đầu vào là `newsCategories.json`.

### `projectCategories.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Đọc `data/processed/projectCategories.json`.
- Kiểm tra file tồn tại.
- Đọc JSON bằng UTF-8.
- Chuyển dữ liệu dạng dictionary thành list nếu cần.
- Kiểm tra dữ liệu có phải list không.
- Bỏ qua category không phải dictionary.
- Lấy các field `id`, `name`, `slug`.
- Bỏ qua category thiếu `name`.
- Tạo `base_metadata` với `type` là `project_category`.
- Tạo text mô tả danh mục dự án.
- Gọi `make_metadata(...)` để tạo metadata cuối cùng.
- Trả về danh sách chunk hợp lệ.

### `projects.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Đọc `data/processed/projects.json`.
- Kiểm tra file tồn tại.
- Đọc JSON bằng UTF-8.
- Chuyển dữ liệu dạng dictionary thành list nếu cần.
- Kiểm tra dữ liệu có phải list không.
- Bỏ qua project không phải dictionary.
- Lấy các field chính như `id`, `title`, `slug`, `investor`, `location`, `description`, `thumbnailUrl`, `completedDate`, `area`, `category`, `interiorStyle`.
- Tạo `base_metadata` với `type` là `project`.
- Tạo chunk overview từ tên dự án.
- Dùng `split_paragraphs(...)` để chia mô tả dự án và tạo các chunk description.
- Tạo chunk style từ danh mục dự án và phong cách nội thất.
- Tạo chunk context từ địa điểm và chủ đầu tư.
- Tạo chunk specs từ diện tích và thời gian hoàn thành.
- Tạo chunk media từ ảnh minh họa.
- Gọi `make_metadata(...)` để tạo metadata cho từng chunk.
- Trả về danh sách chunk hợp lệ.

## Cách Hoạt Động Hiện Tại

Các file trong thư mục này hiện đọc dữ liệu từ:

```text
data/processed/architectureTypes.json
data/processed/companyInfo.json
data/processed/heroSlides.json
data/processed/interiorStyles.json
data/processed/newsCategories.json
data/processed/news.json
data/processed/projectCategories.json
data/processed/projects.json
```

Kết quả trả về của hàm là list các dictionary. Mỗi dictionary có hai key:

- `text`
- `metadata`

## Ghi Chú Kỹ Thuật

Nhiều file chunking đang dùng `ingestion.helpers.make_metadata`. Helper này hiện tồn tại tại `ingestion/helpers/make_metadata.py` và có nhiệm vụ merge metadata gốc với metadata bổ sung, đồng thời thêm `chunk_id` dạng UUID.

`news.py` và `projects.py` đang dùng `ingestion.helpers.split_paragraphs`. Helper này hiện tồn tại tại `ingestion/helpers/split_paragraphs.py` và có nhiệm vụ chia text dài thành các đoạn nhỏ theo giới hạn độ dài.

Trong dữ liệu mẫu đã kiểm tra, nhiều bản ghi `architectureTypes.json` có `description` là `null`. Mã hiện tại chỉ tạo chunk khi có cả `name` và `description`.

Timestamp `created_at` trong metadata được tạo bằng `datetime.utcnow().isoformat()`.

`heroSlides.py` không dùng `make_metadata`; file này tạo metadata trực tiếp theo ảnh tham khảo trong `tai_lieu/anh1.png`, `tai_lieu/anh2.png` và `tai_lieu/anh3.png`.

Các file bytecode trong `ingestion/chunking/__pycache__` là file sinh tự động khi chạy Python, không phải mã nguồn cần bảo trì trực tiếp.
