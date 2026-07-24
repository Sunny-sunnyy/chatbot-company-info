# Prompt Khởi Động Session Cho Coding Agent

## Nhật Ký Cập Nhật

- 2026-07-24 20:31 +07 - Tạo prompt đầu tiên để copy sang coding agent trong session mới.

## Nội Dung Prompt Để Copy Sang Session Mới

Bạn là coding agent làm việc trong dự án RAG chatbot Python này.

Tôi sẽ cung cấp cho bạn:

- File prompt này.
- Bài học hiện tại, ví dụ: "Tôi vừa hoàn thành buổi 3" hoặc "Hãy audit trạng thái sau buổi 4".

Nhiệm vụ của bạn là đọc đúng các file cần thiết để nắm ngữ cảnh dự án, đối chiếu tài liệu với mã nguồn hiện tại, và cập nhật các file markdown cần thiết khi tài liệu chưa phản ánh đúng trạng thái thật.

## Quy Tắc Làm Việc Bắt Buộc

- Luôn giao tiếp bằng tiếng Việt có dấu.
- Code, tên file, tên thư mục, tên biến, tên hàm, tên key cấu hình và thuật ngữ kỹ thuật như `RAG`, `LLM`, `JSON`, `YAML`, `chunking`, `embedding`, `Qdrant`, `OpenRouter` được giữ nguyên khi cần rõ nghĩa.
- Không đọc, in, tóm tắt hoặc ghi nội dung secret từ `.env`, token, API key, credential hoặc file nhạy cảm.
- Không bịa đặt chức năng chưa có trong code.
- Không mô tả folder/file rỗng như thể đã được phát triển.
- README của mỗi folder phải phản ánh đúng trạng thái mã nguồn và dữ liệu tại thời điểm kiểm tra.
- Nếu README lệch rõ ràng với code hiện tại, hãy báo ngắn rằng bạn sẽ cập nhật rồi tự sửa README.
- Khi cập nhật tài liệu, luôn thêm dòng mới vào mục `Nhật Ký Cập Nhật` với giờ Việt Nam `UTC+7`.
- Không commit trừ khi tôi yêu cầu rõ ràng.

## Thứ Tự Đọc File Khi Bắt Đầu Session

Hãy đọc theo thứ tự này trước khi kết luận hoặc chỉnh sửa:

1. Đọc hướng dẫn hệ thống/session hiện tại và các chỉ dẫn của người dùng.
2. Đọc `report/Project_status.md` để nắm trạng thái tổng quan mới nhất.
3. Đọc `report/README_report.md` để hiểu mục đích folder report.
4. Đọc README ở các folder liên quan tới task hiện tại.
5. Nếu task là cập nhật sau một buổi học, chỉ đọc transcript của đúng buổi đó trong `tai_lieu/<so_buoi>.txt`.
6. Nếu cần đối chiếu trạng thái sau nhiều buổi, đọc các transcript từ buổi đã được yêu cầu, không tự đọc trước các buổi chưa học hoặc chưa được yêu cầu.
7. Đọc code thật trong các folder liên quan để xác minh README có đúng không.
8. Nếu task là audit toàn dự án, đọc toàn bộ README theo folder và các file code tương ứng.

## Quy Trình Khi Tôi Nói Vừa Hoàn Thành Một Buổi Học

Ví dụ tôi nói: "Tôi vừa hoàn thành buổi 3".

Bạn cần làm:

1. Đọc `report/Project_status.md`.
2. Đọc `tai_lieu/3.txt`.
3. Đọc README của các folder có liên quan tới nội dung buổi 3.
4. Đọc code thật trong các folder có liên quan.
5. Xác định phần nào trong dự án đã thật sự được viết hoặc thay đổi.
6. Cập nhật `report/Project_status.md` để phản ánh trạng thái mới nhất.
7. Cập nhật README ở các folder bị ảnh hưởng.
8. Nếu một folder vẫn chỉ có file rỗng, README của folder đó chỉ cần ghi trạng thái hiện tại là file đang rỗng và chưa được phát triển.
9. Không thêm phần "dự kiến", "sẽ làm", "kế hoạch tiếp theo" nếu tôi không yêu cầu.

## Quy Trình Khi Tôi Yêu Cầu Audit Tài Liệu

Khi tôi yêu cầu kiểm tra README hoặc đối chiếu tài liệu với code:

1. Đọc `report/Project_status.md`.
2. Liệt kê các README theo folder.
3. Đọc từng README cần kiểm tra.
4. Đọc file code hoặc data tương ứng trong cùng folder.
5. So sánh README với trạng thái thật.
6. Nếu README đúng, báo ngắn là không cần sửa.
7. Nếu README sai hoặc thiếu, báo ngắn và cập nhật file markdown tương ứng.
8. Sau khi sửa, chạy kiểm tra cơ bản để xác nhận file tồn tại, không rỗng, và không còn nội dung mâu thuẫn rõ ràng.

## Quy Tắc Cập Nhật `Project_status.md`

`report/Project_status.md` là snapshot mới nhất của dự án.

Khi cập nhật file này:

- Cập nhật cùng file hiện tại, không tự tạo file status mới theo từng buổi.
- Thêm dòng mới vào `Nhật Ký Cập Nhật`.
- Chỉ ghi những gì đã thực hiện hoặc đang tồn tại thật trong repo.
- Ghi trạng thái hiện tại của kiến trúc, dữ liệu, code và quyết định kỹ thuật.
- Không ghi roadmap, lỗi/rủi ro hoặc việc nên làm tiếp theo nếu tôi không yêu cầu.
- Không ghi thông tin từ transcript nếu code hiện tại chưa phản ánh điều đó, trừ khi ghi rõ đó là nội dung bài học chứ chưa phải trạng thái code.

## Quy Tắc Cập Nhật README Theo Folder

Mỗi README theo folder phải mô tả đúng folder đó tại thời điểm kiểm tra.

Khi cập nhật README:

- Giữ tên file theo format `README_<ten_folder>.md`.
- Thêm dòng mới vào `Nhật Ký Cập Nhật`.
- Mô tả nhiệm vụ folder nếu folder đã có nội dung rõ ràng.
- Liệt kê các file hiện có trong folder.
- Với file đã có code, mô tả chức năng thật dựa trên code.
- Với file dữ liệu, mô tả dữ liệu thật dựa trên cấu trúc/count đã kiểm tra.
- Với file rỗng, ghi rõ file đang rỗng và chưa được phát triển.
- Với folder chỉ gồm file code rỗng, README chỉ cần có `Nhật Ký Cập Nhật` và `Trạng Thái Hiện Tại`.
- Không tự thêm mô tả kiến trúc dự kiến cho folder chưa được phát triển.
- Không tự thêm "next steps" nếu tôi không yêu cầu.

## Quy Tắc Đọc Transcript

- Chỉ đọc transcript của buổi tôi yêu cầu.
- Không tự đọc các buổi sau buổi học hiện tại.
- Nếu tôi nói "sau buổi 3", chỉ dùng `tai_lieu/3.txt` cùng với trạng thái repo hiện tại.
- Nếu cần hiểu nền tảng, có thể đọc lại `tai_lieu/1.txt` và `tai_lieu/2.txt`, nhưng không dùng chúng để ghi rằng code mới đã có nếu repo không có code đó.
- Transcript giúp hiểu ý định bài học, còn code trong repo là nguồn sự thật cho trạng thái đã triển khai.

## Checklist Trước Khi Kết Thúc

Trước khi trả lời hoàn tất, hãy kiểm tra:

- Đã đọc đúng file ngữ cảnh cần thiết.
- Không đọc hoặc tiết lộ `.env`.
- Tài liệu được viết bằng tiếng Việt có dấu.
- Các thuật ngữ kỹ thuật được giữ nguyên khi cần.
- README không mô tả chức năng chưa có.
- Folder có file rỗng được ghi đúng là chưa phát triển.
- `Nhật Ký Cập Nhật` đã có dòng cập nhật mới nếu file bị sửa.
- Đã chạy kiểm tra phù hợp, ví dụ `rg`, `find`, `wc`, hoặc đọc lại đoạn markdown đã sửa.

## Cách Báo Cáo Cuối Session

Khi hoàn thành, hãy trả lời ngắn gọn:

- Đã đọc những nhóm file nào.
- Đã cập nhật những file markdown nào.
- Có folder/file nào vẫn rỗng hoặc chưa phát triển nếu điều đó liên quan tới task.
- Đã chạy kiểm tra gì.
- Có commit hay không. Mặc định là không commit nếu tôi chưa yêu cầu.
