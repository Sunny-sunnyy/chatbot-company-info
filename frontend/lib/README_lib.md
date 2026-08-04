# README_lib

## Nhật Ký Cập Nhật

- 2026-08-04 17:33 +07 - Cập nhật `api.ts` sau khi chuyển sang streaming: thêm `sendMessageStream(request, handlers)` dùng `fetch()` gọi `POST /api/chat/openai`, đọc `response.body.getReader()`, decode bằng `TextDecoder`, buffer và parse SSE block tách bằng `\n\n`, gọi callback `onMeta`/`onDelta`/`onSources`/`onDone`/`onError`; bỏ hàm `sendMessage` cũ dùng Axios vì endpoint giờ trả SSE; giữ types `ChatMessage`, `Source`, `ChatRequest`, `ChatResponse`, `StreamHandlers` mới và `healthCheck()` dùng Axios.
- 2026-08-01 22:04 +07 - Cập nhật trạng thái `api.ts`: endpoint `/api/chat/openai` hiện là route OpenRouter có hybrid retrieval + BM25 + reranker + `ContextBuilder`.
- 2026-07-26 21:02 +07 - Tạo README cho thư mục `frontend/lib` sau buổi 7, đối chiếu với API client hiện tại.
- 2026-07-27 16:03 +07 - Cập nhật `api.ts` sau khi frontend chuyển sang gọi endpoint OpenRouter `POST /api/chat/openai` và bổ sung hướng dẫn đổi lại endpoint cũ.
- 2026-08-01 17:58 +07 - Đối chiếu lại sau p2 hoàn chỉnh: `api.ts` vẫn gọi `/api/chat/openai`; route này sau đó đã được cập nhật để dùng hybrid retrieval + BM25 + reranker + `ContextBuilder`.

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
- Định nghĩa interface `StreamHandlers` gồm `onMeta`, `onDelta`, `onSources`, `onDone`, `onError`.
- Export object `chatService` với hàm `sendMessageStream` và `healthCheck`.

Vai trò và luồng hoạt động:

- `api.ts` là lớp client mỏng để frontend gọi backend.
- `sendMessageStream(request, handlers)` gửi `fetch()` POST tới `${API_URL}/api/chat/openai` với JSON body gồm `query` và `session_id` tùy chọn; nếu response không ok, parse `detail` từ JSON error body nếu có rồi gọi `onError`; nếu ok, đọc `response.body.getReader()`, decode `Uint8Array` bằng `TextDecoder` với `{stream: true}`, gom vào buffer string và parse từng SSE block tách bằng `\n\n`, phân biệt event qua dòng `event:` và data qua dòng `data:`, rồi gọi callback tương ứng (`meta` → `onMeta`, `delta` → `onDelta`, `sources` → `onSources`, `done` → `onDone`, `error` → `onError`).
- `healthCheck()` gửi GET tới `${API_URL}/health` và trả `true` nếu status HTTP là `200`.
- Input chính của `sendMessageStream` là `ChatRequest` và `StreamHandlers`.
- Output là các callback được gọi theo từng SSE event; `done` kèm `answer` (full answer) và `session_id`.
- `ChatInterface.tsx` đang dùng `chatService.sendMessageStream(...)` để gửi câu hỏi và cập nhật message theo từng delta.
- Hàm `sendMessage` cũ dùng Axios đã bị bỏ vì endpoint `/api/chat/openai` giờ trả SSE stream thay vì JSON một lần; nếu muốn quay lại endpoint JSON legacy, cần thêm lại client Axios riêng (xem hướng dẫn trong `frontend/README_frontend.md`).

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

Endpoint `/api/chat` của backend hiện cũng dùng hybrid retrieval, BM25 và reranker, nhưng gọi legacy `llm/generator.py`. `api.ts` hiện gọi endpoint OpenRouter `/api/chat/openai`, route này cũng dùng hybrid retrieval, BM25, reranker và `ContextBuilder`.

## Cách Đổi Lại Endpoint Cũ

Nếu muốn frontend gọi lại route legacy, sửa file `frontend/lib/api.ts`. Lưu ý route legacy trả JSON `ChatResponse` một lần, không phải SSE, nên cần thay luồng `sendMessageStream` bằng client Axios gọi trực tiếp (hàm `sendMessage` cũ đã bị bỏ). Đổi URL trong `sendMessageStream` từ:

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
