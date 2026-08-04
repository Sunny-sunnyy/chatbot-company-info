# Plan: Triển Khai Streaming Và Markdown Cho Chat OpenRouter

## Nhật Ký Cập Nhật

- 2026-08-04 17:02 +07 - Tạo implementation plan cho agent khác triển khai SSE streaming trên `POST /api/chat/openai` và Markdown live rendering trên frontend.

## Phạm Vi

Triển khai đúng spec trong `report/spec_streaming_markdown_chat.md`.

Không làm:

- Không thay đổi logic chunking, embedding, Qdrant, BM25, reranking hoặc prompt ngoài phần cần để stream LLM output.
- Không đổi provider LLM.
- Không tạo lại `docs/`.
- Không xử lý production auth/CORS.

## Giả Định

- Endpoint chính cần chuyển sang SSE là `POST /api/chat/openai`.
- Frontend được phép thêm dependency `react-markdown` và `remark-gfm`.
- Streaming chỉ cần một chiều server -> browser; không dùng WebSocket.
- Vẫn dùng OpenAI Agents SDK qua OpenRouter như hiện tại.

## Bước 1: Chuẩn Bị Dependency Frontend

Thay đổi:

- Trong `frontend/`, thêm:

```bash
npm install react-markdown remark-gfm
```

Verify:

```bash
cd frontend
npm ls react-markdown remark-gfm
```

Ghi chú:

- Agent thực thi cần dùng command phù hợp môi trường.
- Nếu sandbox/network chặn install, xin approval theo quy tắc môi trường.

## Bước 2: Thêm Generator Streaming Ở Backend

File cần sửa:

- `llm/generator_openai.py`

Việc cần làm:

- Import `AsyncIterator` nếu cần type hint.
- Import `ResponseTextDeltaEvent` từ `openai.types.responses`.
- Thêm function `async def stream_answer_async(context: str, question: str)`.
- Function mới tái sử dụng `_validate_inputs()`, `_build_openrouter_agent()` và `build_prompt()`.
- Gọi `Runner.run_streamed(agent, prompt)`.
- Lặp `async for event in result.stream_events()`.
- Khi event là text delta, yield `event.data.delta`.
- Giữ error messages tiếng Việt an toàn, không expose stack trace hoặc secret.

Verify nhỏ:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile llm/generator_openai.py
```

Test nên thêm:

- Fake `Runner.run_streamed()` trả object có `stream_events()`.
- Assert `stream_answer_async()` yield đúng các delta.

## Bước 3: Chuyển Route `/api/chat/openai` Sang SSE

File cần sửa:

- `api/routes/chat_openai.py`

Việc cần làm:

- Import:
  - `json`
  - `AsyncIterator` nếu cần
  - `StreamingResponse` từ `fastapi.responses`
  - `stream_answer_async` từ `llm.generator_openai`
- Thêm helper encode SSE, ví dụ:

```python
def _sse_event(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"
```

- Giữ `ChatRequest` và `ChatResponse` nếu tests hoặc OpenAPI còn cần; nhưng route streaming sẽ không dùng `response_model=ChatResponse`.
- Endpoint `chat_openai_endpoint()` sau khi validate/rate limit/BM25 readiness trả:

```python
return StreamingResponse(event_generator(), media_type="text/event-stream")
```

- `event_generator()` thực hiện retrieval, reranking, context, stream answer, build sources, lưu session.
- Với lỗi trước khi return `StreamingResponse`, tiếp tục dùng `HTTPException`.
- Với lỗi trong generator, yield `error`.

Event order khuyến nghị:

1. `meta`
2. `delta` nhiều lần
3. `sources`
4. `done`

No-documents path:

1. `meta`
2. `delta` với câu `"Tôi không tìm thấy thông tin phù hợp trong dữ liệu hiện có."`
3. `sources` với `[]`
4. `done`

Verify nhỏ:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile api/routes/chat_openai.py
```

## Bước 4: Cập Nhật Backend Tests

File cần sửa:

- `tests/test_api_chat_openai.py`
- Có thể thêm file mới nếu muốn tách SSE parser/backend route tests.

Việc cần làm:

- Vì endpoint giờ trả `StreamingResponse`, test happy path cần consume `response.body_iterator`.
- Monkeypatch:
  - `hybrid_retrieve`
  - `stream_answer_async`
  - `get_bm25`
  - `get_reranker`
  - `check_rate_limit`
- Assert stream chứa:
  - `event: meta`
  - delta mong đợi
  - `event: sources`
  - `event: done`
- Cập nhật test cũ đang kỳ vọng `ChatResponse` object.

Verify:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_chat_openai.py -q
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_llm_generator_openai.py -q
```

## Bước 5: Thêm SSE Client Ở Frontend

File cần sửa:

- `frontend/lib/api.ts`

Việc cần làm:

- Giữ types `ChatRequest`, `ChatResponse`, `Source`, `ChatMessage`.
- Thêm type callbacks:

```ts
interface StreamHandlers {
  onMeta?: (sessionId: string) => void;
  onDelta?: (delta: string) => void;
  onSources?: (sources: Source[]) => void;
  onDone?: (payload: { answer?: string; session_id?: string }) => void;
  onError?: (message: string) => void;
}
```

- Thêm `sendMessageStream(request, handlers)`.
- Dùng `fetch()`:
  - method `POST`
  - `Content-Type: application/json`
  - body JSON.stringify(request)
- Nếu `!response.ok`, parse text/json nếu có và throw error.
- Đọc stream bằng:
  - `response.body?.getReader()`
  - `TextDecoder`
  - buffer string
- Parse SSE blocks tách bằng `\n\n`.
- Với mỗi block, lấy `event:` và `data:`, parse JSON, gọi handler tương ứng.

Verify:

```bash
cd frontend
npm run build
```

## Bước 6: Render Streaming Message Trong ChatInterface

File cần sửa:

- `frontend/components/ChatInterface.tsx`

Việc cần làm:

- Import:

```tsx
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
```

- Khi submit:
  - Add user message.
  - Add assistant placeholder message rỗng.
  - Gọi `chatService.sendMessageStream(...)`.
  - `onDelta`: append delta vào assistant message cuối.
  - `onMeta`: update `sessionId`.
  - `onSources`: gắn sources cho assistant message cuối.
  - `onDone`: đảm bảo `sessionId` được cập nhật và tắt loading.
  - `onError`: hiển thị lỗi trong assistant message cuối.
- Tránh dùng stale closure khi update messages; dùng functional `setMessages(prev => ...)`.
- Thay render text bằng `ReactMarkdown`.

Style Markdown khuyến nghị:

- Container assistant bubble dùng `prose prose-sm max-w-none` nếu có typography plugin; nếu không có plugin, style component thủ công.
- Không bắt buộc thêm `@tailwindcss/typography` để giữ scope nhỏ.
- Component mapping tối thiểu:
  - `p`: margin nhỏ, whitespace bình thường
  - `ul`/`ol`: list indent
  - `li`: margin nhỏ
  - `a`: màu xanh, underline, `target="_blank"`, `rel="noreferrer"`
  - `code`/`pre`: overflow ngang

Verify:

```bash
cd frontend
npm run build
```

## Bước 7: Manual Smoke Test

Điều kiện:

- Qdrant đang chạy.
- Collection hybrid có 450 points.
- Backend có OpenRouter API key trong environment.
- Frontend dev server đang chạy.

Lệnh backend:

```bash
uv run python -m api.app
```

Lệnh frontend:

```bash
cd frontend
npm run dev
```

Smoke test bằng curl:

```bash
curl -N -X POST http://localhost:8000/api/chat/openai \
  -H "Content-Type: application/json" \
  -d '{"query":"Thông tin công ty Nguyen Minh Khang Architects là gì?"}'
```

Kỳ vọng:

- Response header là `text/event-stream`.
- Thấy các event `meta`, nhiều `delta`, `sources`, `done`.

Smoke test UI:

- Gửi câu hỏi "thông tin công ty".
- Text xuất hiện dần.
- Bold/list Markdown render đúng.
- Sources/ảnh vẫn hiển thị nếu metadata có ảnh.
- Không còn thấy raw `**`, bullet Markdown bị dính như text thường, trừ khi model sinh Markdown không hợp lệ.

## Bước 8: Cập Nhật Tài Liệu Sau Khi Code Xong

Chỉ làm bước này sau khi code đã được agent thực thi và verify.

File nên cập nhật:

- `report/Project_status.md`
- `report/README_report.md`
- `README.md`
- `api/README_api.md`
- `api/routes/README_routes.md`
- `llm/README_llm.md`
- `frontend/README_frontend.md`
- `frontend/components/README_components.md`
- `frontend/lib/README_lib.md`
- `tests/README_tests.md`
- `tai_lieu/rag_system_pipeline_deep_dive.md` nếu muốn deep dive phản ánh stream mới.

Mỗi file được sửa cần thêm dòng `Nhật Ký Cập Nhật` theo giờ Việt Nam.

## Thứ Tự Verify Cuối

Chạy từ nhỏ tới rộng:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile llm/generator_openai.py api/routes/chat_openai.py
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_llm_generator_openai.py -q
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_chat_openai.py -q
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/ -q
cd frontend
npm run build
```

Nếu dependency frontend mới chưa được cài, chạy `npm install` trước `npm run build`.

## Rủi Ro Và Cách Giảm

- SSE parse sai khi chunk TCP cắt giữa event: dùng buffer string và chỉ parse khi gặp `\n\n`.
- Markdown live bị nhảy layout khi token chưa hoàn chỉnh: chấp nhận cho MVP; nếu khó chịu, render plain text khi loading và Markdown khi done.
- Không thể đổi HTTP status sau khi stream bắt đầu: lỗi trong generator phải gửi `event: error`.
- Axios không stream browser tốt cho use case này: dùng `fetch()` cho endpoint streaming.
- Tests cũ kỳ vọng JSON response sẽ fail: cập nhật test theo SSE contract.
- Endpoint path chính đổi protocol: mọi client khác gọi `/api/chat/openai` cần được cập nhật để đọc SSE.
