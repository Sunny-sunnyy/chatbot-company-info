# README_chunking

## Nhật Ký Cập Nhật

- 2026-08-04 16:03 +07 - Cập nhật `companyInfo.py`: chunk `contact_info` hiện thêm câu mở đầu `Thông tin liên hệ của <tên công ty>` trước Hotline/Email/Địa chỉ để query tự nhiên về liên hệ match trực tiếp hơn.
- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra mã nguồn hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 21:18 +07 - Cập nhật trạng thái sau khi thêm `heroSlides.py` và đối chiếu các file chunking hiện có.
- 2026-07-24 21:24 +07 - Bổ sung mô tả `interiorStyles.py`, `news.py` và nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-24 21:39 +07 - Chuẩn hóa phần mô tả nhiệm vụ các file mã nguồn.
- 2026-07-24 22:06 +07 - Cập nhật theo trạng thái hiện tại: bổ sung `newCategories.py`, `projectCategories.py`, `projects.py` và ghi nhận helper metadata/split đoạn văn.
- 2026-07-25 20:22 +07 - Bổ sung giải thích vai trò và luồng hoạt động của từng file chunking.
- 2026-07-29 20:56 +07 - Cập nhật trạng thái sau `tai_lieu/p2/2.txt`: xoá mô tả `heroSlides.py`, ghi nhận pipeline không còn dùng hero slides và bổ sung trạng thái chunk count hiện tại.

## Nhiệm Vụ Của Thư Mục

Thư mục `ingestion/chunking` chứa mã chuyển dữ liệu đã xử lý thành chunk.

Tính tới thời điểm hiện tại, thư mục này có mã chunking cho các file processed JSON sau:

- `architectureTypes.json`
- `companyInfo.json`
- `interiorStyles.json`
- `newsCategories.json`
- `news.json`
- `projectCategories.json`
- `projects.json`

File `data/processed/heroSlides.json` vẫn tồn tại trong dữ liệu processed, nhưng thư mục này không còn file `heroSlides.py` và pipeline không còn tạo chunk từ hero slides.

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

Vai trò và luồng hoạt động:

- `architectureTypes.py` chịu trách nhiệm chuyển dữ liệu loại kiến trúc thành chunk dạng định nghĩa.
- `chunk_architecture_types()` đọc `architectureTypes.json`, chuẩn hóa dữ liệu dictionary thành list nếu cần, kiểm tra từng item rồi lấy `id`, `slug`, `name` và `description`.
- Hàm chỉ tạo chunk khi có cả `name` và `description`.
- Metadata được tạo qua `make_metadata(...)` với `chunk_type="definition"` và `priority=3`.
- Output là `list[dict]`, mỗi phần tử có `text` và `metadata`.
- Trạng thái dữ liệu hiện tại: với `data/processed/architectureTypes.json` đang có trong repo, hàm hiện tạo 0 chunk vì các bản ghi thiếu `description` theo điều kiện trong code.

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

Vai trò và luồng hoạt động:

- `companyInfo.py` chịu trách nhiệm tạo các chunk trả lời câu hỏi tổng quan về công ty và thông tin liên hệ.
- `chunk_company_info()` đọc `companyInfo.json`, chuẩn hóa dữ liệu thành list, rồi duyệt từng bản ghi công ty.
- File tách một bản ghi công ty thành nhiều nhóm chunk có độ ưu tiên khác nhau: `overview`, `description` và `contact_info`.
- Chunk `contact_info` hiện bắt đầu bằng câu `Thông tin liên hệ của <tên công ty>:` rồi mới liệt kê Hotline, Email, Địa chỉ, Giờ làm việc, Website và Mạng xã hội. Cách viết này giúp các query tự nhiên như `thông tin liên hệ` match trực tiếp với chunk liên hệ thay vì chỉ dựa vào các từ khóa `Hotline` hoặc `Email`.
- Phần mạng xã hội được chuyển từ dictionary sang text dạng `key: value` trước khi đưa vào chunk liên hệ.
- Output là list chunk đã có metadata chung `type="company_info"` và metadata riêng theo từng `chunk_type`.

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

Vai trò và luồng hoạt động:

- `interiorStyles.py` chịu trách nhiệm chuyển dữ liệu phong cách nội thất thành chunk dạng định nghĩa.
- `chunk_interior_styles()` đọc `interiorStyles.json`, chuẩn hóa dữ liệu thành list, rồi lấy `id`, `slug`, `name` và `imageUrl`.
- Hàm hiện chỉ tạo chunk khi có cả `name` và `imageUrl`.
- Metadata được tạo qua `make_metadata(...)` với `chunk_type="definition"` và `priority=3`.
- Output là list chunk về phong cách nội thất, trong đó text hiện mô tả tên phong cách và URL hình ảnh minh họa.
- Trạng thái dữ liệu hiện tại: hàm tạo 10 chunk từ `interiorStyles.json`.

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

Vai trò và luồng hoạt động:

- `news.py` chịu trách nhiệm chuyển bài viết tin tức từ HTML/raw JSON thành các chunk text có thể embedding.
- `html_to_text(html)` dùng `BeautifulSoup` để bỏ tag HTML và giữ lại text thuần.
- `chunk_news()` đọc `news.json`, lấy title, slug, excerpt và content, chuyển content HTML sang text rồi gọi `split_paragraphs(...)`.
- File tạo chunk `overview` từ title và excerpt nếu có, sau đó tạo các chunk `full_content` cho từng đoạn nội dung.
- Output là list chunk tin tức; mỗi chunk nội dung có metadata từ `make_metadata(...)`, còn `part_index` hiện được đặt ở cấp chunk dictionary cho full content.
- Trạng thái dữ liệu hiện tại: hàm tạo 163 chunk từ `news.json`.

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

Vai trò và luồng hoạt động:

- `newCategories.py` chịu trách nhiệm tạo chunk định nghĩa cho danh mục tin tức.
- `chunk_news_categories()` đọc `newsCategories.json`, chuẩn hóa dữ liệu thành list, bỏ qua category không phải dictionary hoặc thiếu `name`.
- Text chunk mô tả tên danh mục và mục đích phân loại bài viết theo danh mục đó.
- Metadata được tạo qua `make_metadata(...)` với `type="news_category"`, `chunk_type="definition"` và `priority=3`.
- Output là list chunk danh mục tin tức. Tên file hiện là `newCategories.py`, khác một chữ so với tên dữ liệu `newsCategories.json`.
- Trạng thái dữ liệu hiện tại: hàm tạo 4 chunk từ `newsCategories.json`.

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

Vai trò và luồng hoạt động:

- `projectCategories.py` chịu trách nhiệm tạo chunk định nghĩa cho danh mục dự án.
- `chunk_project_categories()` đọc `projectCategories.json`, chuẩn hóa dữ liệu thành list, bỏ qua category không phải dictionary hoặc thiếu `name`.
- Text chunk mô tả tên danh mục và vai trò phân loại các dự án liên quan.
- Metadata được tạo qua `make_metadata(...)` với `type="project_category"`, `chunk_type="definition"` và `priority=3`.
- Output là list chunk danh mục dự án.
- Trạng thái dữ liệu hiện tại: hàm tạo 12 chunk từ `projectCategories.json`.

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

Vai trò và luồng hoạt động:

- `projects.py` chịu trách nhiệm chuyển mỗi dự án thành nhiều chunk nhỏ theo các góc truy vấn khác nhau.
- `chunk_projects()` đọc `projects.json`, chuẩn hóa dữ liệu thành list, rồi lấy các field chính như tên dự án, slug, mô tả, chủ đầu tư, địa điểm, diện tích, ngày hoàn thành, danh mục, phong cách nội thất và ảnh đại diện.
- File tạo chunk `overview` cho tên dự án, chunk `description` từ từng đoạn mô tả sau `split_paragraphs(...)`, chunk `style` cho danh mục/phong cách, chunk `context` cho địa điểm/chủ đầu tư, chunk `specs` cho diện tích/thời gian và chunk `media` cho ảnh minh họa.
- Metadata được tạo qua `make_metadata(...)`, giúp mỗi chunk có `chunk_id`, `chunk_type`, `priority` và các field bổ sung phù hợp.
- Output là list chunk dự án, thường nhiều chunk trên một project để retrieval có thể bắt được nhiều kiểu câu hỏi.
- Trạng thái dữ liệu hiện tại: hàm tạo 258 chunk từ `projects.json`.

### `__init__.py`

File này hiện đang rỗng.

File đánh dấu `ingestion/chunking` là Python package.

## Cách Hoạt Động Hiện Tại

Các file trong thư mục này hiện đọc dữ liệu từ:

```text
data/processed/architectureTypes.json
data/processed/companyInfo.json
data/processed/interiorStyles.json
data/processed/newsCategories.json
data/processed/news.json
data/processed/projectCategories.json
data/processed/projects.json
```

Kết quả trả về của hàm là list các dictionary. Mỗi dictionary có hai key:

- `text`
- `metadata`

Kiểm tra hiện tại bằng cách gọi trực tiếp các hàm chunking, chưa upsert Qdrant, tạo tổng cộng 450 chunks.

## Ghi Chú Kỹ Thuật

Nhiều file chunking đang dùng `ingestion.helpers.make_metadata`. Helper này hiện tồn tại tại `ingestion/helpers/make_metadata.py` và có nhiệm vụ merge metadata gốc với metadata bổ sung, đồng thời thêm `chunk_id` dạng UUID.

`news.py` và `projects.py` đang dùng `ingestion.helpers.split_paragraphs`. Helper này hiện tồn tại tại `ingestion/helpers/split_paragraphs.py` và có nhiệm vụ chia text dài thành các đoạn nhỏ theo giới hạn độ dài.

Trong dữ liệu processed hiện tại, nhiều bản ghi `architectureTypes.json` có `description` là `null`. Mã hiện tại chỉ tạo chunk khi có cả `name` và `description`, nên `chunk_architecture_types()` hiện trả về 0 chunk.

Timestamp `created_at` trong metadata được tạo bằng `datetime.utcnow().isoformat()`.

`heroSlides.py` đã bị xoá khỏi thư mục này sau `tai_lieu/p2/2.txt`. Lý do theo bài học là hero slides có thể trộn nội dung trang chủ, dự án và tin tức, làm nhiễu retrieval nếu đưa thẳng vào vector store.

Các file bytecode trong `ingestion/chunking/__pycache__` là file sinh tự động khi chạy Python, không phải mã nguồn cần bảo trì trực tiếp.
