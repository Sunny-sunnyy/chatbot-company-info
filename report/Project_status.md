# Trạng Thái Hiện Tại Của Dự Án

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo bản ghi trạng thái dự án sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra mã nguồn hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ ghi những phần đã tồn tại trong dự án.
- 2026-07-24 22:06 +07 - Cập nhật trạng thái chunking theo mã nguồn hiện tại trong `ingestion/chunking` và `ingestion/helpers`.
- 2026-07-25 17:23 +07 - Đối chiếu lại README với mã nguồn hiện tại và cập nhật trạng thái các module `embedding`, `ingestion`, `vectorstore`, `retrieval`, `llm` và `chat.py`.
- 2026-07-25 17:34 +07 - Nâng cấp CodeGraph lên `1.5.0`, init index local cho repo và ignore `.codegraph/`.
- 2026-07-25 17:37 +07 - Bổ sung hướng dẫn sử dụng CodeGraph vào `report/Agent_session_prompt.md`.
- 2026-07-25 18:42 +07 - Cập nhật trạng thái sau khi đọc `tai_lieu/4.txt`, kiểm tra code embedding/vectorstore và audit README theo folder.
- 2026-07-25 20:22 +07 - Bổ sung chuẩn mô tả vai trò và luồng hoạt động của file mã nguồn trong README các folder có Python code.

## Mốc Học Hiện Tại

Dự án hiện đã được kiểm tra sau khi hoàn thành buổi 4.

Buổi 4 trình bày phần embedding, batch embedding, kết nối Qdrant, đảm bảo collection tồn tại, build point từ chunk và upsert point vào vector store.

Mã nguồn hiện tại đã có phần embedding và đã có code trong `vectorstore`, nhưng luồng ingestion-to-vector-store chưa chạy được end-to-end trong trạng thái hiện tại.

## Mục Tiêu Dự Án

Đây là dự án học Python RAG để xây dựng chatbot trả lời thông tin về công ty Nguyen Minh Khang Architects.

Dữ liệu hiện tại mô tả thông tin công ty, hero slides, phong cách nội thất, loại kiến trúc, danh mục dự án, dự án, danh mục tin tức và tin tức.

Dự án hiện đi theo hướng RAG, không phải fine-tuning. Dữ liệu được xử lý thành các chunk có thể truy xuất, sau đó dùng làm ngữ cảnh cho LLM khi trả lời câu hỏi.

## Cấu Trúc Thư Mục Hiện Tại

Các thư mục chính hiện có:

- `config`: chứa cấu hình YAML cho ứng dụng và logging.
- `core`: chứa mã dùng chung để đọc settings và cấu hình logging.
- `data`: chứa dữ liệu gốc và dữ liệu đã tách theo bảng.
- `ingestion`: chứa mã nạp dữ liệu, pipeline ingestion và xử lý dữ liệu đầu vào.
- `ingestion/chunking`: chứa mã chunking theo từng bảng dữ liệu.
- `ingestion/helpers`: chứa helper tạo metadata và chia đoạn text.
- `embedding`: chứa mã load model embedding và tạo embedding theo batch.
- `vectorstore`: chứa code kết nối Qdrant, tạo collection, build point và upsert chunk, nhưng hiện còn lỗi import/module khi chạy.
- `retrieval`: hiện chỉ có file Python rỗng.
- `llm`: hiện chỉ có các file Python rỗng.
- `logs`: chứa file log của ứng dụng.
- `report`: chứa tài liệu báo cáo trạng thái dự án.
- `tai_lieu`: chứa phiên âm các buổi học.

## Phần Đã Có Mã Nguồn

`core/settings_loader.py` đã có hàm `load_settings()`. Hàm này đọc `config/settings.yaml`, nạp biến môi trường từ `.env`, sau đó ghi đè một số giá trị cấu hình bằng biến môi trường nếu các biến đó tồn tại.

`core/logging_setup.py` đã có hàm `setup_logging()`. Hàm này tạo thư mục `logs` nếu cần, đọc `config/logging.yaml` và áp dụng cấu hình logging bằng `logging.config.dictConfig`.

`ingestion/load_data.py` đã có hàm `load_data()`. Hàm này đọc file JSON gốc trong `data/raw`, lấy object `tables`, bỏ qua các bảng rỗng và ghi từng bảng có dữ liệu ra `data/processed/<ten_bang>.json`.

`ingestion/pipeline.py` đã có hàm `run_ingestion_pipeline()`. Hàm này gọi các hàm chunking, gom `all_chunks`, rồi gọi `upsert_chunks(all_chunks)`. Trạng thái hiện tại của file này chưa chạy được nguyên vẹn vì đang import `ingestion.chunking.interiorStylesnteriorStyles` trong khi file thật là `ingestion/chunking/interiorStyles.py`. Ngoài ra, phần `vectorstore` hiện có code nhưng còn lỗi import/module nên chưa xác nhận được luồng upsert end-to-end.

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

`embedding/embedder.py` đã có hàm `get_model()` và `embed_texts()`. File này load `SentenceTransformer` theo cấu hình `embedding.model`, cache model trong biến module `_model`, tạo embedding đã normalize và trả về dạng list để lưu vào vector store.

`embedding/batch_embed.py` đã có hàm `batch_embed_texts()`. File này đọc `embedding.batch_size` từ settings, chia danh sách text thành batch, gọi `embed_texts()` cho từng batch và gộp kết quả embedding.

`vectorstore/qdrant.py` đã có hàm `get_qdrant_client()` và `ensure_collection()`. File này đọc cấu hình Qdrant từ settings, tạo `QdrantClient`, kiểm tra kết nối bằng `get_collections()`, và tạo collection có dense vector tên `dense` cùng sparse vector tên `sparse` nếu collection chưa tồn tại.

`vectorstore/index.py` đã có hàm `build_qdrant_points()`. File này lấy text từ các chunk, gọi `embedding.embedder.embed_texts()` để tạo embedding, rồi build point dictionary gồm `id`, `vector` và `payload`.

`vectorstore/upsert.py` đã có hàm `upsert_chunks()`. File này lấy Qdrant client, đảm bảo collection tồn tại, fit sparse embedder, build hybrid point và gọi `client.upsert(...)`.

## Phần Chưa Được Phát Triển

Các file sau hiện tồn tại nhưng đang rỗng:

- `chat.py`
- `retrieval/retriever.py`
- `llm/llm.py`
- `llm/prompt.py`

## Trạng Thái Chạy Hiện Tại

`ingestion/pipeline.py` hiện chưa import được vì file đang import `ingestion.chunking.interiorStylesnteriorStyles`, trong khi file thật là `ingestion/chunking/interiorStyles.py`.

Các module local trong thư mục `vectorstore` hiện chưa import được bằng `import vectorstore.qdrant` trong môi trường `uv run`, vì Python đang resolve `vectorstore` tới package dependency trong `.venv/site-packages/vectorstore`.

`vectorstore/upsert.py` hiện còn tham chiếu hai module chưa tồn tại trong repo:

- `vectorstore.hybrid_index`
- `embedding.sparse_embedder`

Vì các điểm trên, trạng thái code hiện tại chưa xác nhận được việc upsert chunk vào Qdrant chạy thành công end-to-end.

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

CodeGraph đã được cài ở máy local với phiên bản `1.5.0` và đã được init cho repo này. Sau lần sync gần nhất, `codegraph status .` ghi nhận index hiện có 25 file, 170 nodes, 261 edges, backend `node:sqlite` với journal `wal`.

Thư mục `.codegraph/` là artifact local của CodeGraph, đã được thêm vào `.gitignore` và không nên commit.

Codex đã có MCP config cho CodeGraph trong cấu hình người dùng. Sau khi upgrade CodeGraph, session agent mới nên dùng binary mới; session đang chạy từ trước có thể vẫn giữ MCP process cũ cho tới khi restart. CLI `codegraph explore` hiện hoạt động trong repo này.

Theo tài liệu CodeGraph, auto-sync được bật mặc định sau `codegraph init`, nên graph được cập nhật khi file trong project thay đổi. Có thể chạy `codegraph sync` thủ công nếu cần đồng bộ lại.

Cấu hình chính được đặt trong `config/settings.yaml`.

Cấu hình logging được đặt trong `config/logging.yaml`.

Biến môi trường được nạp bằng `python-dotenv`. Tài liệu này không ghi nội dung `.env`.

Embedding model đang được cấu hình là `intfloat/multilingual-e5-small`.

Vector database đang được cấu hình là Qdrant, tên collection là `nmk_chatbot_collection`, distance là `cosine`, vector size là `384`.

Nhà cung cấp LLM trong settings đang là `openrouter`, tên model đang là `qwen/qwen3.5-9b`, temperature là `0.2`.

Dữ liệu được xử lý theo hướng tách bảng, tạo chunk riêng theo từng bảng, tạo embedding theo batch, rồi chuẩn bị point để lưu vào Qdrant. Phần retrieval, LLM và entrypoint chat chưa có mã triển khai.

README ở các folder có file Python thật hiện đã được bổ sung phần giải thích vai trò file mã nguồn, hàm hoặc luồng chính, input/output khi rõ ràng và trạng thái chạy hiện tại nếu luồng chưa hoàn chỉnh. Các file rỗng vẫn được ghi rõ là chưa phát triển.
