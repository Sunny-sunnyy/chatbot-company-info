# README_tai_lieu

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 21:24 +07 - Bổ sung mô tả nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-25 18:42 +07 - Bổ sung mô tả phiên âm buổi 4 sau khi đối chiếu với mã nguồn hiện tại.
- 2026-07-26 12:23 +07 - Bổ sung mô tả phiên âm buổi 5 sau khi Qdrant Docker và pipeline ingestion chạy thành công.
- 2026-07-26 16:54 +07 - Bổ sung mô tả phiên âm buổi 6 sau khi đối chiếu với code retrieval, prompt và LLM generator hiện tại.
- 2026-07-26 21:02 +07 - Bổ sung mô tả phiên âm buổi 7 sau khi đối chiếu với code schema, API backend và frontend hiện tại.
- 2026-07-27 20:45 +07 - Cập nhật mô tả `workflow_backend_frontend.md` sau khi viết lại toàn bộ: thêm phần nền tảng FastAPI, chia nhỏ diagram, thêm hướng dẫn chuyển đổi router.
- 2026-07-29 20:56 +07 - Bổ sung mô tả phiên âm giai đoạn nâng cao `p2/2.txt` sau khi đối chiếu với code chunking hiện tại.
- 2026-07-30 10:54 +07 - Bổ sung mô tả phiên âm giai đoạn nâng cao `p2/3.txt` và `p2/4.txt`, đồng thời cập nhật danh sách file hiện có sau khi các ảnh tham khảo đã bị xoá.

## Nhiệm Vụ Của Thư Mục

Thư mục `tai_lieu` chứa phiên âm các buổi học trong khóa YouTube.

Các file này là tài liệu tham khảo để hiểu bối cảnh học tập và lý do dự án được xây dựng theo cấu trúc hiện tại.

## Các File Hiện Có

### `README_tai_lieu.md`

File này mô tả nhiệm vụ của thư mục `tai_lieu` và nhiệm vụ hiện tại của từng file tài liệu trong thư mục.

### `1.txt`

Phiên âm buổi 1.

Nội dung chính đã dùng để cập nhật tài liệu:

- Giới thiệu bài toán chatbot RAG.
- Giới thiệu luồng xử lý từ dữ liệu gốc tới vector store.
- Giới thiệu các thư mục chính của dự án.
- Giới thiệu vai trò của config, logging, ingestion, chunking, embedding, vector store, retrieval, LLM và chat entrypoint.

### `2.txt`

Phiên âm buổi 2.

Nội dung chính đã dùng để cập nhật tài liệu:

- Viết phần đọc settings.
- Viết phần setup logging.
- Đọc file JSON gốc.
- Tách dữ liệu theo từng bảng.
- Ghi dữ liệu đã tách vào `data/processed`.
- Bắt đầu viết chunking cho `architectureTypes`.

### `3.txt`

File phiên âm buổi 3 hiện có trong thư mục.

### `4.txt`

Phiên âm buổi 4.

Nội dung chính đã dùng để cập nhật tài liệu:

- Giải thích embedding là bước chuyển text thành vector.
- Viết phần load `SentenceTransformer` và cache model trong biến global.
- Viết phần encode danh sách text và batch embedding.
- Trình bày ý tưởng kết nối Qdrant bằng client.
- Trình bày cách đảm bảo collection tồn tại.
- Trình bày cách build point từ chunk và embedding.
- Trình bày cách upsert point vào vector store.

### `5.txt`

Phiên âm buổi 5.

Nội dung chính đã dùng để cập nhật tài liệu:

- Bổ sung các file `__init__.py` cho những folder Python.
- Bổ sung dependency cần thiết cho Qdrant, BeautifulSoup, SentenceTransformer, Ollama và YAML.
- Tạo `docker-compose.yml` để chạy Qdrant local.
- Chạy Qdrant bằng Docker Compose.
- Chạy pipeline ingestion để upsert chunk vào Qdrant.
- Kiểm tra collection và point trong Qdrant dashboard.

### `6.txt`

Phiên âm buổi 6.

Nội dung chính đã dùng để cập nhật tài liệu:

- Viết retriever để nhận query, embedding query và truy vấn Qdrant.
- Chuẩn hóa kết quả truy vấn về schema `RetrievedDocument`.
- Viết prompt template gồm system prompt, context, question và yêu cầu trả lời bằng tiếng Việt dựa trên context.
- Viết generator nhận context/question, build prompt và gọi Ollama để sinh câu trả lời.
- Ghi nhận tại thời điểm cập nhật sau buổi 6 rằng `core/schema.py` và `chat.py` vẫn rỗng, nên luồng retrieval/chat chưa chạy end-to-end ở thời điểm đó.

### `7.txt`

Phiên âm buổi 7.

Nội dung chính đã dùng để cập nhật tài liệu:

- Nối retrieval và generator thành luồng chat nhận question, truy xuất document, build context và sinh answer.
- Tạo schema `RetrievedDocument` để chuẩn hóa document truy xuất.
- Tạo FastAPI backend gồm app chính, health endpoint và chat endpoint.
- Tạo frontend Next.js để gửi câu hỏi tới backend và hiển thị câu trả lời.
- Ghi nhận bảy buổi đầu là giai đoạn 1 của dự án.
- Ghi nhận trong repo hiện tại `llm/generator.py` vẫn chưa được sửa cho provider `openrouter`.

### `p2/`

Thư mục này chứa transcript của giai đoạn nâng cao.

### `p2/0.txt`

Phiên âm bài giới thiệu giai đoạn nâng cao.

Nội dung chính đã dùng để cập nhật tài liệu:

- Giới thiệu mục tiêu cải tiến chatbot sau giai đoạn 1.
- Nêu các hướng cải tiến chunking, embedding, vector store, retrieval, LLM và trải nghiệm chat.
- Ghi rõ đây là định hướng học tập, không tự động đồng nghĩa với code đã triển khai nếu repo chưa có thay đổi tương ứng.

### `p2/2.txt`

Phiên âm bài 2 giai đoạn nâng cao.

Nội dung chính đã dùng để cập nhật tài liệu:

- Làm lại chunking theo hướng nhỏ hơn và rõ ngữ nghĩa hơn.
- Dùng metadata nền cho nhiều chunk cùng một bản ghi.
- Thêm `chunk_id`, `chunk_type` và `priority` vào metadata thông qua helper.
- Dùng `split_paragraphs()` để chia text dài cho news/project khi cần.
- Bỏ `heroSlides` khỏi pipeline vì dữ liệu hero slide có thể gây nhiễu retrieval.
- Đối chiếu với code hiện tại cho thấy `ingestion/chunking/heroSlides.py` đã bị xoá và `ingestion/pipeline.py` không còn gọi hero slides.

### `p2/3.txt`

Phiên âm bài 3 giai đoạn nâng cao.

Nội dung chính đã dùng để cập nhật tài liệu:

- Phân tích vấn đề của dense embedding hiện tại: dense embedding nắm ngữ nghĩa tổng thể nhưng có thể bỏ lỡ keyword quan trọng.
- Nêu ví dụ các keyword quan trọng trong bài toán RAG như địa điểm, con số, diện tích, mức đầu tư hoặc loại công trình.
- Giới thiệu hướng bổ sung sparse/keyword embedding chạy song song với dense embedding.
- Giải thích các khái niệm `document frequency`, `term frequency`, `vocabulary` và `inverse document frequency`.
- Ghi rõ nội dung bài này là nền tảng lý thuyết cho sparse embedding; trạng thái code thật được xác nhận qua `embedding/sparse_embedder.py`.

### `p2/4.txt`

Phiên âm bài 4 giai đoạn nâng cao.

Nội dung chính đã dùng để cập nhật tài liệu:

- Code sparse embedder để tạo biểu diễn sparse song song với dense embedding.
- Viết bước token hóa text: chuyển chữ thường, bỏ ký tự đặc biệt bằng regex và tách token.
- Khởi tạo `vocabulary`, `document_frequency` và `num_documents`.
- Fit sparse embedder trên danh sách text để tạo vocabulary và document frequency.
- Tính IDF bằng công thức `log((num_documents + 1) / (document_frequency + 1)) + 1`.
- Encode text thành dictionary gồm `indices` và `values`.
- Đối chiếu với code hiện tại cho thấy `embedding/sparse_embedder.py` đã có `tokenize()` và class `SparseEmbedder`, nhưng vector store và retrieval hiện chưa dùng sparse embedding.

### Các file transcript khác trong `p2/`

Các file `p2/1.txt`, `p2/5.txt`, `p2/6.txt`, `p2/7.txt`, `p2/8.txt`, `p2/9.txt` và `p2/10.txt` hiện tồn tại trong thư mục.

Các file này không được đọc trong phiên cập nhật sau `p2/4.txt` và không được dùng để ghi nhận trạng thái code hiện tại.

Hiện tại thư mục `tai_lieu` không còn file ảnh `.png`. Các file ảnh tham khảo cũ như `anh1.png`, `anh2.png`, `anh3.png` và `bug1.png` không còn tồn tại trong cây thư mục hiện tại.

### `workflow_backend_frontend.md`

File giải thích luồng hoạt động backend-frontend bằng Mermaid diagram, chia 3 phần:

**Phần A — Kiến Thức Nền Tảng:** Web server, API, REST API, FastAPI, Uvicorn, Router (APIRouter), Pydantic Request/Response model, CORS, async/await. Mỗi khái niệm có định nghĩa, ví dụ và chỉ ra code thực tế trong dự án.

**Phần B — Diagram Kiến Trúc & Luồng (8 diagram nhỏ):**
- B1: Tổng quan 3 tầng (Frontend - Backend - Dịch vụ ngoài)
- B2: Bên trong Backend — App và Router
- B3: Luồng nạp cấu hình từ settings.yaml + .env
- B4: Khởi động Backend từng bước
- B5a-B5c: Xử lý câu hỏi chia 3 giai đoạn (Frontend→Route, Retrieval, Generation)
- B6: Quan hệ file trong tầng api/
- B7: Quan hệ file trong tầng llm/
- B8: Tổng kết luồng dữ liệu 6 bước

**Phần C — Hướng Dẫn Chuyển Đổi Router:**
- Cách 1: Chỉ sửa frontend (đổi endpoint)
- Cách 2: Đổi cả cấu hình LLM provider + frontend
- Kiểm tra sau khi chuyển đổi
- Bảng tổng kết khi nào dùng route nào

## Cách Hoạt Động Hiện Tại

Tài liệu trạng thái hiện tại đã được cập nhật sau khi đọc buổi 7 theo yêu cầu, đồng thời đối chiếu với mã nguồn hiện có.

Khi cập nhật sau các buổi học tiếp theo, cần đọc phiên âm tương ứng và đối chiếu với mã nguồn thực tế.

## Ghi Chú Kỹ Thuật

Phiên âm có thể có lỗi nhận dạng giọng nói. Khi viết tài liệu, thuật ngữ kỹ thuật nên được ghi đúng theo cách dùng phổ biến, ví dụ: RAG, LLM, chunking, embedding, vector store, Qdrant, logging và settings.
