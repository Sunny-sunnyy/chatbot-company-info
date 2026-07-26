# README_components

## Nhật Ký Cập Nhật

- 2026-07-26 21:02 +07 - Tạo README cho thư mục `frontend/components` sau buổi 7, đối chiếu với component chat hiện tại.

## Nhiệm Vụ Của Thư Mục

Thư mục `frontend/components` chứa React components dùng bởi frontend.

Hiện tại thư mục này có component giao diện chat chính.

## File Tài Liệu Trong Thư Mục

### `README_components.md`

File này mô tả nhiệm vụ của thư mục `frontend/components` và trạng thái từng file mã nguồn trong thư mục.

## Nhiệm Vụ Các File Mã Nguồn

### `ChatInterface.tsx`

File này đã có mã nguồn.

Nội dung chính:

- Khai báo `'use client'`.
- Import `useState`, `useRef` và `useEffect` từ React.
- Import icon `Send`, `Bot`, `User` và `Image` từ `lucide-react`.
- Import `chatService` và type `ChatMessage` từ `frontend/lib/api.ts`.
- Định nghĩa component `ChatInterface`.

Vai trò và luồng hoạt động:

- `ChatInterface` là UI chat chính của frontend.
- Component giữ state `messages`, `input`, `isLoading` và `sessionId`.
- Khi người dùng submit form, component thêm message của user vào state, gọi `chatService.sendMessage(...)`, nhận response từ backend, lưu `session_id` nếu có, rồi thêm message assistant vào state.
- Nếu request lỗi, component hiển thị message lỗi tiếng Việt.
- Component tự scroll xuống cuối khi danh sách message thay đổi.
- Với message assistant có `sources`, component lọc source có metadata hình ảnh và hiển thị tối đa 3 hình.
- Input chính là thao tác nhập câu hỏi của người dùng.
- Output là UI chat được render trong browser và request HTTP tới backend.

## Cách Hoạt Động Hiện Tại

`frontend/app/page.tsx` render trực tiếp `ChatInterface`.

Component gọi API qua `chatService` trong `frontend/lib/api.ts`, không gọi `fetch` hoặc Axios trực tiếp trong JSX.

## Ghi Chú Kỹ Thuật

Component dùng thẻ `<img>` HTML thường, chưa dùng `next/image`.

Session hiện được lưu trong React state, nên sẽ mất khi reload trang.
