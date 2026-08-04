# README_components

## Nhật Ký Cập Nhật

- 2026-08-04 18:01 +07 - Sửa bug UI duplicate assistant khi stream: bỏ block loading indicator riêng ở cuối messages list; trong bubble assistant, nếu message là assistant placeholder cuối cùng đang stream (`content` rỗng + `isLoading` + `index === messages.length - 1`) thì hiển thị 3 chấm loading ngay trong bubble thay vì bubble trắng rỗng; khi delta đầu tiên tới, bubble tự chuyển sang render `ReactMarkdown`.
- 2026-08-04 17:33 +07 - Cập nhật `ChatInterface.tsx` sau khi triển khai streaming + Markdown: submit thêm assistant placeholder rỗng, append delta khi stream về, gắn sources khi nhận event, cập nhật `sessionId` khi nhận `meta`/`done`, render assistant content bằng `ReactMarkdown` + `remarkGfm` với component mapping cho `p`/`strong`/`ul`/`ol`/`li`/`a`/`code`/`pre`, bubble thêm `min-w-0 break-words` để không tràn.
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
- Import `ReactMarkdown` từ `react-markdown` và `remarkGfm` từ `remark-gfm`.
- Import icon `Send`, `Bot`, `User` và `Image` từ `lucide-react`.
- Import `chatService` và type `ChatMessage` từ `frontend/lib/api.ts`.
- Định nghĩa component `ChatInterface`.

Vai trò và luồng hoạt động:

- `ChatInterface` là UI chat chính của frontend.
- Component giữ state `messages`, `input`, `isLoading` và `sessionId`.
- Khi người dùng submit form, component thêm message của user vào state, thêm assistant placeholder rỗng, gọi `chatService.sendMessageStream(...)` với callbacks `onMeta`/`onDelta`/`onSources`/`onDone`/`onError`, append từng delta vào assistant message cuối bằng functional `setMessages`, gắn `sources` khi nhận event `sources`, cập nhật `sessionId` khi nhận `meta` hoặc `done`.
- Nếu request lỗi, component hiển thị message lỗi tiếng Việt trong assistant message cuối.
- Component tự scroll xuống cuối khi danh sách message thay đổi.
- Nội dung assistant được render bằng `ReactMarkdown` với `remarkGfm`, component mapping style cho `p`, `strong`, `ul`, `ol`, `li`, `a` (mở tab mới), `code`, `pre` (overflow ngang); bubble có `min-w-0 break-words` để nội dung không tràn trên mobile/desktop.
- Trong lúc stream, chỉ có một assistant row: nếu message là assistant placeholder cuối cùng đang stream (`content` rỗng, `isLoading`, `index === messages.length - 1`), bubble hiển thị 3 chấm loading thay vì bubble trắng rỗng; khi delta đầu tiên tới, bubble tự chuyển sang render `ReactMarkdown`. Không còn block loading indicator riêng ở cuối messages list nên không có duplicate bot icon.
- Với message assistant có `sources`, component lọc source có metadata hình ảnh và hiển thị tối đa 3 hình.
- Input chính là thao tác nhập câu hỏi của người dùng.
- Output là UI chat được render trong browser và request streaming tới backend.

## Cách Hoạt Động Hiện Tại

`frontend/app/page.tsx` render trực tiếp `ChatInterface`.

Component gọi API qua `chatService` trong `frontend/lib/api.ts`, không gọi `fetch` hoặc Axios trực tiếp trong JSX.

## Ghi Chú Kỹ Thuật

Component dùng thẻ `<img>` HTML thường, chưa dùng `next/image`.

Session hiện được lưu trong React state, nên sẽ mất khi reload trang.
