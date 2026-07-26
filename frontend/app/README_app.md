# README_app

## Nhật Ký Cập Nhật

- 2026-07-26 21:02 +07 - Tạo README cho thư mục `frontend/app` sau buổi 7, đối chiếu với mã nguồn App Router hiện tại.

## Nhiệm Vụ Của Thư Mục

Thư mục `frontend/app` chứa các file App Router của Next.js.

Hiện tại thư mục này định nghĩa layout gốc, global CSS và page đầu tiên render giao diện chat.

## File Tài Liệu Trong Thư Mục

### `README_app.md`

File này mô tả nhiệm vụ của thư mục `frontend/app` và trạng thái từng file mã nguồn trong thư mục.

## Nhiệm Vụ Các File Mã Nguồn

### `layout.tsx`

File này đã có mã nguồn.

Nội dung chính:

- Import `Metadata` từ Next.js.
- Import `globals.css`.
- Export metadata gồm title `NMK Chatbot` và description.
- Định nghĩa `RootLayout`.

Vai trò và luồng hoạt động:

- `layout.tsx` là layout gốc của Next.js App Router.
- Input là `children` do Next.js truyền vào.
- Output là HTML structure gồm `<html lang="vi">` và `<body>{children}</body>`.

### `page.tsx`

File này đã có mã nguồn.

Nội dung chính:

- Import `ChatInterface` từ `@/components/ChatInterface`.
- Export component `Home`.

Vai trò và luồng hoạt động:

- `page.tsx` là page mặc định của frontend.
- File render trực tiếp `ChatInterface`.
- Input không nhận prop riêng.
- Output là UI chat chính của ứng dụng.

### `globals.css`

File này đã có mã nguồn CSS.

Nội dung chính:

- Import Tailwind base, components và utilities.
- Khai báo CSS variables `--background` và `--foreground`.
- Có media query `prefers-color-scheme: dark` để đổi CSS variables theo theme hệ thống.
- Cấu hình `body` dùng màu từ CSS variables và font Arial/Helvetica.

Vai trò và luồng hoạt động:

- `globals.css` là CSS global cho frontend.
- File cung cấp Tailwind entry và style nền/chữ mặc định cho toàn app.

## Cách Hoạt Động Hiện Tại

Next.js render `frontend/app/page.tsx`, page này render `ChatInterface` từ `frontend/components`.

## Ghi Chú Kỹ Thuật

Thư mục này không chứa API client. API client nằm ở `frontend/lib/api.ts`.
