# README_frontend

## Nhật Ký Cập Nhật

- 2026-07-26 21:02 +07 - Tạo README tổng quan cho thư mục `frontend` sau buổi 7, đối chiếu với mã nguồn Next.js hiện tại và kết quả build frontend.
- 2026-07-27 16:03 +07 - Cập nhật trạng thái frontend sau khi `frontend/lib/api.ts` chuyển sang endpoint OpenRouter `POST /api/chat/openai` và ghi hướng dẫn đổi lại endpoint cũ.
- 2026-08-01 17:58 +07 - Đối chiếu lại sau p2 hoàn chỉnh: frontend vẫn gọi `/api/chat/openai`, chưa chuyển sang endpoint `/api/chat` hybrid/reranker.

## Nhiệm Vụ Của Thư Mục

Thư mục `frontend` chứa frontend Next.js cho chatbot NMK.

Frontend hiện hiển thị giao diện chat, gửi câu hỏi tới FastAPI backend qua Axios ở endpoint OpenRouter, nhận câu trả lời và hiển thị sources kèm hình ảnh nếu metadata có URL hình ảnh.

## Các File Hiện Có

### `README_frontend.md`

File này mô tả nhiệm vụ của thư mục `frontend`, trạng thái từng file cấu hình và liên kết tới README của các thư mục con.

### `README.md`

File này là README ngắn trong thư mục frontend, ghi lệnh cài đặt và chạy frontend.

### `.gitignore`

File này khai báo các artifact frontend không đưa vào Git, ví dụ dependency local, build output và environment local của Next.js.

### `.next/`

Thư mục này được Next.js tạo sau khi chạy build hoặc dev server.

Trạng thái hiện tại: thư mục tồn tại local sau khi chạy `npm run build` và được `.gitignore` ignore.

### `node_modules/`

Thư mục này chứa dependency frontend đã cài local bằng npm.

Trạng thái hiện tại: thư mục tồn tại local và được `.gitignore` ignore.

### `package.json`

File này khai báo project frontend, scripts và dependency.

Scripts hiện có:

- `dev`: chạy Next.js development server.
- `build`: build production.
- `start`: chạy bản production đã build.
- `lint`: chạy lệnh lint được khai báo trong package.

Dependency chính hiện có:

- `next`
- `react`
- `react-dom`
- `axios`
- `lucide-react`

### `package-lock.json`

File này là lockfile dependency do npm tạo.

### `next.config.ts`

File này khai báo cấu hình Next.js. Hiện file chưa thêm option tùy chỉnh ngoài object `nextConfig` rỗng.

### `tailwind.config.ts`

File này khai báo Tailwind CSS content paths cho `pages`, `components` và `app`, đồng thời map màu `background` và `foreground` từ CSS variables.

### `postcss.config.mjs`

File này cấu hình PostCSS để dùng Tailwind CSS và Autoprefixer.

### `tsconfig.json`

File này cấu hình TypeScript cho Next.js, bật `strict`, khai báo path alias `@/*` trỏ về thư mục frontend.

### `global.d.ts`

File này khai báo module type cho file CSS và CSS module.

### `next-env.d.ts`

File này do Next.js sinh để khai báo type environment cho project.

Trạng thái hiện tại: file tồn tại local sau khi chạy build và được `.gitignore` ignore.

## Nhiệm Vụ Các File Mã Nguồn

Thư mục gốc `frontend` không có file mã nguồn UI trực tiếp ngoài các file cấu hình TypeScript/Next.js. Mã UI và API client nằm trong các thư mục con:

- `app/`
- `components/`
- `lib/`

README chi tiết:

- `frontend/app/README_app.md`
- `frontend/components/README_components.md`
- `frontend/lib/README_lib.md`

## Cách Chạy Hiện Tại

Cài dependency frontend:

```bash
npm install
```

Chạy development server:

```bash
npm run dev
```

Frontend mặc định chạy tại:

```text
http://localhost:3000
```

Nếu cần đổi backend URL, cấu hình biến môi trường:

```text
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Nếu không cấu hình biến này, `frontend/lib/api.ts` mặc định gọi:

```text
http://localhost:8000
```

## Trạng Thái Hiện Tại

Tại thời điểm kiểm tra này, `frontend/node_modules/` tồn tại local và được `frontend/.gitignore` ignore.

Kiểm tra `npm run build` đã chạy thành công trong phiên kiểm tra này.

Development server chưa được khởi động trong phiên kiểm tra này.

## Endpoint Chat Hiện Tại

Frontend gọi endpoint chat OpenRouter tại:

```text
POST http://localhost:8000/api/chat/openai
```

Endpoint cũ vẫn tồn tại ở backend:

```text
POST http://localhost:8000/api/chat
```

Endpoint này sau p2 đã dùng hybrid retrieval, BM25 và reranker, nhưng frontend hiện chưa gọi endpoint đó.

## Cách Đổi Lại Endpoint Cũ

Nếu muốn frontend gọi lại endpoint legacy `POST /api/chat`, sửa file `frontend/lib/api.ts`.

Đổi endpoint trong `chatService.sendMessage(...)` từ:

```ts
`${API_URL}/api/chat/openai`
```

về:

```ts
`${API_URL}/api/chat`
```

Sau đó chạy lại frontend nếu cần:

```bash
npm run dev
```

## Ghi Chú Kỹ Thuật

Frontend gọi health check tại:

```text
GET http://localhost:8000/health
```
