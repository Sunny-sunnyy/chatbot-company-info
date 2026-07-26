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
- 2026-07-26 12:23 +07 - Cập nhật trạng thái sau buổi 5: Qdrant chạy bằng Docker Compose, pipeline ingestion upsert 450 chunks thành công và tài liệu Docker được bổ sung.
- 2026-07-26 16:54 +07 - Cập nhật trạng thái sau buổi 6: bổ sung mô tả code retrieval, prompt template và LLM generator; ghi rõ `core/schema.py` và `chat.py` vẫn rỗng.

## Mốc Học Hiện Tại

Dự án hiện đã được kiểm tra sau khi hoàn thành buổi 6.

Buổi 6 trình bày cách viết retriever để embedding query và truy vấn Qdrant, cách tạo prompt template từ context và question, và cách viết LLM generator dùng Ollama để sinh câu trả lời.

Mã nguồn hiện tại đã có phần embedding, vector store dense-only, retrieval, prompt template và LLM generator. Người dùng đã chạy thành công `uv run python -m ingestion.pipeline`, tạo collection `nmk_chatbot_collection` và upsert 450 chunks vào Qdrant. `core/schema.py` và `chat.py` hiện vẫn rỗng.

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
- `vectorstore`: chứa code kết nối Qdrant, tạo collection dense-only, build point và upsert chunk vào Qdrant.
- `retrieval`: chứa code truy vấn Qdrant bằng embedding query, nhưng hiện phụ thuộc `core/schema.py` đang rỗng.
- `llm`: chứa prompt template và generator tạo câu trả lời bằng Ollama khi `llm.provider` là `ollama`.
- `logs`: chứa file log của ứng dụng.
- `report`: chứa tài liệu báo cáo trạng thái dự án.
- `tai_lieu`: chứa phiên âm các buổi học.
- `qdrant_storage`: chứa dữ liệu local do Qdrant Docker container tạo ra.

## Phần Đã Có Mã Nguồn

`core/settings_loader.py` đã có hàm `load_settings()`. Hàm này đọc `config/settings.yaml`, nạp biến môi trường từ `.env`, sau đó ghi đè một số giá trị cấu hình bằng biến môi trường nếu các biến đó tồn tại.

`core/logging_setup.py` đã có hàm `setup_logging()`. Hàm này tạo thư mục `logs` nếu cần, đọc `config/logging.yaml` và áp dụng cấu hình logging bằng `logging.config.dictConfig`.

`ingestion/load_data.py` đã có hàm `load_data()`. Hàm này đọc file JSON gốc trong `data/raw`, lấy object `tables`, bỏ qua các bảng rỗng và ghi từng bảng có dữ liệu ra `data/processed/<ten_bang>.json`.

`ingestion/pipeline.py` đã có hàm `run_ingestion_pipeline()`. Hàm này gọi các hàm chunking, gom `all_chunks`, rồi gọi `upsert_chunks(all_chunks)`. Sau buổi 5, người dùng đã chạy thành công file này bằng `uv run python -m ingestion.pipeline`; log ghi nhận đã upsert 450 chunks vào vector store.

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

`vectorstore/qdrant.py` đã có hàm `get_qdrant_client()` và `ensure_collection()`. File này đọc cấu hình Qdrant từ settings, tạo `QdrantClient`, kiểm tra kết nối bằng `get_collections()`, và tạo collection dense-only bằng `VectorParams` nếu collection chưa tồn tại.

`vectorstore/index.py` đã có hàm `build_qdrant_points()`. File này lấy text từ các chunk, gọi `embedding.embedder.embed_texts()` để tạo embedding, rồi build point dictionary gồm `id`, `vector` và `payload`.

`vectorstore/upsert.py` đã có hàm `upsert_chunks()`. File này lấy Qdrant client, đảm bảo collection tồn tại, gọi `build_qdrant_points(chunks)` để tạo dense-only point và gọi `client.upsert(...)`.

`retrieval/retriever.py` đã có hàm `retrieve(query)`. File này embedding câu hỏi bằng `embed_texts([query])`, truy vấn Qdrant bằng `client.query_points(...)`, lấy payload gồm `text` và metadata, rồi chuẩn hóa kết quả về `RetrievedDocument`. Trạng thái hiện tại: file chưa import/chạy được nguyên vẹn vì `core/schema.py` vẫn rỗng và chưa định nghĩa `RetrievedDocument`.

`llm/prompt.py` đã có `SYSTEM_PROMPT` và hàm `build_prompt(context, question)`. File này tạo prompt tiếng Việt cho chatbot NMK Architects, yêu cầu trả lời dựa trên context và không tự bịa thông tin ngoài dữ liệu.

`llm/generator.py` đã có hàm `generate_answer(context, question)`. File này kiểm tra context/question rỗng, gọi `build_prompt(...)`, rồi nếu `llm.provider` là `ollama` thì gọi `ollama.Client(...).chat(...)` để sinh câu trả lời. Trạng thái hiện tại: `config/settings.yaml` đang để `llm.provider` là `openrouter`, trong khi code generator hiện chỉ hỗ trợ nhánh `ollama`; với cấu hình hiện tại, hàm sẽ trả về thông báo nhà cung cấp mô hình không được hỗ trợ.

## Phần Chưa Được Phát Triển

Các file sau hiện tồn tại nhưng đang rỗng:

- `chat.py`
- `core/schema.py`

## Trạng Thái Chạy Hiện Tại

Người dùng đã chạy Qdrant bằng Docker Compose và chạy thành công:

```bash
uv run python -m ingestion.pipeline
```

Kết quả chạy thực tế đã ghi nhận:

- Qdrant kết nối thành công qua `http://localhost:6333`.
- Collection `nmk_chatbot_collection` được tạo thành công.
- Embedding model `intfloat/multilingual-e5-small` được load.
- `build_qdrant_points()` build 450 Qdrant points.
- `upsert_chunks()` upsert 450 points vào collection `nmk_chatbot_collection`.
- `run_ingestion_pipeline()` log đã upsert 450 chunks vào vector store.

Trong quá trình chạy có nhiều warning `Empty text provided to split_paragraphs`, phản ánh một số bản ghi thiếu nội dung text để chia đoạn. Các warning này không chặn pipeline; luồng ingestion vẫn hoàn tất.

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

Qdrant local hiện có dữ liệu được lưu trong `qdrant_storage/` do Docker Compose mount từ `./qdrant_storage` vào `/qdrant/storage` trong container. Collection `nmk_chatbot_collection` đã nhận 450 points theo log chạy pipeline sau buổi 5.

## Quyết Định Kỹ Thuật Hiện Tại

Dự án dùng Python và quản lý môi trường bằng `uv`.

File `pyproject.toml` yêu cầu Python `>=3.12`.

CodeGraph đã được cài ở máy local với phiên bản `1.5.0` và đã được init cho repo này. Sau lần kiểm tra gần nhất, `codegraph status .` ghi nhận index hiện có 34 file, 224 nodes, 357 edges, backend `node:sqlite` với journal `wal`, và `Index is up to date`.

Thư mục `.codegraph/` là artifact local của CodeGraph, đã được thêm vào `.gitignore` và không nên commit.

Codex đã có MCP config cho CodeGraph trong cấu hình người dùng. Sau khi upgrade CodeGraph, session agent mới nên dùng binary mới; session đang chạy từ trước có thể vẫn giữ MCP process cũ cho tới khi restart. CLI `codegraph explore` hiện hoạt động trong repo này.

Theo tài liệu CodeGraph, auto-sync được bật mặc định sau `codegraph init`, nên graph được cập nhật khi file trong project thay đổi. Có thể chạy `codegraph sync` thủ công nếu cần đồng bộ lại.

Cấu hình chính được đặt trong `config/settings.yaml`.

Cấu hình logging được đặt trong `config/logging.yaml`.

Biến môi trường được nạp bằng `python-dotenv`. Tài liệu này không ghi nội dung `.env`.

Embedding model đang được cấu hình là `intfloat/multilingual-e5-small`.

Vector database đang được cấu hình là Qdrant, tên collection là `nmk_chatbot_collection`, distance là `cosine`, vector size là `384`.

Qdrant đang được chạy bằng Docker Compose từ `docker-compose.yml`, service tên `qdrant`, container name `qdrant_version_1`, REST API port `6333`, gRPC port `6334`, dashboard tại `http://localhost:6333/dashboard`.

Nhà cung cấp LLM trong settings đang là `openrouter`, tên model đang là `qwen/qwen3.5-9b`, temperature là `0.2`.

Code LLM hiện tại nằm trong `llm/generator.py`, không còn file `llm/llm.py` trong cây thư mục hiện tại. Generator hiện chỉ có nhánh gọi Ollama khi `llm.provider == "ollama"`, nên chưa khớp hoàn toàn với cấu hình `openrouter` trong `config/settings.yaml`.

Dữ liệu được xử lý theo hướng tách bảng, tạo chunk riêng theo từng bảng, tạo embedding theo batch, rồi chuẩn bị point dense-only để lưu vào Qdrant. Phần retrieval và LLM đã có mã bước đầu theo buổi 6, nhưng retrieval chưa chạy được nguyên vẹn vì thiếu schema `RetrievedDocument`. Entrypoint `chat.py` chưa có mã triển khai.

README ở các folder có file Python thật hiện đã được bổ sung phần giải thích vai trò file mã nguồn, hàm hoặc luồng chính, input/output khi rõ ràng và trạng thái chạy hiện tại nếu luồng chưa hoàn chỉnh. Các file rỗng vẫn được ghi rõ là chưa phát triển.
