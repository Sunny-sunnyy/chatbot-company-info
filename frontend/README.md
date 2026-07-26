# Chatbot NMK Frontend

## Nhật Ký Cập Nhật

- 2026-07-26 21:02 +07 - Cập nhật README ngắn của frontend theo trạng thái mã nguồn sau buổi 7 và kết quả build frontend.

## Nhiệm Vụ Của File

File này ghi nhanh lệnh cài đặt và chạy frontend Next.js.

Tài liệu chi tiết của thư mục nằm ở `README_frontend.md`.

## Cài Đặt

```bash
npm install
```

## Chạy Development Server

```bash
npm run dev
```

Truy cập:

```text
http://localhost:3000
```

## Cấu Hình Backend URL

Nếu cần đổi backend URL, cấu hình biến môi trường:

```text
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Nếu không cấu hình biến này, frontend mặc định gọi backend tại `http://localhost:8000`.

## Trạng Thái Hiện Tại

Frontend có code Next.js, React, TypeScript, Tailwind CSS, Axios và lucide-react.

Tại thời điểm kiểm tra này, `node_modules/` tồn tại local và được `.gitignore` ignore.

Kiểm tra `npm run build` đã chạy thành công. Development server chưa được khởi động trong phiên kiểm tra này.
