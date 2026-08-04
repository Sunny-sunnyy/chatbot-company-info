# README_ingestion

## Nhật Ký Cập Nhật

- 2026-08-04 19:44 +07 - Cập nhật sau refactor layout: thư mục `ingestion` đã nằm trong `backend/`; lệnh chạy pipeline từ `backend/` bằng `uv run python -m ingestion.pipeline`.
- 2026-08-04 16:12 +07 - Chạy lại pipeline sau khi cập nhật chunk liên hệ trong `companyInfo.py`; collection Qdrant local được rebuild sạch về 450 hybrid points và query `thông tin liên hệ` truy xuất đúng `company_info/contact_info` ở top 1.
- 2026-08-01 20:28 +07 - Cập nhật trạng thái sau khi kiểm tra log chạy thật: pipeline hybrid đã chạy thành công, collection `nmk_chatbot_collection` đã có schema hybrid và chứa 450 points; lỗi `Not existing vector name error: sparse` chỉ xảy ra ở lần chạy đầu với collection cũ dense-only.
- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra mã nguồn hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 21:24 +07 - Cập nhật mô tả thư mục con `chunking` theo các file hiện có.
- 2026-07-24 21:39 +07 - Chuẩn hóa phần mô tả nhiệm vụ các file mã nguồn.
- 2026-07-25 17:23 +07 - Cập nhật trạng thái `pipeline.py`, danh sách file chunking và thư mục helper theo mã nguồn hiện tại.
- 2026-07-25 18:42 +07 - Cập nhật trạng thái sau buổi 4: `vectorstore` đã có code nhưng pipeline vẫn chưa chạy được end-to-end.
- 2026-07-25 20:22 +07 - Bổ sung giải thích vai trò và luồng hoạt động của các file mã nguồn trong thư mục `ingestion`.
- 2026-07-26 12:23 +07 - Cập nhật trạng thái sau buổi 5: pipeline đã chạy thành công bằng `uv run python -m ingestion.pipeline` và upsert 450 chunks vào Qdrant.
- 2026-07-29 20:56 +07 - Cập nhật trạng thái sau `tai_lieu/p2/2.txt`: pipeline không còn gọi hero slides, sửa import `interiorStyles.py` và kiểm tra số chunk hiện tại trước upsert.
- 2026-08-01 16:51 +07 - Cập nhật trạng thái sau khi đọc `tai_lieu/p2/10.txt`: `pipeline.py` vẫn gom chunk như cũ nhưng `upsert_chunks()` hiện chuyển sang build/upsert hybrid points.
- 2026-08-01 17:58 +07 - Cập nhật trạng thái sau p2 hoàn chỉnh: pipeline đi qua `upsert_chunks()` hybrid; lỗi Qdrant `Not existing vector name error: sparse` là do collection cũ chưa có sparse vector.

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

Vai trò và luồng hoạt động:

- `load_data.py` chịu trách nhiệm biến file export gốc thành các file JSON đã tách theo bảng để các bước chunking đọc được dễ hơn.
- File thêm `PROJECT_ROOT` vào `sys.path` khi chạy trực tiếp, giúp import được `core.settings_loader` từ project root.
- `load_data()` đọc file gốc trong `settings["data"]["raw_dir"]`, lấy object `tables`, bỏ qua bảng rỗng và ghi từng bảng có dữ liệu sang `settings["data"]["processed_dir"]`.
- Input chính là `data/raw/database_export_2026-01-14T02-32-14.json`.
- Output chính là các file JSON trong `data/processed`, ví dụ `companyInfo.json`, `projects.json`, `news.json`.
- File này là bước chuẩn bị dữ liệu trước khi các module trong `ingestion/chunking` tạo chunk.

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

Hàm `run_ingestion_pipeline()` hiện tạo list `all_chunks`, gọi các hàm chunking cho architecture types, company info, interior styles, news categories, news, project categories và projects, sau đó gọi `upsert_chunks(all_chunks)` nếu có chunk. Pipeline hiện không còn gọi `chunk_hero_slides()`.

Lệnh chạy file này từ `backend/`:

```bash
uv run python -m ingestion.pipeline
```

Log chạy thực tế sau buổi 5 ghi nhận pipeline đã upsert 450 chunks vào vector store bằng luồng dense-only thời điểm đó. Sau cập nhật `p2/10`, `pipeline.py` vẫn gom chunk như cũ nhưng `vectorstore/upsert.py` đã chuyển sang fit `SparseEmbedder` và upsert hybrid points dense+sparse.

Vai trò và luồng hoạt động:

- `pipeline.py` chịu trách nhiệm điều phối luồng ingestion từ các hàm chunking sang bước upsert vào vector store.
- `setup_logging()` được gọi ở cấp module để kích hoạt cấu hình logging trước khi pipeline chạy.
- `run_ingestion_pipeline()` tạo `all_chunks`, gọi lần lượt các hàm chunking cho architecture types, company info, interior styles, news categories, news, project categories và projects, rồi gom toàn bộ chunk vào một list.
- File này đã bỏ import và bỏ gọi chunking hero slides.
- Nếu `all_chunks` rỗng, pipeline log warning và dừng.
- Nếu có chunk, pipeline gọi `upsert_chunks(all_chunks)` để chuyển dữ liệu sang vector store.
- Trạng thái kiểm tra hiện tại: `ingestion.pipeline` import được bằng `uv run`. Lệnh gọi trực tiếp các hàm chunking trước đó tạo tổng cộng 450 chunks trước khi upsert. Sau cập nhật `p2/10`, pipeline tạo/upsert hybrid points qua `vectorstore/upsert.py`; để chạy thật cần Qdrant collection đúng schema hybrid.

### `__init__.py`

File này hiện đang rỗng.

File đánh dấu `ingestion` là Python package.

## Thư Mục Con Hiện Có

### `chunking/`

Thư mục con này chứa mã chunking.

Hiện tại trong thư mục `chunking` có các file mã nguồn:

- `architectureTypes.py`
- `companyInfo.py`
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
- `__init__.py`
- `make_metadata.py`
- `split_paragraphs.py`

README chi tiết của thư mục con nằm ở `ingestion/helpers/README_helpers.md`.

## Cách Hoạt Động Hiện Tại

Luồng ingestion đã có ở mức mã nguồn:

1. `load_data.py` đọc file JSON gốc từ `data/raw`.
2. `load_data.py` lấy object `tables`.
3. `load_data.py` bỏ qua bảng rỗng.
4. `load_data.py` ghi từng bảng có dữ liệu sang `data/processed`.
5. Các file trong `ingestion/chunking` đọc dữ liệu từ `data/processed` và trả về list chunk. Sau `p2/2`, `heroSlides.json` không còn có module chunking tương ứng và không còn được đưa vào pipeline.
6. `pipeline.py` gom chunk từ nhiều hàm chunking.
7. `pipeline.py` gọi `upsert_chunks`.
8. `vectorstore/upsert.py` đảm bảo collection Qdrant tồn tại, fit `SparseEmbedder`, build hybrid point có named vector `dense` và `sparse`, rồi upsert point vào Qdrant.

Sau buổi 5, luồng này đã chạy thành công với Qdrant local. Log chạy thực tế ghi nhận:

- Collection `nmk_chatbot_collection` được tạo thành công.
- Embedding model `intfloat/multilingual-e5-small` được load.
- 450 Qdrant points được build.
- 450 points được upsert vào collection.
- 450 chunks được upsert vào vector store.

Trong lúc chạy có warning `Empty text provided to split_paragraphs` cho một số bản ghi thiếu text để chia đoạn. Warning này không làm pipeline dừng.

Sau cập nhật `p2/10`, kiểm tra tĩnh hiện tại đã pass:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile core/startup.py vectorstore/qdrant.py vectorstore/upsert.py vectorstore/hybrid_index.py ingestion/pipeline.py retrieval/hybrid_retriever.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import importlib; importlib.import_module('ingestion.pipeline'); print('ingestion.pipeline import ok')"
```

Người dùng đã chạy pipeline hybrid và upsert thành công theo log thực tế: collection `nmk_chatbot_collection` được tạo lại với named vector `dense` và sparse vector `sparse`, 450 hybrid points được build và upsert, pipeline log `Upserted 450 chunks into the vector store`. Lỗi `Not existing vector name error: sparse` chỉ xảy ra ở lần chạy đầu khi collection cũ dense-only chưa được xoá; sau khi xoá collection cũ, luồng chạy thành công.

Sau cập nhật `p2/2`, kiểm tra không upsert bằng cách gọi trực tiếp các hàm chunking cho kết quả:

- `architectureTypes`: 0 chunk
- `companyInfo`: 3 chunks
- `interiorStyles`: 10 chunks
- `newsCategories`: 4 chunks
- `news`: 163 chunks
- `projectCategories`: 12 chunks
- `projects`: 258 chunks
- Tổng cộng: 450 chunks

Trong kiểm tra này vẫn có warning `Empty text provided to split_paragraphs`, nhưng các hàm chunking vẫn trả kết quả.

## Ghi Chú Kỹ Thuật

File `load_data.py` hiện đang viết trực tiếp tên file JSON gốc trong mã nguồn.

Logger đang dùng tên `ingestion`.

Dữ liệu được đọc và ghi bằng UTF-8.

Thư mục `__pycache__` có thể xuất hiện khi chạy Python, nhưng đó là file sinh tự động và không thuộc phạm vi tài liệu này.
