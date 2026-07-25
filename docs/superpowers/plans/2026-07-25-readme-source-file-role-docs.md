# README Source File Role Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bổ sung giải thích vai trò file, hàm chính và trạng thái chạy vào README của các folder có file Python thật.

**Architecture:** Giữ nguyên cấu trúc README hiện tại và bổ sung nội dung học tập vào phần `Nhiệm Vụ Các File Mã Nguồn`. Không mô tả chức năng chưa có; file rỗng tiếp tục được ghi rõ là chưa phát triển.

**Tech Stack:** Python, Markdown, RAG, Qdrant, SentenceTransformer, `uv`, CodeGraph.

## Global Constraints

- Giao tiếp và tài liệu bằng tiếng Việt có dấu.
- Không đọc, in hoặc ghi nội dung secret từ `.env`, token, API key, credential.
- Không bịa đặt chức năng chưa có trong code.
- Mỗi markdown bị sửa phải thêm dòng `Nhật Ký Cập Nhật` theo giờ Việt Nam `UTC+7`.
- Không commit nếu người dùng chưa yêu cầu.
- Chỉ cập nhật README có file Python thật: `README.md`, `core`, `ingestion`, `ingestion/chunking`, `ingestion/helpers`, `embedding`, `vectorstore`; `llm` và `retrieval` giữ trạng thái rỗng/chưa phát triển.

---

### Task 1: Refresh Source Context

**Files:**
- Read: `core/*.py`
- Read: `ingestion/*.py`
- Read: `ingestion/chunking/*.py`
- Read: `ingestion/helpers/*.py`
- Read: `embedding/*.py`
- Read: `vectorstore/*.py`

**Interfaces:**
- Consumes: current repository files.
- Produces: verified source context for README edits.

- [ ] **Step 1: Read source files in parallel**

Run:

```bash
sed -n '1,220p' core/settings_loader.py
sed -n '1,220p' core/logging_setup.py
sed -n '1,260p' ingestion/pipeline.py
sed -n '1,220p' vectorstore/qdrant.py
```

- [ ] **Step 2: Confirm empty files remain empty**

Run:

```bash
wc -c chat.py retrieval/retriever.py llm/llm.py llm/prompt.py
```

Expected: all four files have `0` bytes.

---

### Task 2: Update README Files With Role And Flow Sections

**Files:**
- Modify: `README.md`
- Modify: `core/README_core.md`
- Modify: `ingestion/README_ingestion.md`
- Modify: `ingestion/chunking/README_chunking.md`
- Modify: `ingestion/helpers/README_helpers.md`
- Modify: `embedding/README_embedding.md`
- Modify: `vectorstore/README_vectorstore.md`

**Interfaces:**
- Consumes: verified source context from Task 1.
- Produces: README sections that explain each non-empty Python file by role, main functions, data flow, and current run status.

- [ ] **Step 1: Add update log line to each modified README**

Use timestamp:

```text
2026-07-25 20:22 +07
```

- [ ] **Step 2: Add role and flow text under each non-empty Python file**

For each file that has code, add a concise section:

```markdown
Vai trò và luồng hoạt động:

- File này chịu trách nhiệm ...
- `<function_name>()` ...
- Input chính là ...
- Output chính là ...
```

- [ ] **Step 3: Preserve empty-file status**

Keep `chat.py`, `retrieval/retriever.py`, `llm/llm.py`, and `llm/prompt.py` documented as empty and undeveloped. Do not add imagined behavior.

---

### Task 3: Update Project Status And Agent Prompt

**Files:**
- Modify: `report/Project_status.md`
- Modify: `report/Agent_session_prompt.md`
- Modify: `report/README_report.md` if its file descriptions become stale.

**Interfaces:**
- Consumes: README updates from Task 2.
- Produces: project snapshot and future-agent prompt that reflect the new README documentation standard.

- [ ] **Step 1: Update `Project_status.md`**

Add one `Nhật Ký Cập Nhật` line and a short note that README files for folders with real Python code now include role and flow explanations for source files.

- [ ] **Step 2: Update `Agent_session_prompt.md`**

Add a concise rule under README folder documentation: for every non-empty source file, README should explain file role, main functions/flow, input/output when clear, and current run status when incomplete.

- [ ] **Step 3: Update `README_report.md` if needed**

If `Agent_session_prompt.md` description no longer reflects the prompt content, add a short update and log entry.

---

### Task 4: Verification

**Files:**
- Read: modified markdown files.
- Run: repository checks.

**Interfaces:**
- Consumes: all documentation edits.
- Produces: final verification result.

- [ ] **Step 1: Confirm modified files exist and are non-empty**

Run:

```bash
wc -c README.md core/README_core.md ingestion/README_ingestion.md ingestion/chunking/README_chunking.md ingestion/helpers/README_helpers.md embedding/README_embedding.md vectorstore/README_vectorstore.md report/Project_status.md report/Agent_session_prompt.md
```

- [ ] **Step 2: Confirm new role wording exists**

Run:

```bash
rg -n "Vai trò và luồng hoạt động|vai trò file|hàm/luồng chính|trạng thái chạy" README.md core/README_core.md ingestion/README_ingestion.md ingestion/chunking/README_chunking.md ingestion/helpers/README_helpers.md embedding/README_embedding.md vectorstore/README_vectorstore.md report/Project_status.md report/Agent_session_prompt.md
```

- [ ] **Step 3: Confirm no secret content was read or written**

Run:

```bash
git diff -- README.md core/README_core.md ingestion/README_ingestion.md ingestion/chunking/README_chunking.md ingestion/helpers/README_helpers.md embedding/README_embedding.md vectorstore/README_vectorstore.md report/Project_status.md report/Agent_session_prompt.md report/README_report.md
```

Expected: diff contains only documentation changes and no `.env` content.
