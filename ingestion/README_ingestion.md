# README_ingestion

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra mã nguồn hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 21:24 +07 - Cập nhật mô tả thư mục con `chunking` theo các file hiện có.
- 2026-07-24 21:39 +07 - Chuẩn hóa phần mô tả nhiệm vụ các file mã nguồn.
- 2026-07-25 17:23 +07 - Cập nhật trạng thái `pipeline.py`, danh sách file chunking và thư mục helper theo mã nguồn hiện tại.
- 2026-07-25 18:42 +07 - Cập nhật trạng thái sau buổi 4: `vectorstore` đã có code nhưng pipeline vẫn chưa chạy được end-to-end.

## Nhiệm Vụ Của Thư Mục

Thư mục `ingestion` chứa mã xử lý dữ liệu đầu vào.

Tính tới thời điểm hiện tại, thư mục này có code đọc file JSON gốc, tách dữ liệu theo từng bảng, tạo chunk từ dữ liệu đã xử lý và khai báo pipeline gom chunk để upsert vào vector store.

## File Tài Liệu Trong Thư Mục

### `README_ingestion.md`

File này mô tả nhiệm vụ của thư mục `ingestion`, nhiệm vụ hiện tại của từng file mã nguồn trong thư mục và liên kết tới README chi tiết của thư mục con `chunking`.

## Nhiệm Vụ Các File Mã Nguồn

### `load_data.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import `json`, `logging`, `Path` và `sys`.
- Xác định `PROJECT_ROOT`.
- Thêm project root vào `sys.path` nếu chưa có.
- Import `load_settings` từ `core.settings_loader`.
- Gọi `load_settings()` để lấy cấu hình.
- Tạo logger tên `ingestion`.
- Định nghĩa hàm `load_data()`.
- Nếu chạy trực tiếp file này, gọi `load_data()`.

Hàm `load_data()` hiện đang làm các việc sau:

- Đọc file `data/raw/database_export_2026-01-14T02-32-14.json`.
- Nếu dữ liệu rỗng thì log lỗi và dừng.
- Lấy object `tables`.
- Nếu không có `tables` thì log warning và dừng.
- Duyệt từng cặp `table_name`, `table_data`.
- Nếu `table_data` rỗng thì log warning và bỏ qua.
- Tạo đường dẫn output `data/processed/<table_name>.json`.
- Ghi dữ liệu bảng ra file JSON.
- Dùng `ensure_ascii=False` để giữ tiếng Việt.
- Dùng `indent=4` để file JSON dễ đọc hơn.
- Log thông tin sau khi ghi xong từng bảng.

### `pipeline.py`

File này đã có mã nguồn.

Nội dung hiện tại:

- Import các hàm chunking từ `ingestion/chunking`.
- Import `setup_logging` từ `core.logging_setup`.
- Import `upsert_chunks` từ `vectorstore.upsert`.
- Gọi `setup_logging()`.
- Tạo logger tên `ingestion`.
- Định nghĩa hàm `run_ingestion_pipeline()`.
- Nếu chạy trực tiếp file này, gọi `run_ingestion_pipeline()`.

Hàm `run_ingestion_pipeline()` hiện tạo list `all_chunks`, gọi các hàm chunking cho architecture types, company info, interior styles, news categories, news, project categories và projects, sau đó gọi `upsert_chunks(all_chunks)` nếu có chunk.

Trạng thái hiện tại của file này chưa chạy được nguyên vẹn vì:

- File đang import `ingestion.chunking.InteriorStyles`, nhưng file thật trong thư mục là `ingestion/chunking/interiorStyles.py`.
- File đang import `upsert_chunks` từ `vectorstore.upsert`. `vectorstore/upsert.py` hiện đã có code, nhưng import `vectorstore.*` đang bị ảnh hưởng bởi dependency package tên `vectorstore` trong môi trường `.venv`, và `upsert.py` còn tham chiếu các module local chưa tồn tại là `vectorstore.hybrid_index` và `embedding.sparse_embedder`.

## Thư Mục Con Hiện Có

### `chunking/`

Thư mục con này chứa mã chunking.

Hiện tại trong thư mục `chunking` có các file mã nguồn:

- `architectureTypes.py`
- `companyInfo.py`
- `heroSlides.py`
- `interiorStyles.py`
- `newCategories.py`
- `news.py`
- `projectCategories.py`
- `projects.py`

README chi tiết của thư mục con nằm ở `ingestion/chunking/README_chunking.md`.

### `helpers/`

Thư mục con này chứa helper dùng chung cho chunking.

Hiện tại trong thư mục `helpers` có các file mã nguồn:

- `README_helpers.md`
- `make_metadata.py`
- `split_paragraphs.py`

README chi tiết của thư mục con nằm ở `ingestion/helpers/README_helpers.md`.

## Cách Hoạt Động Hiện Tại

Luồng ingestion đã có ở mức mã nguồn:

1. `load_data.py` đọc file JSON gốc từ `data/raw`.
2. `load_data.py` lấy object `tables`.
3. `load_data.py` bỏ qua bảng rỗng.
4. `load_data.py` ghi từng bảng có dữ liệu sang `data/processed`.
5. Các file trong `ingestion/chunking` đọc dữ liệu từ `data/processed` và trả về list chunk.
6. `pipeline.py` gom chunk từ nhiều hàm chunking.
7. `pipeline.py` gọi `upsert_chunks`, nhưng luồng pipeline chưa chạy được nguyên vẹn trong trạng thái hiện tại vì lỗi import `InteriorStyles` và các vấn đề import/module trong phần `vectorstore`.

## Ghi Chú Kỹ Thuật

File `load_data.py` hiện đang viết trực tiếp tên file JSON gốc trong mã nguồn.

Logger đang dùng tên `ingestion`.

Dữ liệu được đọc và ghi bằng UTF-8.

Thư mục `__pycache__` có thể xuất hiện khi chạy Python, nhưng đó là file sinh tự động và không thuộc phạm vi tài liệu này.
