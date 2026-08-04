# README_docker

## Nhật Ký Cập Nhật

- 2026-07-26 12:23 +07 - Tạo tài liệu hướng dẫn chạy Qdrant bằng Docker Compose sau khi hoàn thành buổi 5 và upsert dữ liệu thành công.
- 2026-08-04 19:44 +07 - Cập nhật sau refactor layout: lệnh ingestion chạy từ `backend/`; `qdrant_storage/` và `docker-compose.yml` vẫn nằm ở root kể cả khi code backend đã chuyển vào `backend/`.

## Nhiệm Vụ Của File

File này ghi lại cách dùng Docker Compose để chạy Qdrant local cho dự án RAG chatbot.

Qdrant được dùng làm vector database để lưu các point được tạo từ chunk và embedding.

## File Docker Liên Quan

### `docker-compose.yml`

File này khai báo service `qdrant`.

Cấu hình hiện tại:

- Image: `qdrant/qdrant:latest`
- Container name: `qdrant_version_1`
- REST API port: `6333`
- gRPC port: `6334`
- Storage local: `./qdrant_storage:/qdrant/storage`
- Network: `chatbot-network`
- Restart policy: `unless-stopped`

Docker Compose bản mới có thể cảnh báo `version is obsolete` nếu file còn khai báo `version: '3.8'`. Cảnh báo này không làm Qdrant lỗi.

### `qdrant_storage/`

Thư mục này được Docker tạo khi chạy Qdrant.

Đây là nơi lưu dữ liệu local của Qdrant, bao gồm collection và point đã upsert. Không xóa thư mục này nếu muốn giữ dữ liệu vector store.

`qdrant_storage/` vẫn nằm ở root workspace kể cả sau refactor layout khi code backend đã chuyển vào `backend/`. Mount trong `docker-compose.yml` vẫn là `./qdrant_storage:/qdrant/storage`.

## Lệnh Chạy Qdrant

Chạy từ thư mục gốc dự án:

```bash
cd /home/hieu0606sunny/llm_rag
docker compose up -d qdrant
```

Vì hiện tại `docker-compose.yml` chỉ có một service, lệnh sau cũng cho kết quả tương đương:

```bash
docker compose up -d
```

## Kiểm Tra Trạng Thái

```bash
docker compose ps
```

Khi Qdrant chạy đúng, service `qdrant` sẽ có trạng thái `Up` và expose port `6333-6334`.

Có thể mở dashboard tại:

```text
http://localhost:6333/dashboard
```

Có thể kiểm tra API collections bằng:

```bash
curl http://localhost:6333/collections
```

## Dừng Và Chạy Lại

Dừng container nhưng giữ container, network và dữ liệu:

```bash
docker compose stop qdrant
```

Chạy lại container đã dừng:

```bash
docker compose start qdrant
```

Dừng và xóa container/network do Compose tạo:

```bash
docker compose down
```

Sau khi `down`, có thể bật lại bằng:

```bash
docker compose up -d qdrant
```

Với cấu hình hiện tại, dữ liệu vẫn được giữ nếu thư mục `qdrant_storage/` không bị xóa.

## Lệnh Ingestion Sau Khi Qdrant Chạy

Sau khi Qdrant đã chạy, có thể chạy pipeline bằng `uv` từ `backend/`:

```bash
cd backend
uv run python -m ingestion.pipeline
```

Trạng thái đã kiểm chứng sau buổi 5:

- Qdrant container chạy thành công.
- Pipeline kết nối được Qdrant qua `http://localhost:6333`.
- Collection `nmk_chatbot_collection` được tạo thành công.
- Pipeline đã upsert 450 points vào Qdrant.

## Lưu Ý An Toàn Dữ Liệu

Không xóa thư mục này nếu muốn giữ collection và point đã upsert:

```text
qdrant_storage/
```

Không dùng lệnh xóa dữ liệu Docker hoặc xóa thư mục storage nếu chưa chủ động muốn reset vector database.
