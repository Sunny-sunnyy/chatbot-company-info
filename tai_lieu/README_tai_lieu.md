# README_tai_lieu

## Nhật Ký Cập Nhật

- 2026-07-24 20:06 +07 - Tạo tài liệu đầu tiên cho thư mục sau khi đọc phiên âm buổi 1, buổi 2 và kiểm tra trạng thái hiện tại.
- 2026-07-24 20:18 +07 - Chuyển toàn bộ nội dung sang tiếng Việt có dấu và chỉ mô tả trạng thái hiện có.
- 2026-07-24 21:24 +07 - Bổ sung mô tả nhiệm vụ hiện tại của từng file trong thư mục.
- 2026-07-25 18:42 +07 - Bổ sung mô tả phiên âm buổi 4 sau khi đối chiếu với mã nguồn hiện tại.
- 2026-07-26 12:23 +07 - Bổ sung mô tả phiên âm buổi 5 sau khi Qdrant Docker và pipeline ingestion chạy thành công.

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

File phiên âm buổi 6 hiện có trong thư mục.

### `7.txt`

File phiên âm buổi 7 hiện có trong thư mục.

### `anh1.png`

File ảnh tham khảo hiện có trong thư mục.

Tính tới thời điểm cập nhật này, ảnh này được dùng làm tài liệu tham khảo cho việc viết `ingestion/chunking/heroSlides.py`.

### `anh2.png`

File ảnh tham khảo hiện có trong thư mục.

Tính tới thời điểm cập nhật này, ảnh này được dùng làm tài liệu tham khảo cho việc viết `ingestion/chunking/heroSlides.py`.

### `anh3.png`

File ảnh tham khảo hiện có trong thư mục.

Tính tới thời điểm cập nhật này, ảnh này được dùng làm tài liệu tham khảo cho việc viết `ingestion/chunking/heroSlides.py`.

## Cách Hoạt Động Hiện Tại

Tài liệu trạng thái hiện tại đã được cập nhật sau khi đọc buổi 5 theo yêu cầu, đồng thời đối chiếu với mã nguồn hiện có và kết quả chạy pipeline thực tế.

Khi cập nhật sau các buổi học tiếp theo, cần đọc phiên âm tương ứng và đối chiếu với mã nguồn thực tế.

## Ghi Chú Kỹ Thuật

Phiên âm có thể có lỗi nhận dạng giọng nói. Khi viết tài liệu, thuật ngữ kỹ thuật nên được ghi đúng theo cách dùng phổ biến, ví dụ: RAG, LLM, chunking, embedding, vector store, Qdrant, logging và settings.
