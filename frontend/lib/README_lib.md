# README_lib

## Nhật Ký Cập Nhật

- 2026-07-26 21:02 +07 - Tạo README cho thư mục `frontend/lib` sau buổi 7, đối chiếu với API client hiện tại.
- 2026-07-27 16:03 +07 - Cập nhật `api.ts` sau khi frontend chuyển sang gọi endpoint OpenRouter `POST /api/chat/openai` và bổ sung hướng dẫn đổi lại endpoint cũ.

## Nhiệm Vụ Của Thư Mục

Thư mục `frontend/lib` chứa helper và client code dùng chung cho frontend.

Hiện tại thư mục này có API client gọi backend FastAPI.

## File Tài Liệu Trong Thư Mục

### `README_lib.md`

File này mô tả nhiệm vụ của thư mục `frontend/lib` và trạng thái từng file mã nguồn trong thư mục.

## Nhiệm Vụ Các File Mã Nguồn

### `api.ts`

File này đã có mã nguồn.

Nội dung chính:

- Import `axios`.
- Xác định `API_URL` từ `NEXT_PUBLIC_API_URL`, mặc định `http://localhost:8000`.
- Định nghĩa interface `ChatMessage`.
- Định nghĩa interface `Source`.
- Định nghĩa interface `ChatRequest`.
- Định nghĩa interface `ChatResponse`.
- Export object `chatService` với hàm `sendMessage` và `healthCheck`.

Vai trò và luồng hoạt động:

- `api.ts` là lớp client mỏng để frontend gọi backend.
- `sendMessage(request)` gửi POST tới `${API_URL}/api/chat/openai` với JSON body gồm `query` và `session_id` tùy chọn.
- `healthCheck()` gửi GET tới `${API_URL}/health` và trả `true` nếu status HTTP là `200`.
- Input chính của `sendMessage` là `ChatRequest`.
- Output chính của `sendMessage` là `ChatResponse` gồm `answer`, `sources` và `session_id`.
- `ChatInterface.tsx` đang dùng `chatService.sendMessage(...)` để gửi câu hỏi người dùng.

## Cách Hoạt Động Hiện Tại

Nếu không có biến môi trường `NEXT_PUBLIC_API_URL`, frontend gọi backend tại:

```text
http://localhost:8000
```

Endpoint được gọi:

```text
POST /api/chat/openai
GET /health
```

## Cách Đổi Lại Endpoint Cũ

Nếu muốn frontend gọi lại route legacy, sửa file `frontend/lib/api.ts`.

Đổi dòng endpoint trong `chatService.sendMessage(...)` từ:

```ts
`${API_URL}/api/chat/openai`
```

về:

```ts
`${API_URL}/api/chat`
```

Sau khi sửa, chạy lại hoặc để Next.js dev server hot reload:

```bash
npm run dev
```

## Ghi Chú Kỹ Thuật

`healthCheck()` hiện được định nghĩa nhưng chưa được gọi trong `ChatInterface.tsx`.
