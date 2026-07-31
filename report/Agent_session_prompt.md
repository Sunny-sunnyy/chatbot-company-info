# Prompt Khởi Động Session Cho Coding Agent

## Nhật Ký Cập Nhật

- 2026-07-24 20:31 +07 - Tạo prompt đầu tiên để copy sang coding agent trong session mới.
- 2026-07-24 21:24 +07 - Bổ sung quy tắc README phải mô tả nhiệm vụ của từng file trong thư mục.
- 2026-07-24 21:39 +07 - Làm rõ README phải có phần riêng mô tả nhiệm vụ các file mã nguồn.
- 2026-07-25 17:37 +07 - Bổ sung hướng dẫn sử dụng CodeGraph, kiểm tra đồng bộ index và ví dụ truy vấn cho coding agent.
- 2026-07-25 20:22 +07 - Bổ sung quy tắc README phải giải thích vai trò, hàm/luồng chính và trạng thái chạy của từng file mã nguồn đã có code.
- 2026-07-29 10:28 +07 - Bổ sung quy tắc đọc transcript giai đoạn nâng cao trong `tai_lieu/p2/<so_buoi>.txt`.
- 2026-07-31 17:24 +07 - Bổ sung quy tắc khi viết README cho folder phải nêu rõ nhiệm vụ của từng file `.py` trong folder đó.

## Nội Dung Prompt Để Copy Sang Session Mới

Bạn là coding agent làm việc trong dự án RAG chatbot Python này.

Trước khi làm bất kỳ thay đổi nào, hãy đọc kỹ toàn bộ ngữ cảnh sau để nắm đúng trạng thái hiện tại của repo.

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
- README của mỗi folder phải mô tả nhiệm vụ của thư mục và nhiệm vụ hoặc trạng thái hiện tại của từng file trong thư mục đó, bao gồm cả file README của chính thư mục nếu file đó tồn tại.
- Với folder có file mã nguồn, README phải có phần riêng tên `Nhiệm Vụ Các File Mã Nguồn` và mô tả từng file mã nguồn trong folder đó.
- Khi folder có file `.py`, README của folder đó phải nêu rõ từng file `.py` chịu trách nhiệm làm gì. Với file `.py` có code, ghi trách nhiệm chính dựa trên code thật; với file `.py` rỗng, ghi rõ file đang rỗng hoặc chỉ là package marker và không chứa logic xử lý.
- Với mỗi file mã nguồn đã có code, README cần giải thích thêm vai trò file, hàm hoặc luồng chính, input/output khi rõ ràng, và trạng thái chạy hiện tại nếu file hoặc flow chưa hoàn chỉnh.
- Với file mã nguồn đang rỗng, README chỉ ghi rõ file đang rỗng và chưa được phát triển; không gán vai trò xử lý hoặc mô tả flow chưa tồn tại.
- Nếu README lệch rõ ràng với code hiện tại, hãy báo ngắn rằng bạn sẽ cập nhật rồi tự sửa README.
- Khi cập nhật tài liệu, luôn thêm dòng mới vào mục `Nhật Ký Cập Nhật` với giờ Việt Nam `UTC+7`.
- Không commit trừ khi tôi yêu cầu rõ ràng.

## Thứ Tự Đọc File Khi Bắt Đầu Session

Hãy đọc theo thứ tự này trước khi kết luận hoặc chỉnh sửa:

1. Đọc hướng dẫn hệ thống/session hiện tại và các chỉ dẫn của người dùng.
2. Đọc `report/Project_status.md` để nắm trạng thái tổng quan mới nhất.
3. Đọc `report/README_report.md` để hiểu mục đích folder report.
4. Đọc README ở các folder liên quan tới task hiện tại.
5. Nếu task là cập nhật sau một buổi học, chỉ đọc transcript của đúng buổi đó trong `tai_lieu/<so_buoi>.txt` hoặc `tai_lieu/p2/<so_buoi>.txt`.
6. Nếu cần đối chiếu trạng thái sau nhiều buổi, đọc các transcript từ buổi đã được yêu cầu, không tự đọc trước các buổi chưa học hoặc chưa được yêu cầu.
7. Đọc code thật trong các folder liên quan để xác minh README có đúng không.
8. Nếu task là audit toàn dự án, đọc toàn bộ README theo folder và các file code tương ứng.

Nếu người dùng nói tới giai đoạn nâng cao, phần 2 hoặc `p2`, transcript tương ứng nằm trong `tai_lieu/p2/<so_buoi>.txt`. Ví dụ bài giới thiệu giai đoạn nâng cao là `tai_lieu/p2/0.txt`.

Chúng ta đã chuyển sang giai đoạn nâng cao của dự án.

## Quy Tắc Sử Dụng CodeGraph

CodeGraph là công cụ hỗ trợ coding agent hiểu code nhanh hơn bằng graph cục bộ của project. CodeGraph không thay thế `report/Project_status.md`, README theo folder hoặc transcript bài học. Các tài liệu markdown vẫn là nguồn ngữ cảnh học tập; code thật trong repo vẫn là nguồn sự thật về trạng thái triển khai.

Trước khi dùng CodeGraph trong session mới, hãy kiểm tra trạng thái đồng bộ:

```bash
codegraph version
codegraph status .
```

Trạng thái tốt cần có:

- Project đã được initialized, không báo `Not initialized`.
- `codegraph status .` báo `Index is up to date`.
- Backend dùng SQLite bình thường, ví dụ `node:sqlite` và journal `wal`.

Nếu `codegraph status .` báo chưa initialized, không tự chạy `codegraph init` trừ khi người dùng yêu cầu hoặc đã thống nhất. Khi chưa có index, dùng `rg`, `find`, `sed`, `wc` và đọc file trực tiếp theo quy trình bình thường.

Nếu index không đồng bộ hoặc nghi ngờ stale, có thể chạy:

```bash
codegraph sync
codegraph status .
```

Nếu người dùng yêu cầu init hoặc đã thống nhất dùng CodeGraph cho project, chạy:

```bash
codegraph init
codegraph status .
```

Thư mục `.codegraph/` là index SQLite local, đã được ignore trong `.gitignore` và không được commit.

Theo tài liệu CodeGraph, sau `codegraph init`, auto-sync được bật mặc định. CodeGraph sẽ watch project và cập nhật graph khi file thay đổi. Không cần chạy thủ công sau mỗi lần sửa file. Chỉ chạy `codegraph sync` khi muốn xác nhận lại hoặc khi nghi ngờ index lệch.

Khi MCP CodeGraph khả dụng trong coding agent, ưu tiên dùng `codegraph_explore` trước khi đọc hàng loạt file cho các câu hỏi kiểu:

- Một flow hoạt động như thế nào.
- Hàm nào gọi hàm nào.
- Sửa một symbol có thể ảnh hưởng tới file nào.
- Cần hiểu nhanh một module có nhiều import/call liên quan.

Ví dụ MCP query:

```text
projectPath: /home/hieu0606sunny/llm_rag
query: run_ingestion_pipeline chunk_architecture_types chunk_company_info
maxFiles: 6
```

Ví dụ CLI tương đương khi MCP chưa dùng được:

```bash
codegraph explore "run_ingestion_pipeline chunk_architecture_types chunk_company_info"
codegraph explore "How does embedding batch_embed_texts call embed_texts?"
codegraph explore "What depends on ingestion.helpers.make_metadata?"
```

Kết quả CodeGraph có thể chứa source code theo dòng, call path và blast radius. Hãy xem đó là ngữ cảnh đã đọc cho các file được trả về, nhưng vẫn phải kiểm tra lại bằng `sed` hoặc `rg` nếu:

- MCP báo lỗi.
- Kết quả có dấu hiệu stale.
- Bạn sắp sửa file và cần line number chính xác cho patch.
- Task yêu cầu audit README/data count chi tiết.

Nếu MCP CodeGraph lỗi sau khi vừa upgrade CodeGraph, có thể session agent hiện tại vẫn giữ process CodeGraph cũ. Trong trường hợp đó, dùng CLI `codegraph explore` hoặc công cụ đọc file thông thường, rồi ghi rõ trong báo cáo rằng session mới/restart agent sẽ dùng binary mới.

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
- Mô tả nhiệm vụ hoặc trạng thái hiện tại của từng file trong folder, bao gồm cả file README của chính folder nếu có.
- Nếu folder có file mã nguồn, thêm hoặc cập nhật phần `Nhiệm Vụ Các File Mã Nguồn`.
- Nếu folder có file `.py`, trong phần `Nhiệm Vụ Các File Mã Nguồn` phải có mục riêng cho từng file `.py` và nêu rõ file đó chịu trách nhiệm làm gì trong project.
- Với file mã nguồn đã có code, ngoài danh sách import/hàm hiện có, hãy bổ sung vai trò file, hàm hoặc luồng chính, input/output khi rõ ràng, và trạng thái chạy nếu code chưa import/chạy được nguyên vẹn.
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
- Nếu tôi nói "p2 bài 0", "giai đoạn nâng cao bài 0" hoặc yêu cầu tương đương, chỉ dùng `tai_lieu/p2/0.txt` cùng với trạng thái repo hiện tại.
- Với các buổi thuộc giai đoạn nâng cao, dùng đúng file `tai_lieu/p2/<so_buoi>.txt`; không tự đọc các file p2 sau buổi được yêu cầu.
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



## Đọc cả các hướng dẫn/link liên quan nếu thực sự cần để hiểu đúng context.

## Đừng bắt đầu bất kỳ công việc nào khác ngoài việc đọc và kiểm tra cấu trúc thư mục. Khi bạn đã đọc xong tất cả, hãy cho tôi biết nếu bạn có thắc mắc trước khi chúng ta bắt đầu.
