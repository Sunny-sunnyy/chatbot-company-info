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
- 2026-07-26 16:54 +07 - Cập nhật trạng thái sau buổi 6: bổ sung mô tả code retrieval, prompt template và LLM generator; tại thời điểm đó `core/schema.py` và `chat.py` vẫn rỗng.
- 2026-07-26 21:02 +07 - Cập nhật trạng thái sau buổi 7: bổ sung `core/schema.py`, FastAPI backend trong `api`, frontend Next.js trong `frontend`, README cho các folder mới và kết quả kiểm tra build frontend.
- 2026-07-26 21:16 +07 - Cập nhật trạng thái sau khi người dùng xoá `chat.py` ở thư mục gốc và kiểm tra lại file rỗng hiện tại.
- 2026-07-27 16:03 +07 - Cập nhật trạng thái sau khi thêm luồng OpenRouter isolated path bằng OpenAI Agents SDK, endpoint `POST /api/chat/openai`, frontend gọi endpoint mới và automated tests không gọi API thật.
- 2026-07-27 17:04 +07 - Cập nhật trạng thái sau khi xác định `final_output` rỗng do OpenRouter reasoning tokens dùng hết `max_tokens`; `generator_openai.py` đã tắt reasoning bằng `ModelSettings.extra_body`.
- 2026-07-27 17:13 +07 - Cập nhật `api/app.py` để lệnh `uv run python -m api.app` chạy Uvicorn với `reload=False` và bind `127.0.0.1`, tránh WatchFiles theo dõi toàn repo.
- 2026-07-27 17:19 +07 - Đổi host trong `api/app.py` sang `localhost` để backend chạy tại `localhost:8000`.
- 2026-07-29 10:28 +07 - Cập nhật mốc học: dự án chuyển sang nhánh `UpdateV2` và bắt đầu giai đoạn nâng cao theo nội dung giới thiệu trong `tai_lieu/p2/0.txt`.
- 2026-07-29 20:56 +07 - Cập nhật trạng thái sau khi đọc `tai_lieu/p2/2.txt`: hoàn thiện mô tả chunking nâng cao, loại bỏ `heroSlides.py` khỏi pipeline, sửa import `interiorStyles.py` trong pipeline và kiểm tra lại số chunk hiện tại.

## Mốc Học Hiện Tại

Dự án hiện đã hoàn thành giai đoạn 1 sau buổi 7 và đang ở branch `UpdateV2` của giai đoạn nâng cao.

`tai_lieu/p2/0.txt` là bài giới thiệu của giai đoạn nâng cao. Nội dung bài này mô tả mục tiêu cải tiến chatbot hiện tại để trả lời nhanh hơn, đầy đủ hơn và có trải nghiệm tốt hơn so với bản cơ bản sau giai đoạn 1. Các nhóm cải tiến được giới thiệu gồm cải tiến chunking, chia chunk lớn thành chunk nhỏ hơn, bổ sung hướng embedding nâng cao, xem xét lại vector store, cải tiến retrieval và hoàn thiện trải nghiệm chat.

`tai_lieu/p2/2.txt` là bài hoàn thiện code chunking và đánh giá point dữ liệu. Nội dung bài tập trung vào việc làm gọn chunking, tách chunk theo ngữ nghĩa nhỏ hơn, dùng metadata nền, thêm `chunk_id`, `chunk_type`, `priority`, chia text dài bằng `split_paragraphs()` và bỏ `heroSlides` khỏi pipeline vì loại dữ liệu này dễ gây nhiễu retrieval.

Tại thời điểm cập nhật sau `p2/2`, phần chunking trong code đã có helper metadata, helper chia đoạn, nhiều loại chunk nhỏ cho `projects`, `news`, `companyInfo`, các danh mục, phong cách nội thất và loại kiến trúc. File `ingestion/chunking/heroSlides.py` đã bị xoá và `ingestion/pipeline.py` không còn gọi `chunk_hero_slides()`.

Mã nguồn hiện tại đã có phần embedding, vector store dense-only, retrieval, schema `RetrievedDocument`, prompt template, legacy Ollama generator, OpenRouter generator bằng OpenAI Agents SDK, FastAPI backend và frontend Next.js. Người dùng đã từng chạy thành công `uv run python -m ingestion.pipeline` sau buổi 5, tạo collection `nmk_chatbot_collection` và upsert 450 chunks vào Qdrant. Sau cập nhật `p2/2`, code chunking hiện tạo 450 chunk khi chỉ chạy các hàm chunking, nhưng pipeline chưa được chạy lại để upsert bộ point mới vào Qdrant trong phiên kiểm tra này. `chat.py` ở thư mục gốc đã được xoá; luồng chat legacy hiện nằm trong `api/routes/chat.py`, còn luồng OpenRouter mới nằm trong `api/routes/chat_openai.py`.

## Mục Tiêu Dự Án

Đây là dự án học Python RAG để xây dựng chatbot trả lời thông tin về công ty Nguyen Minh Khang Architects.

Dữ liệu hiện tại mô tả thông tin công ty, hero slides, phong cách nội thất, loại kiến trúc, danh mục dự án, dự án, danh mục tin tức và tin tức. Trong code chunking hiện tại, `heroSlides.json` vẫn tồn tại trong dữ liệu processed nhưng không còn được đưa vào pipeline tạo chunk.

Dự án hiện đi theo hướng RAG, không phải fine-tuning. Dữ liệu được xử lý thành các chunk có thể truy xuất, sau đó dùng làm ngữ cảnh cho LLM khi trả lời câu hỏi.

## Cấu Trúc Thư Mục Hiện Tại

Các thư mục chính hiện có:

- `config`: chứa cấu hình YAML cho ứng dụng và logging.
- `core`: chứa mã dùng chung để đọc settings và cấu hình logging.
- `api`: chứa FastAPI backend, health check, chat route legacy và chat route OpenRouter.
- `data`: chứa dữ liệu gốc và dữ liệu đã tách theo bảng.
- `frontend`: chứa frontend Next.js, React, TypeScript và Tailwind CSS cho giao diện chat.
- `ingestion`: chứa mã nạp dữ liệu, pipeline ingestion và xử lý dữ liệu đầu vào.
- `ingestion/chunking`: chứa mã chunking theo từng bảng dữ liệu đang dùng; `heroSlides.py` đã bị xoá khỏi code chunking hiện tại.
- `ingestion/helpers`: chứa helper tạo metadata và chia đoạn text.
- `embedding`: chứa mã load model embedding và tạo embedding theo batch.
- `vectorstore`: chứa code kết nối Qdrant, tạo collection dense-only, build point và upsert chunk vào Qdrant.
- `retrieval`: chứa code truy vấn Qdrant bằng embedding query và chuẩn hóa kết quả về `RetrievedDocument`.
- `llm`: chứa prompt template, legacy Ollama generator và OpenRouter generator dùng OpenAI Agents SDK.
- `logs`: chứa file log của ứng dụng.
- `report`: chứa tài liệu báo cáo trạng thái dự án.
- `tai_lieu`: chứa phiên âm các buổi học.
- `tests`: chứa automated tests cho luồng OpenRouter mới, không gọi API thật.
- `qdrant_storage`: chứa dữ liệu local do Qdrant Docker container tạo ra.

## Phần Đã Có Mã Nguồn

`core/settings_loader.py` đã có hàm `load_settings()`. Hàm này đọc `config/settings.yaml`, nạp biến môi trường từ `.env`, sau đó ghi đè một số giá trị cấu hình bằng biến môi trường nếu các biến đó tồn tại.

`core/logging_setup.py` đã có hàm `setup_logging()`. Hàm này tạo thư mục `logs` nếu cần, đọc `config/logging.yaml` và áp dụng cấu hình logging bằng `logging.config.dictConfig`.

`core/schema.py` đã có dataclass `RetrievedDocument`. Schema này gồm `id`, `score`, `text` và `metadata`, đang được `retrieval/retriever.py` dùng để chuẩn hóa kết quả truy vấn từ Qdrant.

`api/app.py` đã có FastAPI app. File này gọi `setup_logging()`, cấu hình CORS, đăng ký `GET /`, `GET /health`, `POST /api/chat` và `POST /api/chat/openai`, đồng thời có block chạy Uvicorn khi dùng `uv run python -m api.app`. Block này hiện bind `localhost`, port `8000` và không bật reload.

`api/health.py` đã có endpoint `GET /health`. Endpoint kiểm tra kết nối Qdrant, thử load embedding model và trả cấu hình LLM provider/model. Health check này có thể load embedding model khi được gọi.

`api/routes/chat.py` đã có endpoint `POST /chat`. Vì `api/app.py` đăng ký router với prefix `/api`, endpoint đầy đủ là `POST /api/chat`. Route nhận `query` và `session_id`, gọi `retrieve(question)`, build context từ document truy xuất được, gọi `generate_answer(context, question)`, lưu session trong memory và trả `answer`, `sources`, `session_id`.

`api/routes/chat_openai.py` đã có endpoint `POST /chat/openai`. Vì `api/app.py` đăng ký router với prefix `/api`, endpoint đầy đủ là `POST /api/chat/openai`. Route này giữ schema riêng, nhận `query` và `session_id`, gọi `retrieve(question)`, build context từ document truy xuất được, gọi `await generate_answer_async(context, question)` từ `llm/generator_openai.py`, lưu session trong memory và trả `answer`, `sources`, `session_id`.

`ingestion/load_data.py` đã có hàm `load_data()`. Hàm này đọc file JSON gốc trong `data/raw`, lấy object `tables`, bỏ qua các bảng rỗng và ghi từng bảng có dữ liệu ra `data/processed/<ten_bang>.json`.

`ingestion/pipeline.py` đã có hàm `run_ingestion_pipeline()`. Hàm này gọi các hàm chunking cho architecture types, company info, interior styles, news categories, news, project categories và projects, gom `all_chunks`, rồi gọi `upsert_chunks(all_chunks)`. Sau `p2/2`, pipeline không còn import hoặc gọi `heroSlides.py`. Import trong pipeline đã được kiểm tra lại bằng `uv run` và hiện import được.

`ingestion/chunking` hiện có các module chunking cho nhiều bảng dữ liệu đã xử lý:

- `architectureTypes.py`: tạo chunk cho loại kiến trúc từ `architectureTypes.json`.
- `companyInfo.py`: tạo chunk tổng quan, mô tả và thông tin liên hệ công ty từ `companyInfo.json`.
- `interiorStyles.py`: tạo chunk cho phong cách nội thất từ `interiorStyles.json`.
- `newCategories.py`: tạo chunk cho danh mục tin tức từ `newsCategories.json`.
- `news.py`: chuyển HTML tin tức sang text, chia nội dung thành đoạn và tạo chunk từ `news.json`.
- `projectCategories.py`: tạo chunk cho danh mục dự án từ `projectCategories.json`.
- `projects.py`: tạo nhiều loại chunk cho dự án từ `projects.json`, gồm overview, description, style, context, specs và media.

`ingestion/chunking/heroSlides.py` không còn tồn tại. Theo nội dung `tai_lieu/p2/2.txt`, hero slides bị loại khỏi pipeline vì có thể trộn lẫn nội dung trang chủ, dự án, tin tức và các phần trình bày khác, làm nhiễu retrieval nếu không xử lý riêng.

`ingestion/helpers/make_metadata.py` hiện có hàm `make_metadata()` để thêm `chunk_id` UUID và merge metadata. `ingestion/helpers/split_paragraphs.py` hiện có hàm `split_paragraphs()` để chia text dài thành các đoạn nhỏ. `ingestion/helpers/__init__.py` đang rỗng và chỉ đóng vai trò package marker.

`embedding/embedder.py` đã có hàm `get_model()` và `embed_texts()`. File này load `SentenceTransformer` theo cấu hình `embedding.model`, cache model trong biến module `_model`, tạo embedding đã normalize và trả về dạng list để lưu vào vector store.

`embedding/batch_embed.py` đã có hàm `batch_embed_texts()`. File này đọc `embedding.batch_size` từ settings, chia danh sách text thành batch, gọi `embed_texts()` cho từng batch và gộp kết quả embedding.

`vectorstore/qdrant.py` đã có hàm `get_qdrant_client()` và `ensure_collection()`. File này đọc cấu hình Qdrant từ settings, tạo `QdrantClient`, kiểm tra kết nối bằng `get_collections()`, và tạo collection dense-only bằng `VectorParams` nếu collection chưa tồn tại.

`vectorstore/index.py` đã có hàm `build_qdrant_points()`. File này lấy text từ các chunk, gọi `embedding.embedder.embed_texts()` để tạo embedding, rồi build point dictionary gồm `id`, `vector` và `payload`.

`vectorstore/upsert.py` đã có hàm `upsert_chunks()`. File này lấy Qdrant client, đảm bảo collection tồn tại, gọi `build_qdrant_points(chunks)` để tạo dense-only point và gọi `client.upsert(...)`.

`retrieval/retriever.py` đã có hàm `retrieve(query)`. File này embedding câu hỏi bằng `embed_texts([query])`, truy vấn Qdrant bằng `client.query_points(...)`, lấy payload gồm `text` và metadata, rồi chuẩn hóa kết quả về `RetrievedDocument`. Sau buổi 7, module này đã import được vì `core/schema.py` đã có `RetrievedDocument`.

`llm/prompt.py` đã có `SYSTEM_PROMPT` và hàm `build_prompt(context, question)`. File này tạo prompt tiếng Việt cho chatbot NMK Architects, yêu cầu trả lời dựa trên context và không tự bịa thông tin ngoài dữ liệu.

`llm/generator.py` đã có hàm `generate_answer(context, question)`. File này được giữ nguyên làm legacy Ollama generator: kiểm tra context/question rỗng, gọi `build_prompt(...)`, rồi nếu `llm.provider` là `ollama` thì gọi `ollama.Client(...).chat(...)` để sinh câu trả lời. Với cấu hình `llm.provider: openrouter`, file này sẽ trả về thông báo nhà cung cấp mô hình không được hỗ trợ.

`llm/generator_openai.py` đã có hàm async `generate_answer_async(context, question)`. File này kiểm tra input, yêu cầu `llm.provider` là `openrouter`, lấy API key OpenRouter từ settings đã nạp biến môi trường, build prompt bằng `build_prompt(...)`, tạo `AsyncOpenAI` với `base_url` OpenRouter, tạo `OpenAIChatCompletionsModel`, tạo `Agent` tên `nmk_chatbot`, truyền `temperature` và `max_tokens` qua `ModelSettings`, tắt OpenRouter reasoning bằng `extra_body={"reasoning": {"effort": "none"}}`, disable tracing bằng `set_tracing_disabled(True)`, rồi gọi `await Runner.run(agent, prompt)` để sinh câu trả lời. File này trả thông báo tiếng Việt khi thiếu API key, provider không hỗ trợ, timeout, lỗi kết nối hoặc lỗi API.

`frontend/app/page.tsx` đã render `ChatInterface`. `frontend/app/layout.tsx` đã khai báo layout gốc và metadata. `frontend/app/globals.css` đã cấu hình Tailwind và CSS variables nền/chữ.

`frontend/components/ChatInterface.tsx` đã có UI chat client-side. Component lưu messages, input, loading state và session id; gửi câu hỏi bằng `chatService.sendMessage(...)`; hiển thị câu trả lời, lỗi cơ bản và tối đa 3 hình ảnh từ metadata source nếu có.

`frontend/lib/api.ts` đã có Axios client. File này hiện gọi `POST /api/chat/openai` và có hàm `healthCheck()` gọi `GET /health`. `healthCheck()` hiện được định nghĩa nhưng chưa được gọi trong UI.

`tests/conftest.py` đã thêm project root vào `sys.path` để pytest import được package local.

`tests/test_llm_generator_openai.py` đã test `generate_answer_async()` với context rỗng, question rỗng, thiếu API key OpenRouter và happy path monkeypatch `Runner.run`. Test này không gọi OpenRouter thật.

`tests/test_api_chat_openai.py` đã test trực tiếp `chat_openai_endpoint()` với monkeypatch retrieval và generator. Test này không gọi Qdrant hoặc OpenRouter thật.

## File Rỗng Hiện Tại

Các file sau hiện tồn tại nhưng đang rỗng:

- `api/__init__.py`
- `core/__init__.py`
- `embedding/__init__.py`
- `ingestion/__init__.py`
- `ingestion/chunking/__init__.py`
- `ingestion/helpers/__init__.py`
- `llm/__init__.py`
- `retrieval/__init__.py`
- `vectorstore/__init__.py`

Các file `__init__.py` rỗng hiện chỉ đóng vai trò package marker.

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

Sau khi cập nhật code chunking theo `p2/2`, kiểm tra import tối thiểu đã chạy thành công:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import importlib; importlib.import_module('ingestion.pipeline'); print('ingestion.pipeline import ok')"
```

Kết quả: `ingestion.pipeline import ok`.

Kiểm tra số chunk hiện tại bằng cách gọi trực tiếp các hàm chunking, không upsert Qdrant, cho kết quả:

- `architectureTypes`: 0 chunk
- `companyInfo`: 3 chunks
- `interiorStyles`: 10 chunks
- `newsCategories`: 4 chunks
- `news`: 163 chunks
- `projectCategories`: 12 chunks
- `projects`: 258 chunks
- Tổng cộng: 450 chunks

Trong lần kiểm tra số chunk này vẫn có warning `Empty text provided to split_paragraphs` do một số bản ghi có trường text rỗng hoặc thiếu nội dung để chia đoạn. Warning không làm các hàm chunking dừng.

Sau khi thêm code buổi 7, kiểm tra tĩnh đã từng chạy thành công:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile api/app.py api/health.py api/routes/chat.py retrieval/retriever.py llm/generator.py core/schema.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import importlib; importlib.import_module('api.app'); print('api.app import ok')"
```

Kết quả: các file Python liên quan compile được và `api.app` import được.

Sau khi thêm luồng OpenRouter isolated path, các kiểm tra mới đã chạy thành công:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_llm_generator_openai.py -q
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_chat_openai.py -q
npm run build
```

Kết quả: generator tests pass, route OpenRouter test pass và frontend production build compile thành công. E2E thật với Qdrant, backend, frontend và OpenRouter API key ban đầu trả response có `answer` rỗng vì OpenRouter dùng hết `max_tokens` cho reasoning tokens. Sau khi tắt reasoning bằng `ModelSettings.extra_body`, request thật qua backend tạm đã trả `answer_len: 730`.

Frontend hiện có `node_modules/` local tại thời điểm kiểm tra này. Thư mục này được `frontend/.gitignore` ignore.

Kiểm tra frontend hiện tại đã chạy thành công:

```bash
npm run build
```

Kết quả: Next.js production build compile thành công, type check thành công và route `/` được prerender thành static content. Development server chưa được khởi động trong phiên kiểm tra này.

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

Qdrant local hiện có dữ liệu được lưu trong `qdrant_storage/` do Docker Compose mount từ `./qdrant_storage` vào `/qdrant/storage` trong container. Collection `nmk_chatbot_collection` đã nhận 450 points theo log chạy pipeline sau buổi 5. Sau cập nhật `p2/2`, code chunking đã đổi thành phần chunk nhưng chưa chạy lại ingestion để thay thế dữ liệu trong Qdrant trong phiên kiểm tra này.

## Quyết Định Kỹ Thuật Hiện Tại

Dự án dùng Python và quản lý môi trường bằng `uv`.

File `pyproject.toml` yêu cầu Python `>=3.12`.

CodeGraph đã được cài ở máy local với phiên bản `1.5.0` và đã được init cho repo này. Sau lần kiểm tra gần nhất, `codegraph status .` ghi nhận index hiện có 51 file, 350 nodes, 543 edges, backend `node:sqlite` với journal `wal`, và `Index is up to date`.

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

Code LLM legacy nằm trong `llm/generator.py`, không còn file `llm/llm.py` trong cây thư mục hiện tại. `llm/generator.py` chỉ có nhánh gọi Ollama khi `llm.provider == "ollama"` và được giữ nguyên để so sánh/rollback.

Code LLM OpenRouter mới nằm trong `llm/generator_openai.py`. File này dùng OpenAI Agents SDK và OpenAI Python SDK để gọi OpenRouter qua endpoint OpenAI-compatible. File hiện tắt reasoning tokens cho OpenRouter để tránh câu trả lời rỗng với model hiện tại.

Dữ liệu được xử lý theo hướng tách bảng, tạo chunk riêng theo từng nhóm dữ liệu đang dùng, tạo embedding theo batch, rồi chuẩn bị point dense-only để lưu vào Qdrant. Sau `p2/2`, `heroSlides.json` vẫn là dữ liệu processed nhưng không còn có module chunking và không còn nằm trong pipeline. Phần retrieval, schema, API backend, frontend và luồng OpenRouter mới đã có mã. Entrypoint `chat.py` ở thư mục gốc đã được xoá; backend hiện chạy qua `api/app.py`.

Backend chạy bằng:

```bash
uv run python -m api.app
```

Lệnh này hiện không bật Uvicorn reload, nên không còn WatchFiles theo dõi toàn bộ repo trong lúc chạy song song frontend.

Frontend chạy trong terminal riêng bằng:

```bash
cd frontend
npm install
npm run dev
```

Frontend hiện gọi endpoint OpenRouter mới:

```text
POST /api/chat/openai
```

Nếu muốn đổi frontend về endpoint legacy `POST /api/chat`, sửa endpoint trong `frontend/lib/api.ts` theo hướng dẫn trong `frontend/README_frontend.md` hoặc `frontend/lib/README_lib.md`.

README ở các folder có file Python thật hiện đã được bổ sung phần giải thích vai trò file mã nguồn, hàm hoặc luồng chính, input/output khi rõ ràng và trạng thái chạy hiện tại nếu luồng chưa hoàn chỉnh. Các file rỗng vẫn được ghi rõ là chưa phát triển.
