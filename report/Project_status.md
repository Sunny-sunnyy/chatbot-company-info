# Trạng Thái Hiện Tại Của Dự Án

## Nhật Ký Cập Nhật

- 2026-08-04 19:44 +07 - Cập nhật trạng thái layout: tạo thư mục `backend/` làm runtime root cho Python backend; các folder `api`, `config`, `core`, `data`, `embedding`, `ingestion`, `llm`, `logs`, `reranking`, `retrieval`, `scoring`, `vectorstore`, `tests` đã nằm trong `backend/`; frontend, `.env`, Docker Compose, `qdrant_storage/`, `report/` và `tai_lieu/` vẫn ở root; `core/settings_loader.py` load settings từ `backend/config/settings.yaml` và `.env` từ root; lệnh backend chạy từ `backend/`; cập nhật số liệu CodeGraph mới nhất.
- 2026-08-04 19:53 +07 - Audit nhanh sau refactor layout: xác nhận `backend/` có đủ 13 folder mục tiêu, các folder backend cũ không còn ở root, `settings_loader.py` trỏ đúng `backend/config/settings.yaml` và `.env` ở root; sửa các path hiện hành còn sót trong tài liệu từ root sang `backend/...`.
- 2026-08-04 18:01 +07 - Sửa bug UI duplicate assistant khi stream trong `frontend/components/ChatInterface.tsx`: bỏ block loading indicator riêng ở cuối messages list; assistant placeholder cuối cùng đang stream hiển thị 3 chấm loading ngay trong bubble và tự chuyển sang `ReactMarkdown` khi delta đầu tiên tới; `npm run build` pass.
- 2026-08-04 17:33 +07 - Cập nhật trạng thái sau khi triển khai streaming + Markdown: `POST /api/chat/openai` trả SSE `text/event-stream` với các event `meta`/`delta`/`sources`/`done`/`error`; `llm/generator_openai.py` thêm `stream_answer_async()` dùng `Runner.run_streamed()`; `frontend/lib/api.ts` thêm `sendMessageStream()` dùng `fetch`; `ChatInterface.tsx` render Markdown live bằng `react-markdown` + `remark-gfm`; backend tests cập nhật theo SSE contract và smoke test E2E stream 276 delta thành công.
- 2026-08-04 16:03 +07 - Cập nhật `ingestion/chunking/companyInfo.py`: chunk `contact_info` thêm cụm `Thông tin liên hệ của <tên công ty>` để query tự nhiên về thông tin liên hệ truy xuất đúng chunk liên hệ hơn.
- 2026-08-04 16:12 +07 - Rebuild collection Qdrant local `nmk_chatbot_collection` sau thay đổi chunk liên hệ: xoá collection local bị duplicate, chạy lại `ingestion.pipeline`, collection sạch hiện có 450 hybrid points và query `thông tin liên hệ` đưa `company_info/contact_info` lên top 1.
- 2026-08-04 15:41 +07 - Sửa lỗi backend bị WatchFiles reload/kẹt startup khi chạy `uv run python -m api.app`: `api/app.py` hiện tắt Uvicorn `reload`, vẫn bind `0.0.0.0:8000`.
- 2026-08-01 22:04 +07 - Kiểm tra lại `api/routes/chat_openai.py` và sửa tài liệu: `/api/chat/openai` hiện dùng hybrid retrieval + BM25 + reranker + `ContextBuilder`, không dùng dense-only retriever; cập nhật trạng thái CodeGraph mới nhất.
- 2026-08-01 20:40 +07 - Cập nhật trạng thái sau khi nâng cấp `/api/chat/openai` lên v2 (hybrid retrieval + BM25 + reranker + ContextBuilder, vẫn dùng OpenRouter qua OpenAI Agents SDK) và ghi nhận pipeline hybrid đã chạy thành công với collection hybrid 450 points.
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
- 2026-07-30 10:54 +07 - Cập nhật trạng thái sau khi đọc `tai_lieu/p2/3.txt` và `tai_lieu/p2/4.txt`: bổ sung mô tả sparse embedding, ghi nhận `embedding/sparse_embedder.py`, cập nhật trạng thái dữ liệu raw/processed và trạng thái CodeGraph hiện tại.
- 2026-07-30 12:20 +07 - Cập nhật trạng thái sau khi đọc `tai_lieu/p2/5.txt`, `tai_lieu/p2/6.txt` và `tai_lieu/p2/7.txt`: bổ sung `hybrid_index.py`, `hybrid_retriever.py`, `scoring/bm25.py`, lý thuyết BM25/hybrid retrieval và trạng thái CodeGraph mới nhất.
- 2026-07-31 17:07 +07 - Cập nhật trạng thái sau khi đọc `tai_lieu/p2/8.txt` và `tai_lieu/p2/9.txt`: bổ sung mô tả hybrid retriever có BM25, folder `reranking`, `retrieval/context_builder.py` và trạng thái CodeGraph mới nhất.
- 2026-08-01 16:51 +07 - Cập nhật trạng thái khi đang ở `tai_lieu/p2/10.txt`: bổ sung `core/startup.py`, chuyển vectorstore/upsert sang hybrid dense+sparse và ghi nhận rủi ro collection Qdrant cũ dense-only trước khi chạy pipeline.
- 2026-08-01 17:58 +07 - Cập nhật trạng thái sau khi hoàn thành toàn bộ p2: API startup khởi tạo RAG components, `/api/chat` dùng hybrid retrieval + reranker, `/api/chat/openai` sau đó được cập nhật lên hybrid retrieval + OpenRouter và frontend vẫn gọi endpoint OpenRouter.

## Mốc Học Hiện Tại

Dự án hiện đã hoàn thành giai đoạn 1 sau buổi 7 và đã đi hết các transcript giai đoạn nâng cao trong `tai_lieu/p2/0.txt` tới `tai_lieu/p2/10.txt`.

`tai_lieu/p2/0.txt` là bài giới thiệu của giai đoạn nâng cao. Nội dung bài này mô tả mục tiêu cải tiến chatbot hiện tại để trả lời nhanh hơn, đầy đủ hơn và có trải nghiệm tốt hơn so với bản cơ bản sau giai đoạn 1. Các nhóm cải tiến được giới thiệu gồm cải tiến chunking, chia chunk lớn thành chunk nhỏ hơn, bổ sung hướng embedding nâng cao, xem xét lại vector store, cải tiến retrieval và hoàn thiện trải nghiệm chat.

`tai_lieu/p2/1.txt` là bài phân tích và thiết kế lại chunking nâng cao. Nội dung bài tập trung vào việc tách chunk lớn thành các chunk nhỏ hơn theo ý nghĩa, giữ metadata nền, đánh `chunk_id`, dùng `chunk_type` và `priority`, chia description dài thành đoạn nhỏ để retrieval truy xuất đúng phần người dùng hỏi thay vì đọc toàn bộ project/news.

`tai_lieu/p2/2.txt` là bài hoàn thiện code chunking và đánh giá point dữ liệu. Nội dung bài tập trung vào việc làm gọn chunking, tách chunk theo ngữ nghĩa nhỏ hơn, dùng metadata nền, thêm `chunk_id`, `chunk_type`, `priority`, chia text dài bằng `split_paragraphs()` và bỏ `heroSlides` khỏi pipeline vì loại dữ liệu này dễ gây nhiễu retrieval.

Tại thời điểm cập nhật sau `p2/2`, phần chunking trong code đã có helper metadata, helper chia đoạn, nhiều loại chunk nhỏ cho `projects`, `news`, `companyInfo`, các danh mục, phong cách nội thất và loại kiến trúc. File `ingestion/chunking/heroSlides.py` đã bị xoá và `ingestion/pipeline.py` không còn gọi `chunk_hero_slides()`.

`tai_lieu/p2/3.txt` là bài phân tích vấn đề của dense embedding hiện tại và lý do cần bổ sung sparse/keyword embedding. Nội dung bài giải thích dense embedding nắm ngữ nghĩa tổng thể nhưng có thể bỏ lỡ keyword quan trọng như địa điểm, con số, mức đầu tư hoặc loại công trình; hướng xử lý là tạo thêm biểu diễn sparse dựa trên token, vocabulary, document frequency, term frequency và inverse document frequency.

`tai_lieu/p2/4.txt` là bài code sparse embedding. Nội dung bài xây dựng file sparse embedder gồm bước token hóa text, tạo vocabulary, tính document frequency, fit theo danh sách text, tính IDF và encode từng text thành cấu trúc sparse gồm `indices` và `values`.

`tai_lieu/p2/5.txt` là bài code hybrid index. Nội dung bài thêm hướng build Qdrant point có cả dense vector và sparse vector, dùng `SparseEmbedder.encode_batch(texts)` để tạo sparse vector rồi lưu cùng dense embedding.

`tai_lieu/p2/6.txt` là bài lý thuyết BM25 trong retriever. Nội dung bài giải thích vì sao sparse embedder chỉ cho biết keyword trong document quan trọng thế nào, còn BM25 trả lời document có liên quan tới query không và liên quan bao nhiêu. Bài giải thích các thành phần IDF, TF, `k1`, `b`, độ dài document và độ dài trung bình document.

`tai_lieu/p2/7.txt` là bài code BM25 scorer. Nội dung bài tạo class `BM25`, tính average document length, tính score giữa query và từng document, rồi chuẩn bị dùng score này trong hybrid retriever.

`tai_lieu/p2/8.txt` là bài đưa BM25 score vào hybrid retriever. Nội dung bài giải thích việc lấy dư candidate bằng dense retrieval, tính BM25 score theo query/text, trộn điểm bằng `dense_weight` và `bm25_weight`, lưu thêm `dense_score` và `bm25_score` vào metadata, sort lại theo hybrid score và trả về `TOP_K` document.

`tai_lieu/p2/9.txt` là bài hoàn thiện reranking và context builder để chuẩn bị context cho LLM. Nội dung bài tạo base reranker, CrossEncoder model wrapper, CrossEncoder reranker để chấm điểm cặp query/document, sort/cắt top document, và `ContextBuilder` để ghép document thành context có giới hạn số document, giới hạn độ dài và separator.

`tai_lieu/p2/10.txt` là bài hoàn thiện chatbot với các cải tiến và sửa lỗi. Phần đã phản ánh trong code hiện tại gồm tạo `core/startup.py` để khởi tạo `SparseEmbedder`, `BM25` và `CrossEncoderReranker` từ corpus trong Qdrant; sửa `vectorstore/qdrant.py` để tạo collection kiểu hybrid có named vector `dense` và sparse vector `sparse` khi collection chưa tồn tại; sửa `vectorstore/upsert.py` để fit `SparseEmbedder`, gọi `init_sparse_embedder(...)`, build hybrid point bằng `build_hybrid_qdrant_points(...)` và upsert hybrid points; sửa `api/app.py` để gọi `initialize_rag_components()` trong lifespan startup; sửa `api/health.py` để trả trạng thái RAG components; và sửa `api/routes/chat.py` để dùng `hybrid_retrieve()`, BM25, reranker và rate limit in-memory.

Mã nguồn hiện tại đã có phần dense embedding, sparse embedding, hybrid index, BM25 scorer, hybrid retriever, reranking bằng CrossEncoder, context builder, schema `RetrievedDocument`, prompt template, legacy Ollama generator, OpenRouter generator bằng OpenAI Agents SDK, FastAPI backend và frontend Next.js. `backend/embedding/sparse_embedder.py` đã tồn tại và có code cho `tokenize()` cùng class `SparseEmbedder`. `backend/vectorstore/hybrid_index.py` đã có code build point với named vector `dense` và `sparse`, `backend/vectorstore/upsert.py` hiện đã gọi luồng build hybrid point, `backend/vectorstore/qdrant.py` hiện tạo collection hybrid khi collection chưa tồn tại, `backend/scoring/bm25.py` đã có class `BM25`, `backend/retrieval/hybrid_retriever.py` đã có hàm `hybrid_retrieve(query, bm25)`, `backend/reranking` đã có `BaseReranker`, `CrossEncoderModel` và `CrossEncoderReranker`, còn `backend/retrieval/context_builder.py` đã có class `ContextBuilder`. `backend/api/app.py` hiện gọi `initialize_rag_components()` lúc startup. Endpoint `POST /api/chat` hiện dùng hybrid retriever, BM25, reranker và `ContextBuilder`, nhưng vẫn gọi legacy `backend/llm/generator.py`. Endpoint `POST /api/chat/openai` hiện dùng hybrid retrieval + BM25 + reranker + `ContextBuilder` và vẫn gọi `backend/llm/generator_openai.py` (OpenRouter). Frontend hiện gọi `POST /api/chat/openai`. Người dùng đã từng chạy thành công `uv run python -m ingestion.pipeline` sau buổi 5, tạo collection `nmk_chatbot_collection` và upsert 450 chunks vào Qdrant theo schema cũ. Sau cập nhật `p2/10`, pipeline build/upsert hybrid points và đã chạy thành công: sau khi xoá collection cũ dense-only, collection `nmk_chatbot_collection` được tạo lại đúng schema hybrid (named vector `dense` + sparse vector `sparse`) với 450 points. `chat.py` ở thư mục gốc đã được xoá; luồng chat hiện nằm trong `backend/api/routes/chat.py` và `backend/api/routes/chat_openai.py`.

## Mục Tiêu Dự Án

Đây là dự án học Python RAG để xây dựng chatbot trả lời thông tin về công ty Nguyen Minh Khang Architects.

Dữ liệu raw hiện tại vẫn có bảng `heroSlides`, nhưng `backend/data/processed/heroSlides.json` không còn được sử dụng trong code chunking hoặc pipeline ingestion hiện tại.

Dự án hiện đi theo hướng RAG, không phải fine-tuning. Dữ liệu được xử lý thành các chunk có thể truy xuất, sau đó dùng làm ngữ cảnh cho LLM khi trả lời câu hỏi.

## Cấu Trúc Thư Mục Hiện Tại

Các thư mục chính hiện có:

- `backend`: runtime root của toàn bộ Python backend, gồm các folder liệt kê dưới đây; lệnh backend chạy từ `backend/`.
- `backend/config`: chứa cấu hình YAML cho ứng dụng và logging.
- `backend/core`: chứa mã dùng chung để đọc settings, cấu hình logging, schema dùng chung và startup helper cho BM25/reranker.
- `backend/api`: chứa FastAPI backend, health check, chat route legacy và chat route OpenRouter.
- `backend/data`: chứa dữ liệu gốc và dữ liệu đã tách theo bảng.
- `frontend`: chứa frontend Next.js, React, TypeScript và Tailwind CSS cho giao diện chat.
- `backend/ingestion`: chứa mã nạp dữ liệu, pipeline ingestion và xử lý dữ liệu đầu vào.
- `backend/ingestion/chunking`: chứa mã chunking theo từng bảng dữ liệu đang dùng; `heroSlides.py` đã bị xoá khỏi code chunking hiện tại.
- `backend/ingestion/helpers`: chứa helper tạo metadata và chia đoạn text.
- `backend/embedding`: chứa mã load model dense embedding, tạo embedding theo batch và sparse embedder dựa trên token/TF-IDF.
- `backend/vectorstore`: chứa code kết nối Qdrant, tạo collection hybrid khi collection chưa tồn tại, build point dense-only cũ, build point hybrid và upsert chunk vào Qdrant.
- `backend/retrieval`: chứa code truy vấn Qdrant bằng dense embedding query, code hybrid retriever có BM25 score và chuẩn hóa kết quả về `RetrievedDocument`.
- `backend/scoring`: chứa code tính điểm BM25 cho query/document.
- `backend/reranking`: chứa code rerank document bằng CrossEncoder trước khi build context cho LLM.
- `backend/llm`: chứa prompt template, legacy Ollama generator và OpenRouter generator dùng OpenAI Agents SDK.
- `backend/logs`: chứa file log của ứng dụng.
- `report`: chứa tài liệu báo cáo trạng thái dự án.
- `tai_lieu`: chứa phiên âm các buổi học.
- `backend/tests`: chứa automated tests cho luồng OpenRouter mới, không gọi API thật.
- `qdrant_storage`: chứa dữ liệu local do Qdrant Docker container tạo ra.

## Phần Đã Có Mã Nguồn

Sau refactor layout ngày 2026-08-04, toàn bộ path Python backend trong mục này nằm trong thư mục `backend/`, ví dụ `backend/core/settings_loader.py`.

`core/settings_loader.py` đã có hàm `load_settings()`. Hàm này đọc `config/settings.yaml`, nạp biến môi trường từ `.env`, sau đó ghi đè một số giá trị cấu hình bằng biến môi trường nếu các biến đó tồn tại.

`core/logging_setup.py` đã có hàm `setup_logging()`. Hàm này tạo thư mục `logs` nếu cần, đọc `config/logging.yaml` và áp dụng cấu hình logging bằng `logging.config.dictConfig`.

`core/schema.py` đã có dataclass `RetrievedDocument`. Schema này gồm `id`, `score`, `text` và `metadata`, đang được `retrieval/retriever.py` dùng để chuẩn hóa kết quả truy vấn từ Qdrant.

`core/startup.py` đã có các hàm `initialize_rag_components()`, `get_bm25()`, `get_reranker()` và `get_initialization_status()`. File này load corpus từ Qdrant bằng `client.scroll(...)`, fit `SparseEmbedder`, khởi tạo `BM25`, tính average document length, khởi tạo `CrossEncoderModel` và bọc bằng `CrossEncoderReranker`. Trạng thái hiện tại: `api/app.py` gọi `initialize_rag_components()` trong lifespan startup; `api/health.py` gọi `get_initialization_status()`; `api/routes/chat.py` gọi `get_bm25()` và `get_reranker()`. File phụ thuộc Qdrant đã có collection/points và có thể load CrossEncoder model thật khi `initialize_rag_components()` chạy.

`api/app.py` đã có FastAPI app. File này gọi `setup_logging()`, định nghĩa lifespan startup/shutdown, gọi `initialize_rag_components()` khi startup, cấu hình CORS, thêm middleware `track_response_time` để gắn header `X-Response-Time`, đăng ký `GET /`, `GET /health`, `POST /api/chat` và `POST /api/chat/openai`, đồng thời có block chạy Uvicorn khi dùng `uv run python -m api.app`. Block này hiện bind `0.0.0.0`, port `8000` và tắt `reload` để tránh WatchFiles theo dõi toàn repo và restart/kẹt startup khi Qdrant/log/cache thay đổi.

`api/health.py` đã có endpoint `GET /health`. Endpoint kiểm tra kết nối Qdrant, thử load embedding model, trả cấu hình LLM provider/model và trả trạng thái RAG components từ `core.startup.get_initialization_status()`. Health check này có thể load embedding model khi được gọi.

`api/routes/chat.py` đã có endpoint `POST /chat`. Vì `api/app.py` đăng ký router với prefix `/api`, endpoint đầy đủ là `POST /api/chat`. Route nhận `query` và `session_id`, kiểm tra rate limit in-memory theo IP, lấy BM25/reranker từ `core.startup`, gọi `hybrid_retrieve(question, bm25)`, rerank document nếu reranker sẵn sàng, build context bằng `ContextBuilder`, gọi `generate_answer(context, question)` từ legacy `llm/generator.py`, lưu session trong memory và trả `answer`, `sources`, `session_id`. Với cấu hình hiện tại `llm.provider: openrouter`, route này vẫn phụ thuộc điểm lưu ý là `llm/generator.py` chỉ hỗ trợ provider `ollama`.

`api/routes/chat_openai.py` đã có endpoint `POST /chat/openai`. Vì `api/app.py` đăng ký router với prefix `/api`, endpoint đầy đủ là `POST /api/chat/openai`. Route nhận `query` và `session_id`, kiểm tra rate limit in-memory theo IP, lấy BM25/reranker từ `core.startup`, rồi trả `StreamingResponse` media type `text/event-stream`. Trong stream, route gọi `hybrid_retrieve(question, bm25)`, rerank document nếu reranker sẵn sàng, build context bằng `ContextBuilder`, gọi `stream_answer_async(context, question)` từ `llm/generator_openai.py`, lưu session trong memory với full answer, và gửi các event SSE `meta` (session_id), nhiều `delta` (từng text delta), `sources`, `done` (answer + session_id); lỗi sau khi stream bắt đầu gửi event `error`. Lỗi trước khi stream bắt đầu vẫn dùng `HTTPException`: `400` query rỗng, `429` rate limit, `503` BM25 chưa khởi tạo. Case không có documents: stream `meta`, một `delta` câu không tìm thấy thông tin, `sources` rỗng, rồi `done`.

`ingestion/load_data.py` đã có hàm `load_data()`. Hàm này đọc file JSON gốc trong `data/raw`, lấy object `tables`, bỏ qua các bảng rỗng và ghi từng bảng có dữ liệu ra `data/processed/<ten_bang>.json`.

`ingestion/pipeline.py` đã có hàm `run_ingestion_pipeline()`. Hàm này gọi các hàm chunking cho architecture types, company info, interior styles, news categories, news, project categories và projects, gom `all_chunks`, rồi gọi `upsert_chunks(all_chunks)`. Sau `p2/2`, pipeline không còn import hoặc gọi `heroSlides.py`. Import trong pipeline đã được kiểm tra lại bằng `uv run` và hiện import được.

`ingestion/chunking` hiện có các module chunking cho nhiều bảng dữ liệu đã xử lý:

- `architectureTypes.py`: tạo chunk cho loại kiến trúc từ `architectureTypes.json`.
- `companyInfo.py`: tạo chunk tổng quan, mô tả và thông tin liên hệ công ty từ `companyInfo.json`; chunk `contact_info` hiện có câu mở đầu `Thông tin liên hệ của <tên công ty>` trước Hotline/Email/Địa chỉ để hỗ trợ query tự nhiên về liên hệ.
- `interiorStyles.py`: tạo chunk cho phong cách nội thất từ `interiorStyles.json`.
- `newCategories.py`: tạo chunk cho danh mục tin tức từ `newsCategories.json`.
- `news.py`: chuyển HTML tin tức sang text, chia nội dung thành đoạn và tạo chunk từ `news.json`.
- `projectCategories.py`: tạo chunk cho danh mục dự án từ `projectCategories.json`.
- `projects.py`: tạo nhiều loại chunk cho dự án từ `projects.json`, gồm overview, description, style, context, specs và media.

`ingestion/chunking/heroSlides.py` không còn tồn tại. Theo nội dung `tai_lieu/p2/2.txt`, hero slides bị loại khỏi pipeline vì có thể trộn lẫn nội dung trang chủ, dự án, tin tức và các phần trình bày khác, làm nhiễu retrieval nếu không xử lý riêng.

`ingestion/helpers/make_metadata.py` hiện có hàm `make_metadata()` để thêm `chunk_id` UUID và merge metadata. `ingestion/helpers/split_paragraphs.py` hiện có hàm `split_paragraphs()` để chia text dài thành các đoạn nhỏ. `ingestion/helpers/__init__.py` đang rỗng và chỉ đóng vai trò package marker.

`embedding/embedder.py` đã có hàm `get_model()` và `embed_texts()`. File này load `SentenceTransformer` theo cấu hình `embedding.model`, cache model trong biến module `_model`, tạo embedding đã normalize và trả về dạng list để lưu vào vector store.

`embedding/batch_embed.py` đã có hàm `batch_embed_texts()`. File này đọc `embedding.batch_size` từ settings, chia danh sách text thành batch, gọi `embed_texts()` cho từng batch và gộp kết quả embedding.

`embedding/sparse_embedder.py` đã có hàm `tokenize()` và class `SparseEmbedder`. `tokenize(text)` chuyển text về chữ thường, bỏ ký tự đặc biệt bằng regex và tách token bằng khoảng trắng. `SparseEmbedder` lưu `vocabulary`, `document_frequency` và `num_documents`; `fit(texts)` xây vocabulary và document frequency từ danh sách text; `encode(text)` trả sparse vector dạng dictionary gồm `indices` và `values`; `encode_batch(texts)` encode nhiều text bằng cách gọi `encode()` cho từng phần tử. File này hiện được `vectorstore/hybrid_index.py` dùng để build sparse vector, được `vectorstore/upsert.py` fit trên corpus chunk trước khi upsert hybrid points, được `core/startup.py` fit lại từ corpus Qdrant để khởi tạo BM25, và được `scoring/bm25.py` dùng cho tokenization, vocabulary, document frequency và document count.

`vectorstore/qdrant.py` đã có hàm `get_qdrant_client()` và `ensure_collection()`. File này đọc cấu hình Qdrant từ settings, tạo `QdrantClient`, kiểm tra kết nối bằng `get_collections()`, và tạo collection hybrid nếu collection chưa tồn tại. Collection mới dùng named vector `dense` với `VectorParams` và sparse vector `sparse` với `SparseVectorParams`. Trạng thái hiện tại: nếu collection `nmk_chatbot_collection` đã tồn tại với schema cũ, `ensure_collection()` chỉ log rồi trả về, không tự migrate schema.

`vectorstore/index.py` đã có hàm `build_qdrant_points()`. File này lấy text từ các chunk, gọi `embedding.embedder.embed_texts()` để tạo embedding, rồi build point dictionary gồm `id`, `vector` và `payload`.

`vectorstore/upsert.py` đã có hàm `upsert_chunks()`. File này lấy Qdrant client, đảm bảo collection tồn tại, fit `SparseEmbedder` trên toàn bộ `chunk["text"]`, gọi `init_sparse_embedder(...)`, gọi `build_hybrid_qdrant_points(chunks)` để tạo point có named vector `dense` và `sparse`, rồi gọi `client.upsert(...)`.

`vectorstore/hybrid_index.py` đã có hàm `init_sparse_embedder(embedder)` và `build_hybrid_qdrant_points(chunks)`. File này nhận `SparseEmbedder` đã fit sẵn, tạo dense embedding bằng `embed_texts(texts)`, tạo sparse embedding bằng `_sparse_embedder.encode_batch(texts)`, rồi build `PointStruct` có named vector `dense` và `sparse`. Trạng thái hiện tại: file đang được `vectorstore/upsert.py` gọi khi pipeline upsert chunks.

`retrieval/retriever.py` đã có hàm `retrieve(query)`. File này embedding câu hỏi bằng `embed_texts([query])`, truy vấn Qdrant bằng `client.query_points(...)`, lấy payload gồm `text` và metadata, rồi chuẩn hóa kết quả về `RetrievedDocument`. Sau buổi 7, module này đã import được vì `core/schema.py` đã có `RetrievedDocument`. Trạng thái hiện tại: không còn route nào gọi hàm `retrieve()`; file được giữ làm legacy dense-only.

`retrieval/hybrid_retriever.py` đã có hàm `hybrid_retrieve(query, bm25)`. File này embedding query thành dense vector, truy vấn Qdrant bằng named vector `dense` với `limit=TOP_K * 3`, tính `bm25.score(query, text)` cho từng payload text, rồi tính `hybrid_score = DENSE_WEIGHT * dense_score + BM25_WEIGHT * bm25_score`. Metadata trả về có thêm `dense_score` và `bm25_score`. Trạng thái hiện tại: cả hai endpoint `POST /api/chat` và `POST /api/chat/openai` hiện đều gọi file này.

`retrieval/context_builder.py` đã có class `ContextBuilder`. Class này nhận `max_documents`, `max_context_length` và `separator`; hàm `build(documents)` lấy tối đa số document cấu hình, bỏ qua document rỗng, cắt text nếu context vượt giới hạn độ dài, ghép các phần bằng separator và trả về chuỗi context. Trạng thái hiện tại: `ContextBuilder` được cả `api/routes/chat.py` và `api/routes/chat_openai.py` dùng để build context trước khi gọi generator.

`scoring/bm25.py` đã có class `BM25`. Class này nhận `SparseEmbedder` đã fit, đọc `vocabulary`, `document_frequency` và `num_documents`, có `compute_average_document_length(documents)` để tính độ dài document trung bình, `score(query, document)` để tính BM25 score giữa một query và một document, và `score_batch(query, documents)` để tính nhiều document. Trạng thái hiện tại: file được `core/startup.py` khởi tạo và được `retrieval/hybrid_retriever.py` dùng trong endpoint `POST /api/chat`.

`reranking/base.py` đã có class `BaseReranker` với method `rerank(query, documents, top_k=None)` raise `NotImplementedError`, đóng vai trò interface chung cho các reranker.

`reranking/models/cross_encoder.py` đã có class `CrossEncoderModel`. Class này load `sentence_transformers.CrossEncoder` theo `model_name` và `device`, rồi có method `score_batch(pairs)` để chấm điểm danh sách cặp `(query, document_text)`.

`reranking/reranker.py` đã có class `CrossEncoderReranker` kế thừa `BaseReranker`. Class này nhận `CrossEncoderModel`, tạo các cặp `(query, doc.text)`, gọi `score_batch(...)`, ghi `rerank_score` vào metadata từng document, sort document theo `rerank_score` giảm dần, cắt `top_k` nếu được truyền và trả về list `RetrievedDocument`. Trạng thái hiện tại: `core/startup.py` khởi tạo reranker; cả hai endpoint `POST /api/chat` và `POST /api/chat/openai` gọi `reranker.rerank(...)` nếu reranker sẵn sàng.

`llm/prompt.py` đã có `SYSTEM_PROMPT` và hàm `build_prompt(context, question)`. File này tạo prompt tiếng Việt cho chatbot NMK Architects, yêu cầu trả lời dựa trên context và không tự bịa thông tin ngoài dữ liệu.

`llm/generator.py` đã có hàm `generate_answer(context, question)`. File này được giữ nguyên làm legacy Ollama generator: kiểm tra context/question rỗng, gọi `build_prompt(...)`, rồi nếu `llm.provider` là `ollama` thì gọi `ollama.Client(...).chat(...)` để sinh câu trả lời. Với cấu hình `llm.provider: openrouter`, file này sẽ trả về thông báo nhà cung cấp mô hình không được hỗ trợ.

`llm/generator_openai.py` đã có hàm async `generate_answer_async(context, question)` và hàm streaming `stream_answer_async(context, question)`. File này kiểm tra input, yêu cầu `llm.provider` là `openrouter`, lấy API key OpenRouter từ settings đã nạp biến môi trường, build prompt bằng `build_prompt(...)`, tạo `AsyncOpenAI` với `base_url` OpenRouter, tạo `OpenAIChatCompletionsModel`, tạo `Agent` tên `nmk_chatbot`, truyền `temperature` và `max_tokens` qua `ModelSettings`, tắt OpenRouter reasoning bằng `extra_body={"reasoning": {"effort": "none"}}`, disable tracing bằng `set_tracing_disabled(True)`. `generate_answer_async()` gọi `await Runner.run(agent, prompt)` và trả full string; `stream_answer_async()` là async generator gọi `Runner.run_streamed(agent, prompt)` (không `await` vì SDK trả `RunResultStreaming` trực tiếp), lặp `async for event in result.stream_events()` và chỉ yield text delta khi event là `raw_response_event` và data là `ResponseTextDeltaEvent`. Cả hai hàm trả thông báo tiếng Việt khi thiếu API key, provider không hỗ trợ, timeout, lỗi kết nối hoặc lỗi API; không expose stack trace hoặc secret.

`frontend/app/page.tsx` đã render `ChatInterface`. `frontend/app/layout.tsx` đã khai báo layout gốc và metadata. `frontend/app/globals.css` đã cấu hình Tailwind và CSS variables nền/chữ.

`frontend/components/ChatInterface.tsx` đã có UI chat client-side. Component lưu messages, input, loading state và session id. Khi submit, component thêm user message và assistant placeholder rỗng, gọi `chatService.sendMessageStream(...)`, append delta vào assistant message cuối, gắn sources khi nhận event `sources`, cập nhật `sessionId` khi nhận `meta`/`done`, hiển thị lỗi tiếng Việt khi có lỗi. Nội dung assistant được render bằng `ReactMarkdown` + `remarkGfm` với component mapping cho `p`, `strong`, `ul`, `ol`, `li`, `a`, `code`, `pre`; vẫn hiển thị tối đa 3 hình ảnh từ metadata source nếu có. Bubble có `min-w-0 break-words` để nội dung không tràn. Trong lúc stream chỉ có một assistant row: assistant placeholder cuối cùng đang stream hiển thị 3 chấm loading ngay trong bubble và tự chuyển sang `ReactMarkdown` khi delta đầu tiên tới; không còn loading indicator riêng nên không có duplicate bot icon.

`frontend/lib/api.ts` đã có API client. File này dùng `fetch()` cho hàm `sendMessageStream(request, handlers)` gọi `POST /api/chat/openai`, đọc `response.body.getReader()`, decode bằng `TextDecoder`, buffer và parse SSE block tách bằng `\n\n`, gọi callback `onMeta`/`onDelta`/`onSources`/`onDone`/`onError`. File giữ types `ChatMessage`, `Source`, `ChatRequest`, `ChatResponse` và hàm `healthCheck()` gọi `GET /health` (dùng Axios). `healthCheck()` hiện được định nghĩa nhưng chưa được gọi trong UI; hàm `sendMessage` cũ dùng Axios đã bị bỏ vì endpoint giờ trả SSE.

`tests/conftest.py` đã thêm project root vào `sys.path` để pytest import được package local.

`tests/test_llm_generator_openai.py` đã test `generate_answer_async()` với context rỗng, question rỗng, thiếu API key OpenRouter và happy path monkeypatch `Runner.run`. File này thêm test cho `stream_answer_async()`: context rỗng, question rỗng, thiếu API key, happy path monkeypatch `Runner.run_streamed` bằng fake sync function trả `FakeStreamingResult` có `stream_events()` yield `ResponseTextDeltaEvent`, và test bỏ qua event không phải text delta. Các test không gọi OpenRouter thật.

`tests/test_api_chat_openai.py` đã test trực tiếp `chat_openai_endpoint()` với monkeypatch retrieval, generator streaming, BM25/reranker và rate limit. Vì endpoint giờ trả `StreamingResponse`, test consume `response.body_iterator` và parse SSE thành list event; happy path kiểm tra chuỗi event `meta` → nhiều `delta` → `sources` → `done`, session được lưu với full answer, case không có documents stream câu không tìm thấy với sources rỗng, case reranker được gọi với `top_k`, và các case 503/429 vẫn dùng `HTTPException`. Test không gọi Qdrant hoặc OpenRouter thật.

## File Rỗng Hiện Tại

Các file sau hiện tồn tại nhưng đang rỗng:

- `backend/api/__init__.py`
- `backend/core/__init__.py`
- `backend/embedding/__init__.py`
- `backend/ingestion/__init__.py`
- `backend/ingestion/chunking/__init__.py`
- `backend/ingestion/helpers/__init__.py`
- `backend/llm/__init__.py`
- `backend/reranking/__init__.py`
- `backend/reranking/models/__init__.py`
- `backend/retrieval/__init__.py`
- `backend/scoring/__init__.py`
- `backend/vectorstore/__init__.py`

Các file `__init__.py` rỗng hiện chỉ đóng vai trò package marker.

## Trạng Thái Chạy Hiện Tại

Các lệnh `uv run` trong mục này từng chạy từ root trước refactor layout ngày 2026-08-04. Sau refactor, tất cả lệnh Python backend chạy từ `backend/`, ví dụ `cd backend && uv run python -m ingestion.pipeline`.

Người dùng đã chạy Qdrant bằng Docker Compose và chạy thành công:

```bash
cd backend
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

Sau khi cập nhật code ở `p2/10`, kiểm tra tĩnh và import tối thiểu trước đó đã chạy thành công:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile core/startup.py vectorstore/qdrant.py vectorstore/upsert.py vectorstore/hybrid_index.py ingestion/pipeline.py retrieval/hybrid_retriever.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import importlib; importlib.import_module('ingestion.pipeline'); print('ingestion.pipeline import ok')"
```

Kết quả: các file compile được và `ingestion.pipeline` import được.

Người dùng đã chạy Qdrant bằng Docker Compose và chạy pipeline hybrid. Lần chạy đầu upsert bị Qdrant trả lỗi `Wrong input: Not existing vector name error: sparse` vì collection cũ dense-only chưa có vector name `sparse`. Sau khi xoá collection cũ, pipeline chạy lại thành công: collection `nmk_chatbot_collection` được tạo lại với named vector `dense` (384, cosine) và sparse vector `sparse`, 450 hybrid points được build và upsert, pipeline log `Upserted 450 chunks into the vector store`. `SparseEmbedder` fit trên 450 documents với vocabulary size 1486.

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

Sau khi triển khai streaming + Markdown (2026-08-04 17:33 +07), smoke test E2E đã chạy thành công với Qdrant, backend và OpenRouter:

- Backend startup khởi tạo đủ RAG components: BM25 ready, reranker ready, vocabulary size 1486, avg_document_length 48.84.
- `curl -N -X POST /api/chat/openai` trả `HTTP 200` với `content-type: text/event-stream; charset=utf-8`.
- Body stream gồm `event: meta` (1), `event: delta` (276 delta token-by-token), `event: sources` (1), `event: done` (1), không có `event: error`.
- `done` trả `answer` là full answer ghép từ các delta, có Markdown list (`*   **Hotline:** ...`) và `session_id` khớp với `meta`.

Trong lần smoke test đầu, `stream_answer_async()` bị lỗi `TypeError: object RunResultStreaming can't be used in 'await' expression` vì `Runner.run_streamed()` trong SDK 0.18.3 là sync function trả `RunResultStreaming` trực tiếp. Đã sửa code bỏ `await` và sửa fake test tương ứng sang sync function; sau đó tests pass và smoke test stream 276 delta thành công.

## Trạng Thái Dữ Liệu Hiện Tại

File dữ liệu gốc hiện có:

- `backend/data/raw/database_export_2026-01-14T02-32-14.json`
- `backend/data/raw/database_export_2026-01-23T02-02-46.json`

Hai file raw này đã được kiểm tra bằng `sha256sum` và có checksum giống nhau, nên nội dung hiện tại giống hệt nhau. Theo xác nhận của người dùng, các lần làm việc tiếp theo sẽ dùng file `database_export_2026-01-23T02-02-46.json`. Tuy nhiên code hiện tại trong `backend/ingestion/load_data.py` vẫn đang đọc trực tiếp `database_export_2026-01-14T02-32-14.json`; chưa có thay đổi code trong phiên cập nhật tài liệu này.

Mỗi file raw có object `tables` gồm 10 bảng:

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

Các file đã được tách trong `backend/data/processed`:

- `architectureTypes.json`
- `companyInfo.json`
- `heroSlides.json`
- `interiorStyles.json`
- `news.json`
- `newsCategories.json`
- `projectCategories.json`
- `projects.json`

`backend/data/processed/heroSlides.json` vẫn tồn tại vì được tách từ bảng có dữ liệu trong raw export, nhưng file này không còn được dùng bởi module chunking hoặc `backend/ingestion/pipeline.py`.

Qdrant local hiện có dữ liệu trong `qdrant_storage/` do Docker Compose mount. Collection `nmk_chatbot_collection` hiện có schema hybrid (named vector `dense` + sparse vector `sparse`) và chứa 450 hybrid points theo log chạy pipeline hybrid.

## Quyết Định Kỹ Thuật Hiện Tại

Dự án dùng Python và quản lý môi trường bằng `uv`.

File `pyproject.toml` yêu cầu Python `>=3.12`.

CodeGraph đã được cài ở máy local với phiên bản `1.5.0` và đã được init cho repo này. Sau lần kiểm tra gần nhất ngày 2026-08-04 19:44 +07 (sau refactor layout khi các folder backend đã move vào `backend/`), `codegraph status .` ghi nhận index hiện có 65 files, 538 nodes, 916 edges, DB size 1.38 MB, backend `node:sqlite` với full WAL, journal `wal`, và `Index is up to date`.

Thư mục `.codegraph/` là artifact local của CodeGraph, đã được thêm vào `.gitignore` và không nên commit.

Codex đã có MCP config cho CodeGraph trong cấu hình người dùng. Sau khi upgrade CodeGraph, session agent mới nên dùng binary mới; session đang chạy từ trước có thể vẫn giữ MCP process cũ cho tới khi restart. CLI `codegraph explore` hiện hoạt động trong repo này.

Theo tài liệu CodeGraph, auto-sync được bật mặc định sau `codegraph init`, nên graph được cập nhật khi file trong project thay đổi. Có thể chạy `codegraph sync` thủ công nếu cần đồng bộ lại.

Cấu hình chính được đặt trong `backend/config/settings.yaml`.

Cấu hình logging được đặt trong `backend/config/logging.yaml`.

Biến môi trường được nạp bằng `python-dotenv`. Tài liệu này không ghi nội dung `.env`.

Embedding model đang được cấu hình là `intfloat/multilingual-e5-small`.

Vector database đang được cấu hình là Qdrant, tên collection là `nmk_chatbot_collection`, distance là `cosine`, vector size là `384`.

Qdrant đang được chạy bằng Docker Compose từ `docker-compose.yml`, service tên `qdrant`, container name `qdrant_version_1`, REST API port `6333`, gRPC port `6334`, dashboard tại `http://localhost:6333/dashboard`.

Nhà cung cấp LLM trong settings đang là `openrouter`, tên model đang là `qwen/qwen3.5-9b`, temperature là `0.2`.

Code LLM legacy nằm trong `backend/llm/generator.py`, không còn file `backend/llm/llm.py` trong cây thư mục hiện tại. `backend/llm/generator.py` chỉ có nhánh gọi Ollama khi `llm.provider == "ollama"` và được giữ nguyên để so sánh/rollback.

Code LLM OpenRouter mới nằm trong `backend/llm/generator_openai.py`. File này dùng OpenAI Agents SDK và OpenAI Python SDK để gọi OpenRouter qua endpoint OpenAI-compatible. File hiện tắt reasoning tokens cho OpenRouter để tránh câu trả lời rỗng với model hiện tại. File có hai đường sinh câu trả lời: `generate_answer_async()` dùng `Runner.run()` trả full string, và `stream_answer_async()` dùng `Runner.run_streamed()` (sync, không `await`) yield từng text delta từ `stream_events()`.

Dữ liệu được xử lý theo hướng tách bảng, tạo chunk riêng theo từng nhóm dữ liệu đang dùng, tạo dense embedding theo batch, fit sparse embedder trên corpus chunk và build point hybrid dense+sparse để lưu vào Qdrant. Sau `p2/2`, `heroSlides.json` vẫn là dữ liệu processed nhưng không còn có module chunking và không còn nằm trong pipeline. Sau `p2/4`, repo có thêm `backend/embedding/sparse_embedder.py` để tạo sparse representation dạng `indices`/`values`. Sau `p2/5` tới `p2/8`, repo có thêm code hybrid index, BM25 scorer và hybrid retriever. Sau `p2/9`, repo có thêm folder `backend/reranking` và `backend/retrieval/context_builder.py`. Sau `p2/10`, `backend/vectorstore/upsert.py` đã chuyển sang build/upsert hybrid points, `backend/vectorstore/qdrant.py` tạo collection hybrid khi collection chưa tồn tại, `backend/core/startup.py` khởi tạo sparse embedder/BM25/reranker từ Qdrant lúc backend startup, và endpoint `POST /api/chat` dùng hybrid retrieval + reranker. `ContextBuilder` hiện được cả hai route chat dùng. Endpoint `POST /api/chat/openai` hiện dùng hybrid retrieval + BM25 + reranker + `ContextBuilder` và vẫn dùng OpenRouter; response của endpoint này là SSE stream `text/event-stream` với các event `meta`/`delta`/`sources`/`done`/`error` thay vì JSON một lần. Frontend hiện gọi endpoint OpenRouter qua `fetch` streaming và render Markdown live bằng `react-markdown` + `remark-gfm` (dependency mới đã cài trong `frontend/package.json`). Entrypoint `chat.py` ở thư mục gốc đã được xoá; backend hiện chạy qua `backend/api/app.py`.

Backend chạy bằng (từ `backend/`):

```bash
cd backend
uv run python -m api.app
```

Lệnh này hiện tắt Uvicorn `reload` trong `api/app.py` và bind `0.0.0.0:8000`.

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
