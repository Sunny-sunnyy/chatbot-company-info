# README_core

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra mã nguồn hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 21:24 +07 - Bổ sung mô tả nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-24 21:39 +07 - Chuẩn hóa phần mô tả nhiệm vụ các file mã nguồn.
- 2026-07-25 20:22 +07 - Bổ sung giải thích vai trò và luồng hoạt động của từng file mã nguồn trong thư mục.

## Nhiệm Vụ Của Thư Mục

Thư mục `core` chứa mã dùng chung cho dự án.

Tính tới thời điểm hiện tại, thư mục này có hai nhiệm vụ:

- Đọc cấu hình từ YAML và biến môi trường.
- Thiết lập logging cho toàn bộ ứng dụng.

## File Tài Liệu Trong Thư Mục

### `README_core.md`

File này mô tả nhiệm vụ của thư mục `core` và nhiệm vụ hiện tại của từng file mã nguồn dùng chung trong thư mục.

## Nhiệm Vụ Các File Mã Nguồn

### `settings_loader.py`

File này đã có mã nguồn.

Nội dung chính:

- Import `os`, `yaml`, `Path` và `load_dotenv`.
- Xác định `BASE_DIR` là thư mục gốc của dự án.
- Xác định đường dẫn `config/settings.yaml`.
- Xác định đường dẫn `.env`.
- Gọi `load_dotenv(ENV_PATH)`.
- Định nghĩa hàm `load_settings()`.

Hàm `load_settings()` đang làm các việc sau:

- Mở `config/settings.yaml`.
- Đọc YAML bằng `yaml.safe_load`.
- Ghi đè `settings["app"]["env"]` bằng `APP_ENV` nếu có.
- Ghi đè cấu hình Qdrant bằng các biến `QDRANT_URL`, `QDRANT_API_KEY`, `QDRANT_COLLECTION_NAME`, `QDRANT_TIMEOUT` nếu có.
- Ghi đè cấu hình embedding bằng `EMBEDDING_MODEL`, `EMBEDDING_DEVICE`, `EMBEDDING_BATCH_SIZE` nếu có.
- Ghi đè cấu hình LLM bằng `LLM_PROVIDER`, `LLM_MODEL_NAME`, `LLM_BASE_URL`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, `LLM_TEMPERATURE`, `LLM_MAX_TOKENS`, `LLM_TIMEOUT` nếu có.
- Ghi đè cấu hình retrieval bằng `RETRIEVAL_TOP_K`, `RETRIEVAL_SCORE_THRESHOLD`, `DENSE_WEIGHT`, `BM25_WEIGHT` nếu có.
- Đảm bảo key `reranking` tồn tại.
- Ghi đè cấu hình reranking bằng `RERANKING_MODEL`, `RERANKING_DEVICE`, `RERANKING_TOP_K` nếu có.
- Trả về dictionary `settings`.

Vai trò và luồng hoạt động:

- `settings_loader.py` chịu trách nhiệm gom cấu hình runtime của dự án từ `config/settings.yaml` và biến môi trường.
- `load_dotenv(ENV_PATH)` được gọi ở cấp module để nạp `.env` vào environment, nhưng tài liệu không đọc hoặc ghi nội dung secret.
- `load_settings()` đọc YAML trước để lấy cấu hình mặc định, sau đó ghi đè từng nhóm cấu hình bằng biến môi trường nếu biến đó tồn tại.
- Input chính là file `config/settings.yaml` và các biến môi trường đã nạp.
- Output chính là một dictionary `settings` đã sẵn sàng cho các module khác dùng chung.
- Đây là điểm tập trung cấu hình cho `data`, `embedding`, `vector_database`, `llm`, `retrieval` và `reranking`.

### `logging_setup.py`

File này đã có mã nguồn.

Nội dung chính:

- Import `logging.config`, `yaml` và `Path`.
- Xác định `BASE_DIR` là thư mục gốc của dự án.
- Xác định đường dẫn `config/logging.yaml`.
- Xác định thư mục `logs`.
- Định nghĩa hàm `setup_logging()`.

Hàm `setup_logging()` đang làm các việc sau:

- Tạo thư mục `logs` nếu thư mục chưa tồn tại.
- Mở file `config/logging.yaml`.
- Đọc YAML bằng `yaml.safe_load`.
- Áp dụng cấu hình logging bằng `logging.config.dictConfig`.

Vai trò và luồng hoạt động:

- `logging_setup.py` chịu trách nhiệm khởi tạo logging cho toàn bộ ứng dụng theo cấu hình YAML.
- `setup_logging()` đảm bảo thư mục `logs` tồn tại trước khi `FileHandler` ghi log.
- Hàm đọc `config/logging.yaml`, chuyển YAML thành dictionary Python, rồi truyền vào `logging.config.dictConfig`.
- Input chính là file `config/logging.yaml`.
- Output là trạng thái logging global đã được cấu hình; các module khác có thể gọi `logging.getLogger("<ten_logger>")` để ghi log theo cấu hình này.

## Cách Hoạt Động Hiện Tại

Các module khác import `load_settings()` để lấy cấu hình dạng dictionary.

Khi cần logging theo cấu hình YAML, entrypoint cần gọi `setup_logging()`. Sau đó các module có thể dùng `logging.getLogger("<ten_logger>")`.

Ví dụ hiện tại trong `ingestion/load_data.py`, logger được lấy bằng tên `ingestion`.

## Ghi Chú Kỹ Thuật

File `.env` được nạp nhưng tài liệu này không đọc hoặc ghi nội dung `.env`.

Git status hiện cho thấy các file cũ `core/load_settings.py` và `core/setup_logging.py` đang ở trạng thái deleted, còn `core/settings_loader.py` và `core/logging_setup.py` là file hiện có trong thư mục.
