# Spec: Streaming Và Markdown Cho Chat OpenRouter

## Nhật Ký Cập Nhật

- 2026-08-04 17:02 +07 - Tạo spec cho việc chuyển route chat OpenRouter sang SSE streaming và render Markdown live bằng `react-markdown` + `remark-gfm`.

## Mục Tiêu

Nâng cấp trải nghiệm chat hiện tại để:

- Endpoint chính `POST /api/chat/openai` trả lời dạng stream thay vì chờ toàn bộ câu trả lời.
- UI hiển thị token/delta liên tục khi LLM sinh văn bản.
- Nội dung assistant được render Markdown live để các cú pháp như `**bold**`, bullet list, link và line break hiển thị đúng.
- Vẫn giữ sources, `session_id`, rate limit, retrieval, BM25, reranking và `ContextBuilder` như luồng hiện tại.

Không thay đổi mục tiêu RAG, không fine-tuning, không thay retrieval/reranking hiện tại.

## Bối Cảnh Code Hiện Tại

Backend:

- `api/routes/chat_openai.py` hiện định nghĩa `POST /api/chat/openai`, nhận `ChatRequest`, chạy `hybrid_retrieve()`, reranker, `ContextBuilder`, gọi `generate_answer_async()`, rồi trả `ChatResponse` JSON một lần.
- `llm/generator_openai.py` hiện dùng `Runner.run(agent, prompt)` và trả full string từ `result.final_output`.
- OpenAI Agents SDK trong môi trường hiện tại có `Runner.run_streamed(...)`.
- Official docs của OpenAI Agents SDK mô tả `Runner.run_streamed()` trả `RunResultStreaming`, đọc token bằng `result.stream_events()` và lọc `raw_response_event` với `ResponseTextDeltaEvent`.

Frontend:

- `frontend/lib/api.ts` hiện dùng Axios `post()` tới `/api/chat/openai` và chờ full JSON response.
- `frontend/components/ChatInterface.tsx` hiện render assistant content bằng `<p className="whitespace-pre-wrap">{message.content}</p>`, nên Markdown bị hiển thị như text thường.

## Quyết Định Thiết Kế

### Streaming Protocol

Dùng Server-Sent Events với media type:

```text
text/event-stream
```

Lý do:

- Phù hợp luồng một chiều server -> browser cho token streaming.
- Dễ gửi nhiều event type: `meta`, `delta`, `sources`, `done`, `error`.
- Dễ debug bằng browser devtools hoặc curl.
- Không cần WebSocket cho MVP vì client chỉ gửi một request, server stream một response.

### Endpoint Chính

Giữ URL chính:

```text
POST /api/chat/openai
```

Nhưng chuyển response của endpoint này sang SSE stream.

Lưu ý tương thích:

- Các test hoặc client cũ đang kỳ vọng JSON sẽ cần được cập nhật.
- Nếu muốn giữ tương thích backward, agent thực thi có thể thêm endpoint phụ `/api/chat/openai/json`; nhưng yêu cầu hiện tại là streaming cho path chính nên không bắt buộc.

### Markdown Renderer

Dùng:

```text
react-markdown
remark-gfm
```

Frontend render Markdown live trong assistant bubble. Không dùng `IPython.display.Markdown` vì cách đó chỉ áp dụng trong notebook, không áp dụng cho Next.js/browser.

## SSE Event Contract

Backend trả từng event theo format SSE:

```text
event: <event_type>
data: <json_string>

```

Các event bắt buộc:

### `meta`

Gửi ngay sau khi request hợp lệ và `session_id` đã được xác định.

```json
{
  "session_id": "uuid"
}
```

### `delta`

Gửi mỗi khi OpenAI Agents SDK trả text delta.

```json
{
  "delta": "một phần text"
}
```

Frontend append `delta` vào message assistant hiện tại.

### `sources`

Gửi sau khi retrieval/reranking hoàn tất và trước hoặc sau các delta đều được, nhưng khuyến nghị gửi trước `done`.

```json
{
  "sources": [
    {
      "text": "source text rút gọn...",
      "metadata": {},
      "score": 1.23
    }
  ]
}
```

### `done`

Gửi khi stream kết thúc thành công.

```json
{
  "answer": "full answer đã ghép từ các delta",
  "session_id": "uuid"
}
```

Backend dùng `answer` này để lưu session in-memory giống route hiện tại.

### `error`

Gửi khi lỗi xảy ra sau khi stream đã bắt đầu.

```json
{
  "message": "Thông báo lỗi tiếng Việt an toàn cho người dùng"
}
```

Nếu lỗi xảy ra trước khi tạo `StreamingResponse` hoặc trước khi bắt đầu body, có thể dùng `HTTPException` như hiện tại cho `400`, `429`, `503`.

## Backend Behavior

Luồng endpoint mới:

1. Nhận `ChatRequest`.
2. Check rate limit theo IP như hiện tại.
3. Strip `query`; query rỗng trả `400`.
4. Tạo hoặc dùng lại `session_id`.
5. Lấy BM25/reranker từ `core.startup`.
6. BM25 chưa sẵn sàng trả `503`.
7. Chạy `hybrid_retrieve(question, bm25)`.
8. Nếu không có documents, stream `meta`, một `delta` chứa câu không tìm thấy thông tin, `sources` rỗng, rồi `done`.
9. Nếu có documents, rerank nếu reranker sẵn sàng; nếu không có reranker thì cắt top K như hiện tại.
10. Build context bằng `ContextBuilder`.
11. Build prompt giống `generate_answer_async()`.
12. Gọi `Runner.run_streamed(agent, prompt)`.
13. Lặp `async for event in result.stream_events()`.
14. Nếu `event.type == "raw_response_event"` và `event.data` là `ResponseTextDeltaEvent`, lấy `event.data.delta`, append vào `answer_parts`, yield SSE `delta`.
15. Khi stream kết thúc, ghép `answer = "".join(answer_parts).strip()`.
16. Build `sources`.
17. Lưu session in-memory với question, answer, sources.
18. Yield `sources` và `done`.

## LLM Generator Design

Nên tách logic generator thành 2 đường:

- `generate_answer_async(context, question) -> str`: giữ hoặc chỉnh tối thiểu cho non-stream tests/fallback.
- `stream_answer_async(context, question) -> AsyncIterator[str]`: generator mới yield text delta.

`stream_answer_async()` nên tái sử dụng:

- `_validate_inputs(context, question)`
- `_build_openrouter_agent()`
- `build_prompt(context, question)`
- error handling an toàn

Nếu validation lỗi, generator có thể yield một delta duy nhất là thông báo lỗi, hoặc route xử lý trước khi gọi generator. Khuyến nghị route xử lý validation trước để dễ phân biệt lỗi HTTP và lỗi stream.

## Frontend Behavior

`frontend/lib/api.ts`:

- Axios không phù hợp để đọc browser stream token-by-token trong use case này.
- Dùng `fetch()` cho request streaming.
- Thêm function mới, ví dụ `sendMessageStream(request, handlers)`.
- Function này đọc `response.body.getReader()`, decode `Uint8Array` bằng `TextDecoder`, parse SSE event, gọi callback theo event:
  - `onMeta(sessionId)`
  - `onDelta(delta)`
  - `onSources(sources)`
  - `onDone(payload)`
  - `onError(message)`

`frontend/components/ChatInterface.tsx`:

- Khi submit, thêm user message như hiện tại.
- Thêm ngay assistant message rỗng `{ role: "assistant", content: "", sources: [] }`.
- Khi nhận `delta`, update assistant message cuối bằng cách append content.
- Khi nhận `sources`, gắn sources vào assistant message cuối.
- Khi nhận `done`, tắt loading.
- Khi error, append hoặc thay content bằng thông báo lỗi tiếng Việt.

Markdown live:

- Thay `<p className="whitespace-pre-wrap">{message.content}</p>` bằng `ReactMarkdown`.
- Dùng `remarkGfm`.
- Style các element cơ bản: `p`, `ul`, `ol`, `li`, `strong`, `a`, `code`, `pre`.
- Giữ giới hạn bubble hiện tại nhưng cần tránh text/table tràn ngang; dùng `break-words` và `overflow-x-auto` cho code/table nếu có.

## Error Handling

Giữ các HTTP error trước stream:

- `400`: query rỗng sau strip.
- `429`: rate limit.
- `503`: BM25 chưa sẵn sàng.

Sau khi stream bắt đầu:

- Không thể đổi status code HTTP một cách đáng tin cậy.
- Gửi SSE `event: error` với message an toàn.
- Frontend hiển thị message lỗi trong assistant bubble và tắt loading.

## Tests Cần Có

Backend:

- Test SSE endpoint trả `meta`, `delta`, `sources`, `done` trong happy path với monkeypatch `stream_answer_async`.
- Test `503` khi BM25 chưa sẵn sàng.
- Test `429` khi rate limit fail.
- Test không có documents: stream answer mặc định và sources rỗng.
- Test session lưu full answer sau khi stream hoàn tất.

LLM generator:

- Test `stream_answer_async()` yield delta từ `Runner.run_streamed()` bằng fake streaming result.
- Test validation/provider/API key error không gọi network thật.

Frontend:

- Nếu project chưa có test frontend, tối thiểu chạy `npm run build`.
- Nếu thêm unit test sau này, test parser SSE riêng là phần đáng ưu tiên.

## Acceptance Criteria

- Người dùng gửi câu hỏi từ UI và thấy câu trả lời xuất hiện dần, không đợi full response.
- Nội dung Markdown render đúng trong assistant bubble: bold, bullet list, numbered list, link, line break.
- Sources và ảnh từ metadata vẫn hiển thị sau hoặc trong lúc câu trả lời stream.
- `session_id` vẫn được giữ giữa các lượt hỏi.
- Rate limit, BM25 readiness, no-document behavior vẫn hoạt động.
- Không đọc hoặc log secret từ `.env`.
- `uv run pytest tests/ -q` pass sau khi cập nhật tests.
- `npm run build` pass trong `frontend/`.

## Nguồn Tham Khảo Chính

- OpenAI Agents SDK Streaming: `https://openai.github.io/openai-agents-python/streaming/`
- OpenAI Agents SDK Running Agents: `https://openai.github.io/openai-agents-python/running_agents/`
- FastAPI StreamingResponse: `https://fastapi.tiangolo.com/advanced/stream-data/`
