# README_report

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 20:31 +07 - Bổ sung mô tả file `Agent_session_prompt.md`.
- 2026-07-25 17:23 +07 - Cập nhật mô tả `Project_status.md` theo snapshot hiện tại của repo.
- 2026-07-25 17:37 +07 - Cập nhật mô tả `Agent_session_prompt.md` sau khi bổ sung hướng dẫn sử dụng CodeGraph cho coding agent.
- 2026-07-25 18:42 +07 - Cập nhật mô tả `Project_status.md` sau khi audit trạng thái dự án theo buổi 4.
- 2026-07-25 20:22 +07 - Cập nhật mô tả `Project_status.md` và `Agent_session_prompt.md` sau khi bổ sung chuẩn giải thích vai trò file mã nguồn trong README.
- 2026-07-26 12:23 +07 - Cập nhật mô tả `Project_status.md` sau buổi 5: Qdrant Docker và pipeline ingestion đã chạy thành công.
- 2026-07-26 16:54 +07 - Cập nhật mô tả `Project_status.md` sau buổi 6: retrieval, prompt template và LLM generator đã có code bước đầu.
- 2026-07-26 21:02 +07 - Cập nhật mô tả `Project_status.md` sau buổi 7: schema, FastAPI backend và frontend Next.js đã có code bước đầu.
- 2026-07-26 21:16 +07 - Cập nhật mô tả `Project_status.md` sau khi `chat.py` ở thư mục gốc được xoá.
- 2026-07-27 16:03 +07 - Cập nhật mô tả `Project_status.md` sau khi thêm luồng OpenRouter isolated path, frontend gọi endpoint mới và automated tests liên quan.
- 2026-07-27 17:04 +07 - Cập nhật mô tả `Project_status.md` sau khi xử lý lỗi `final_output` rỗng bằng cách tắt OpenRouter reasoning.
- 2026-07-27 17:13 +07 - Cập nhật mô tả `Project_status.md` sau khi `api/app.py` chuyển sang chạy Uvicorn không reload khi dùng `uv run python -m api.app`.
- 2026-07-29 10:28 +07 - Cập nhật mô tả `Project_status.md` và `Agent_session_prompt.md` sau khi bắt đầu giai đoạn nâng cao trên branch `UpdateV2` theo `tai_lieu/p2/0.txt`.
- 2026-07-29 20:56 +07 - Cập nhật mô tả `Project_status.md` sau `tai_lieu/p2/2.txt`: chunking nâng cao, bỏ `heroSlides.py` khỏi pipeline và kiểm tra số chunk hiện tại.
- 2026-07-30 10:54 +07 - Cập nhật mô tả `Project_status.md` sau `tai_lieu/p2/3.txt` và `tai_lieu/p2/4.txt`: sparse embedding, dữ liệu raw mới trùng nội dung với raw cũ, `heroSlides.json` không còn dùng trong pipeline và trạng thái CodeGraph mới nhất.
- 2026-07-30 12:20 +07 - Cập nhật mô tả `Project_status.md` sau `tai_lieu/p2/5.txt`, `tai_lieu/p2/6.txt` và `tai_lieu/p2/7.txt`: hybrid index, BM25 scorer, hybrid retriever và trạng thái chưa nối vào pipeline/API.
- 2026-07-31 17:07 +07 - Cập nhật mô tả `Project_status.md` sau `tai_lieu/p2/8.txt` và `tai_lieu/p2/9.txt`: hybrid retriever có BM25, folder `reranking`, `retrieval/context_builder.py` và trạng thái chưa nối vào API.

## Nhiệm Vụ Của Thư Mục

Thư mục `report` chứa tài liệu báo cáo trạng thái dự án và prompt hướng dẫn coding agent khi tiếp tục làm việc với repo.

## Các File Hiện Có

### `Project_status.md`

File này ghi snapshot mới nhất của dự án tại thời điểm kiểm tra.

Nội dung hiện có:

- Mốc học hiện tại.
- Mục tiêu dự án.
- Cấu trúc thư mục hiện tại.
- Phần đã có mã nguồn.
- Phần chưa được phát triển.
- Trạng thái chạy hiện tại của pipeline và vector store.
- Trạng thái dữ liệu hiện tại.
- Quyết định kỹ thuật hiện tại.
- Trạng thái Docker Compose cho Qdrant local.
- Trạng thái code retrieval, prompt template và LLM generator qua buổi 6 và buổi 7.
- Trạng thái schema `RetrievedDocument`, FastAPI backend và frontend Next.js sau buổi 7.
- Ghi chú `chat.py` ở thư mục gốc đã được xoá; luồng chat hiện nằm trong `api/routes/chat.py`.
- Ghi chú `llm/generator.py` được giữ nguyên làm legacy Ollama generator.
- Trạng thái `llm/generator_openai.py` dùng OpenAI Agents SDK với OpenRouter.
- Trạng thái endpoint mới `POST /api/chat/openai`.
- Trạng thái frontend hiện gọi endpoint OpenRouter mới và có hướng dẫn đổi lại endpoint cũ trong README frontend.
- Trạng thái automated tests mới trong thư mục `tests`.
- Trạng thái tắt OpenRouter reasoning trong `llm/generator_openai.py`.
- Trạng thái `uv run python -m api.app` không còn bật Uvicorn reload.
- Chuẩn README hiện tại cho các folder có file Python thật.
- Mốc bắt đầu giai đoạn nâng cao trên branch `UpdateV2` theo bài giới thiệu `tai_lieu/p2/0.txt`, đồng thời phân biệt rõ nội dung định hướng với trạng thái code đã triển khai.
- Mốc sau `tai_lieu/p2/2.txt`: code chunking hiện đã bỏ `heroSlides.py`, pipeline không còn gọi hero slides, các chunk còn lại dùng metadata có `chunk_id`, `chunk_type` và `priority`, và kiểm tra trực tiếp các hàm chunking hiện tạo tổng cộng 450 chunks trước khi upsert.
- Mốc sau `tai_lieu/p2/3.txt` và `tai_lieu/p2/4.txt`: repo có `embedding/sparse_embedder.py` với `tokenize()` và `SparseEmbedder`.
- Mốc sau `tai_lieu/p2/5.txt`, `tai_lieu/p2/6.txt` và `tai_lieu/p2/7.txt`: repo có `vectorstore/hybrid_index.py`, `scoring/bm25.py` và `retrieval/hybrid_retriever.py`; pipeline và API hiện vẫn chưa chuyển sang hybrid.
- Mốc sau `tai_lieu/p2/8.txt` và `tai_lieu/p2/9.txt`: repo có `retrieval/hybrid_retriever.py` trộn dense score với BM25 score, folder `reranking` với `BaseReranker`, `CrossEncoderModel`, `CrossEncoderReranker`, và `retrieval/context_builder.py`; API hiện vẫn chưa gọi các module này.
- Trạng thái dữ liệu raw hiện có hai file export giống hệt nhau theo checksum; từ các lần làm việc tiếp theo người dùng muốn dùng `database_export_2026-01-23T02-02-46.json`, trong khi code hiện tại vẫn đọc file ngày `2026-01-14`.
- Trạng thái CodeGraph mới nhất: CLI `1.5.0`, index `up to date`, 62 files, 436 nodes, 674 edges, backend `node:sqlite` full WAL.

### `README_report.md`

File này mô tả chính thư mục `report` và trạng thái hiện tại của từng file trong thư mục.

### `Agent_session_prompt.md`

File này chứa prompt có thể copy sang coding agent trong session mới.

Nội dung file hướng dẫn agent đọc đúng tài liệu ngữ cảnh, đọc transcript đúng buổi học được yêu cầu, đối chiếu code với README theo folder, cập nhật `Project_status.md`, cập nhật README khi lệch trạng thái thật, không bịa đặt chức năng chưa có trong mã nguồn, giải thích vai trò/hàm/luồng chính của file mã nguồn đã có code, ghi rõ file rỗng là chưa phát triển, và sử dụng CodeGraph đúng cách khi cần hiểu flow hoặc quan hệ symbol trong code.

File này hiện cũng ghi rõ cách đọc transcript giai đoạn nâng cao trong `tai_lieu/p2/<so_buoi>.txt` khi người dùng yêu cầu.

## Cách Hoạt Động Hiện Tại

Tài liệu trong thư mục này dùng để giúp người học hoặc coding agent hiểu trạng thái dự án tại một thời điểm cụ thể.

Các file markdown trong dự án đang dùng mục `Nhật Ký Cập Nhật` để ghi thời gian cập nhật theo giờ Việt Nam.

## Ghi Chú Kỹ Thuật

Tài liệu trong thư mục này không chứa secret và không ghi nội dung `.env`.
