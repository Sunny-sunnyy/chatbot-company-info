# Trạng Thái Dự Án Sau Buổi 2

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo bản ghi trạng thái dự án sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra mã nguồn hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ ghi những phần đã tồn tại trong dự án.
- 2026-07-24 22:06 +07 - Cập nhật trạng thái chunking theo mã nguồn hiện tại trong `ingestion/chunking` và `ingestion/helpers`.

## Mốc Học Hiện Tại

Dự án hiện đang ở trạng thái sau khi hoàn thành buổi 2 của khóa học.

Buổi 1 giới thiệu cấu trúc tổng thể của một chatbot RAG dùng dữ liệu công ty. Luồng tổng quan được trình bày trong buổi học gồm: nạp dữ liệu, chia dữ liệu thành các phần nhỏ, tạo chunk, tạo embedding, lưu vào vector store, truy xuất dữ liệu liên quan khi người dùng hỏi, ghép context vào prompt và gọi LLM để trả lời.

Buổi 2 đã triển khai các phần đầu tiên của luồng đó: cấu hình settings, cấu hình logging, tách file JSON gốc thành các file JSON theo từng bảng, và bắt đầu viết các hàm chunking theo bảng.

## Mục Tiêu Dự Án

Đây là dự án học Python RAG để xây dựng chatbot trả lời thông tin về công ty Nguyen Minh Khang Architects.

Dữ liệu hiện tại mô tả thông tin công ty, hero slides, phong cách nội thất, loại kiến trúc, danh mục dự án, dự án, danh mục tin tức và tin tức.

Dự án hiện đi theo hướng RAG, không phải fine-tuning. Dữ liệu được xử lý thành các phần có thể truy xuất, sau đó dùng làm ngữ cảnh cho LLM khi trả lời câu hỏi.

## Cấu Trúc Thư Mục Hiện Tại

Các thư mục chính hiện có:

- `config`: chứa cấu hình YAML cho ứng dụng và logging.
- `core`: chứa mã dùng chung để đọc settings và cấu hình logging.
- `data`: chứa dữ liệu gốc và dữ liệu đã tách theo bảng.
- `ingestion`: chứa mã nạp dữ liệu và xử lý dữ liệu đầu vào.
- `ingestion/chunking`: chứa mã chunking theo từng bảng dữ liệu.
- `embedding`: hiện chỉ có file Python rỗng.
- `vectorstore`: hiện chỉ có file Python rỗng.
- `retrieval`: hiện chỉ có file Python rỗng.
- `llm`: hiện chỉ có file Python rỗng.
- `logs`: chứa file log của ứng dụng.
- `report`: chứa tài liệu báo cáo trạng thái dự án.
- `tai_lieu`: chứa phiên âm các buổi học.

## Phần Đã Có Mã Nguồn

`core/settings_loader.py` đã có hàm `load_settings()`. Hàm này đọc `config/settings.yaml`, nạp biến môi trường từ `.env`, sau đó ghi đè một số giá trị cấu hình bằng biến môi trường nếu các biến đó tồn tại.

`core/logging_setup.py` đã có hàm `setup_logging()`. Hàm này tạo thư mục `logs` nếu cần, đọc `config/logging.yaml` và áp dụng cấu hình logging bằng `logging.config.dictConfig`.

`ingestion/load_data.py` đã có hàm `load_data()`. Hàm này đọc file JSON gốc trong `data/raw`, lấy object `tables`, bỏ qua các bảng rỗng và ghi từng bảng có dữ liệu ra `data/processed/<ten_bang>.json`.

`ingestion/chunking` hiện có các module chunking cho nhiều bảng dữ liệu đã xử lý:

- `architectureTypes.py`: tạo chunk cho loại kiến trúc từ `architectureTypes.json`.
- `companyInfo.py`: tạo chunk tổng quan, mô tả và thông tin liên hệ công ty từ `companyInfo.json`.
- `heroSlides.py`: tạo chunk cho hero slide từ `heroSlides.json`.
- `interiorStyles.py`: tạo chunk cho phong cách nội thất từ `interiorStyles.json`.
- `newCategories.py`: tạo chunk cho danh mục tin tức từ `newsCategories.json`.
- `news.py`: chuyển HTML tin tức sang text, chia nội dung thành đoạn và tạo chunk từ `news.json`.
- `projectCategories.py`: tạo chunk cho danh mục dự án từ `projectCategories.json`.
- `projects.py`: tạo nhiều loại chunk cho dự án từ `projects.json`, gồm overview, description, style, context, specs và media.

`ingestion/helpers/make_metadata.py` hiện có hàm `make_metadata()` để thêm `chunk_id` UUID và merge metadata. `ingestion/helpers/split_paragraphs.py` hiện có hàm `split_paragraphs()` để chia text dài thành các đoạn nhỏ.

## Trạng Thái Dữ Liệu Hiện Tại

File dữ liệu gốc hiện có:

- `data/raw/database_export_2026-01-14T02-32-14.json`

File gốc có object `tables` gồm 10 bảng:

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

Các file đã được tách trong `data/processed`:

- `architectureTypes.json`
- `companyInfo.json`
- `heroSlides.json`
- `interiorStyles.json`
- `news.json`
- `newsCategories.json`
- `projectCategories.json`
- `projects.json`

## Quyết Định Kỹ Thuật Hiện Tại

Dự án dùng Python và quản lý môi trường bằng `uv`.

File `pyproject.toml` yêu cầu Python `>=3.12`.

Cấu hình chính được đặt trong `config/settings.yaml`.

Cấu hình logging được đặt trong `config/logging.yaml`.

Biến môi trường được nạp bằng `python-dotenv`. Tài liệu này không ghi nội dung `.env`.

Embedding model đang được cấu hình là `intfloat/multilingual-e5-small`.

Vector database đang được cấu hình là Qdrant, tên collection là `nmk_chatbot_collection`, distance là `cosine`, vector size là `384`.

Nhà cung cấp LLM trong settings đang là `openrouter`, tên model đang là `qwen/qwen3.5-9b`, temperature là `0.2`.

Dữ liệu được xử lý theo hướng tách bảng trước, sau đó mới viết chunking riêng cho từng bảng.
