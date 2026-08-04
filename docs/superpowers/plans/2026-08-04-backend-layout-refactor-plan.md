# Backend Layout Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the Python backend runtime into `backend/` while keeping frontend, Docker Compose, dependency files, root `.env`, docs, and Qdrant storage at the workspace root.

**Architecture:** `backend/` becomes the Python runtime root. Internal backend imports stay top-level (`from core...`, `from api...`) and commands are run from inside `backend/`. Root remains the workspace root for frontend, Docker Compose, dependency lockfiles, report docs, and `.env`.

**Tech Stack:** Python 3.12+, uv, FastAPI, pytest, Qdrant, SentenceTransformer, OpenAI Agents SDK, Next.js frontend, Docker Compose.

## Global Constraints

- Do not change RAG business logic.
- Do not change API endpoint paths.
- Do not change `/api/chat/openai` SSE event contract.
- Do not change frontend behavior.
- Do not move `.env`; keep it at root and do not read or print its contents.
- Do not move `qdrant_storage/`; keep it at root.
- Do not move `frontend/`, `report/`, or `tai_lieu/`.
- Do not move `pyproject.toml`, `uv.lock`, or `docker-compose.yml`.
- Do not convert imports to `backend.*`.
- Do not create wrappers for old root commands.
- Standard backend commands run from `backend/`.
- Default validation must not call Qdrant or OpenRouter real services.
- Do not commit unless the user explicitly asks.

---

## File Structure

### Create

- `backend/README_backend.md`: overview of the new backend runtime root and command conventions.

### Move

Move these root folders into `backend/`:

- `api/` -> `backend/api/`
- `config/` -> `backend/config/`
- `core/` -> `backend/core/`
- `data/` -> `backend/data/`
- `embedding/` -> `backend/embedding/`
- `ingestion/` -> `backend/ingestion/`
- `llm/` -> `backend/llm/`
- `logs/` -> `backend/logs/`
- `reranking/` -> `backend/reranking/`
- `retrieval/` -> `backend/retrieval/`
- `scoring/` -> `backend/scoring/`
- `vectorstore/` -> `backend/vectorstore/`
- `tests/` -> `backend/tests/`

### Modify

- `backend/core/settings_loader.py`: split backend directory from project root so settings load from backend and `.env` loads from root.
- `backend/core/logging_setup.py`: verify config/log path after move.
- `backend/api/app.py`: verify uvicorn module path remains `api.app:app`.
- `README.md`: update root structure and backend commands.
- `RUN_GUIDE.md`: update backend/ingestion/test commands.
- `README_docker.md`: keep Qdrant storage root mount clear.
- `report/Project_status.md`: update snapshot to new backend layout.
- `report/README_report.md`: update description if it summarizes `Project_status.md`.
- README files moved inside `backend/`: update old root-relative command/path text where it would be wrong.

### Do Not Modify Unless Required By Validation

- `frontend/**`
- `docker-compose.yml`
- `pyproject.toml`
- `uv.lock`
- `qdrant_storage/**`
- `.env`
- RAG business logic files beyond path fixes.

---

## Task 1: Preflight And Baseline

**Files:**
- Read: `docs/superpowers/specs/2026-08-04-backend-layout-refactor-design.md`
- Read: `report/Project_status.md`
- Read: `README.md`
- Read: `RUN_GUIDE.md`
- Read: `core/settings_loader.py`
- Read: `core/logging_setup.py`
- Read: `config/settings.yaml`
- Read: `config/logging.yaml`

**Interfaces:**
- Consumes: approved design spec.
- Produces: confirmed baseline and list of files to move/update.

- [ ] **Step 1: Confirm working tree state**

Run:

```bash
git status --short
```

Expected: note existing unrelated changes. Do not revert unrelated user changes.

- [ ] **Step 2: Confirm no current `backend/` folder conflict**

Run:

```bash
test ! -e backend
```

Expected: command exits `0`. If it fails, inspect `backend/` and stop for user confirmation before overwriting or merging.

- [ ] **Step 3: Confirm source folders exist at root**

Run:

```bash
for d in api config core data embedding ingestion llm logs reranking retrieval scoring vectorstore tests; do test -d "$d" || exit 1; done
```

Expected: command exits `0`.

- [ ] **Step 4: Confirm root folders/files that must stay**

Run:

```bash
for p in frontend report tai_lieu docker-compose.yml pyproject.toml uv.lock qdrant_storage; do test -e "$p" || exit 1; done
```

Expected: command exits `0`.

---

## Task 2: Move Backend Runtime Folders

**Files:**
- Create directory: `backend/`
- Move folders listed in File Structure.

**Interfaces:**
- Consumes: root backend folders.
- Produces: backend runtime root with top-level packages inside `backend/`.

- [ ] **Step 1: Create `backend/`**

Run:

```bash
mkdir backend
```

Expected: `backend/` exists and is empty.

- [ ] **Step 2: Move backend folders**

Run:

```bash
mv api config core data embedding ingestion llm logs reranking retrieval scoring vectorstore tests backend/
```

Expected: all listed folders are under `backend/`.

- [ ] **Step 3: Verify moved layout**

Run:

```bash
for d in api config core data embedding ingestion llm logs reranking retrieval scoring vectorstore tests; do test -d "backend/$d" || exit 1; done
```

Expected: command exits `0`.

- [ ] **Step 4: Verify root retained folders**

Run:

```bash
for p in frontend report tai_lieu docker-compose.yml pyproject.toml uv.lock qdrant_storage; do test -e "$p" || exit 1; done
```

Expected: command exits `0`.

---

## Task 3: Fix Backend Path Resolution

**Files:**
- Modify: `backend/core/settings_loader.py`
- Modify if needed: `backend/core/logging_setup.py`

**Interfaces:**
- Consumes: backend runtime root under `backend/`.
- Produces: settings loaded from `backend/config/settings.yaml`, secrets loaded from root `.env`, logs written under `backend/logs/`.

- [ ] **Step 1: Update `backend/core/settings_loader.py` path constants**

Replace the old constants:

```python
BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_PATH = BASE_DIR / "config" / "settings.yaml"
ENV_PATH = BASE_DIR / ".env"
```

With:

```python
BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent
SETTINGS_PATH = BACKEND_DIR / "config" / "settings.yaml"
ENV_PATH = PROJECT_ROOT / ".env"
```

Keep:

```python
load_dotenv(ENV_PATH)
```

Do not read or print `.env`.

- [ ] **Step 2: Review `backend/core/logging_setup.py` constants**

Expected final path behavior:

```python
BASE_DIR = Path(__file__).resolve().parent.parent
LOGGING_CONFIG_PATH = BASE_DIR / "config" / "logging.yaml"
LOGS_DIR = BASE_DIR / "logs"
```

This is correct after the move because `BASE_DIR` points to `backend/`. Only edit if the file differs from this behavior.

- [ ] **Step 3: Verify settings load from backend and env path points to root**

Run from root:

```bash
cd backend && uv run python -c "from core.settings_loader import SETTINGS_PATH, ENV_PATH; print(SETTINGS_PATH); print(ENV_PATH)"
```

Expected output paths:

```text
/home/hieu0606sunny/llm_rag/backend/config/settings.yaml
/home/hieu0606sunny/llm_rag/.env
```

Do not print any environment variable values.

- [ ] **Step 4: Verify logging config path**

Run from root:

```bash
cd backend && uv run python -c "from core.logging_setup import LOGGING_CONFIG_PATH, LOGS_DIR; print(LOGGING_CONFIG_PATH); print(LOGS_DIR)"
```

Expected output paths:

```text
/home/hieu0606sunny/llm_rag/backend/config/logging.yaml
/home/hieu0606sunny/llm_rag/backend/logs
```

---

## Task 4: Verify Imports And Runtime Entrypoints

**Files:**
- Verify: `backend/api/app.py`
- Verify: `backend/ingestion/pipeline.py`
- Verify: `backend/tests/conftest.py`

**Interfaces:**
- Consumes: top-level packages under `backend/`.
- Produces: backend commands that work when run from `backend/`.

- [ ] **Step 1: Check root-level old imports are not converted to `backend.*`**

Run from root:

```bash
rg -n "from backend\\.|import backend\\." backend
```

Expected: no matches.

- [ ] **Step 2: Verify backend app import**

Run from root:

```bash
cd backend && uv run python -c "import importlib; importlib.import_module('api.app'); print('api.app import ok')"
```

Expected:

```text
api.app import ok
```

This import must not start Uvicorn.

- [ ] **Step 3: Verify ingestion pipeline import**

Run from root:

```bash
cd backend && uv run python -c "import importlib; importlib.import_module('ingestion.pipeline'); print('ingestion.pipeline import ok')"
```

Expected:

```text
ingestion.pipeline import ok
```

- [ ] **Step 4: Verify `tests/conftest.py` still adds backend root to `sys.path`**

Expected `backend/tests/conftest.py` logic:

```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
```

After moving tests to `backend/tests`, this correctly points to `backend/`.

---

## Task 5: Compile And Run Existing Tests

**Files:**
- Test: `backend/tests/test_api_chat_openai.py`
- Test: `backend/tests/test_context_builder.py`
- Test: `backend/tests/test_llm_generator_openai.py`

**Interfaces:**
- Consumes: moved code and fixed path resolution.
- Produces: proof that package imports and mocked tests still pass.

- [ ] **Step 1: Compile core backend modules**

Run from root:

```bash
cd backend && uv run python -m py_compile \
  api/app.py api/health.py api/routes/chat.py api/routes/chat_openai.py \
  core/settings_loader.py core/logging_setup.py core/schema.py core/startup.py \
  ingestion/pipeline.py ingestion/load_data.py \
  embedding/embedder.py embedding/batch_embed.py embedding/sparse_embedder.py \
  vectorstore/qdrant.py vectorstore/upsert.py vectorstore/hybrid_index.py \
  retrieval/hybrid_retriever.py retrieval/context_builder.py retrieval/retriever.py \
  scoring/bm25.py \
  reranking/base.py reranking/reranker.py reranking/models/cross_encoder.py \
  llm/prompt.py llm/generator.py llm/generator_openai.py
```

Expected: command exits `0`.

- [ ] **Step 2: Run backend tests**

Run from root:

```bash
cd backend && uv run pytest tests/ -q
```

Expected: all existing tests pass. These tests must not call Qdrant or OpenRouter real services.

- [ ] **Step 3: If `uv` cannot discover the root project from `backend/`, use the root-project form and document it**

Fallback command:

```bash
cd backend && uv run --project .. pytest tests/ -q
```

If this fallback is required, update docs to use `uv run --project .. ...` consistently instead of plain `uv run ...` from `backend/`. Prefer plain `uv run ...` only if it works.

---

## Task 6: Create `backend/README_backend.md`

**Files:**
- Create: `backend/README_backend.md`

**Interfaces:**
- Consumes: final backend folder layout and command decisions.
- Produces: backend folder documentation for future agents/students.

- [ ] **Step 1: Write README header and update log**

Before writing the line, run:

```bash
date '+%Y-%m-%d %H:%M +07'
```

Use that concrete output in this line:

````markdown
# README_backend

## Nhật Ký Cập Nhật

- 2026-08-04 19:05 +07 - Tạo README cho thư mục `backend` sau refactor layout: backend trở thành runtime root chứa các package Python, data, logs và tests; frontend, `.env`, Docker Compose và `qdrant_storage/` vẫn ở root.
````

The timestamp shown above is an example format; replace it with the actual command output.

- [ ] **Step 2: Document backend purpose**

Include:

````markdown
## Nhiệm Vụ Của Thư Mục

Thư mục `backend` là runtime root cho toàn bộ Python backend của dự án RAG chatbot NMK.

Khi chạy backend, ingestion hoặc tests, working directory chuẩn là `backend/`.
````

- [ ] **Step 3: List child folders and responsibilities**

Include every child folder:

````markdown
- `api/`: FastAPI app, health endpoint và chat routes.
- `config/`: YAML settings và logging config.
- `core/`: settings loader, logging setup, schema và startup components.
- `data/`: raw và processed JSON data.
- `embedding/`: dense embedding, batch embedding và sparse embedder.
- `ingestion/`: load data, chunking pipeline và helpers.
- `llm/`: prompt, legacy Ollama generator và OpenRouter streaming generator.
- `logs/`: application log file.
- `reranking/`: CrossEncoder reranker.
- `retrieval/`: legacy dense retriever, hybrid retriever và context builder.
- `scoring/`: BM25 scorer.
- `vectorstore/`: Qdrant client, point builders và upsert.
- `tests/`: pytest tests cho backend.
````

- [ ] **Step 4: Document commands**

Add this section to `backend/README_backend.md`:

````markdown
## Lệnh Chạy

```bash
cd backend
uv run python -m api.app
uv run python -m ingestion.pipeline
uv run pytest tests/ -q
```
````

- [ ] **Step 5: Document root-owned files**

Include:

````markdown
## Thành Phần Vẫn Ở Root

- `.env`: file secret/config local, được `core/settings_loader.py` load từ root. Không đọc hoặc ghi nội dung file này vào tài liệu.
- `docker-compose.yml`: Docker Compose cho Qdrant.
- `qdrant_storage/`: dữ liệu local của Qdrant do Docker mount.
- `frontend/`: Next.js frontend.
- `report/` và `tai_lieu/`: tài liệu trạng thái và học tập.
````

---

## Task 7: Update Root Documentation

**Files:**
- Modify: `README.md`
- Modify: `RUN_GUIDE.md`
- Modify: `README_docker.md` if needed
- Modify: `report/Project_status.md`
- Modify: `report/README_report.md` if needed

**Interfaces:**
- Consumes: new folder layout and command syntax.
- Produces: docs that do not instruct old root backend commands.

- [ ] **Step 1: Update root README structure**

In `README.md`, replace descriptions that say backend folders are at root with descriptions that say backend code is under `backend/`.

Required new facts:

```text
Thư mục `backend/` chứa toàn bộ Python backend runtime.
Frontend vẫn nằm ở `frontend/`.
Docker Compose, `pyproject.toml`, `uv.lock`, `.env` và `qdrant_storage/` vẫn nằm ở root.
```

- [ ] **Step 2: Update root README commands**

Replace:

```bash
uv run python -m api.app
uv run python -m ingestion.pipeline
```

With:

```bash
cd backend
uv run python -m api.app
uv run python -m ingestion.pipeline
```

If Task 5 required `uv run --project ..`, use that command form consistently.

- [ ] **Step 3: Update RUN_GUIDE commands**

In `RUN_GUIDE.md`, keep Qdrant command at root:

```bash
docker compose up -d qdrant
```

Change backend commands to:

```bash
cd backend
uv run python -m ingestion.pipeline
uv run python -m api.app
```

Frontend command stays:

```bash
cd frontend
npm run dev
```

- [ ] **Step 4: Update README_docker only for storage clarity**

Keep:

```yaml
./qdrant_storage:/qdrant/storage
```

Make clear that `qdrant_storage/` remains at root even after backend code moves into `backend/`.

- [ ] **Step 5: Update `report/Project_status.md`**

Before writing the line, run:

```bash
date '+%Y-%m-%d %H:%M +07'
```

Add a new `Nhật Ký Cập Nhật` entry using that concrete output:

````markdown
- 2026-08-04 19:05 +07 - Cập nhật trạng thái layout: tạo thư mục `backend/` làm runtime root cho Python backend; các folder `api`, `config`, `core`, `data`, `embedding`, `ingestion`, `llm`, `logs`, `reranking`, `retrieval`, `scoring`, `vectorstore`, `tests` đã nằm trong `backend/`; frontend, `.env`, Docker Compose, `qdrant_storage/`, `report/` và `tai_lieu/` vẫn ở root.
````

The timestamp shown above is an example format; replace it with the actual command output.

Then update any sections that list top-level folders so they point to `backend/<folder>` for backend modules.

- [ ] **Step 6: Update `report/README_report.md` if it summarizes stale Project_status content**

If `README_report.md` says backend folders are root-level, update it to say `Project_status.md` now documents the `backend/` runtime root.

---

## Task 8: Update Moved Folder README Files

**Files:**
- Modify as needed under `backend/**/README*.md`

**Interfaces:**
- Consumes: moved folder paths.
- Produces: folder READMEs that remain truthful after the move.

- [ ] **Step 1: Search for old root command references inside backend docs**

Run from root:

```bash
rg -n "uv run python -m api\\.app|uv run python -m ingestion\\.pipeline|uv run pytest tests|data/raw|data/processed|logs/application\\.log|qdrant_storage" backend -g "README*.md"
```

- [ ] **Step 2: Update command references**

For README files under `backend/`, commands can assume the user is in `backend/`.

Use:

```bash
uv run python -m api.app
uv run python -m ingestion.pipeline
uv run pytest tests/ -q
```

Do not instruct old root command usage.

- [ ] **Step 3: Update root-relative path language**

Use these conventions:

- Inside backend docs, backend-local paths can be written as `api/app.py`, `data/raw`, `logs/application.log`.
- When referring from root docs, use `backend/api/app.py`, `backend/data/raw`, `backend/logs/application.log`.
- Always describe `qdrant_storage/` as root-level.
- Always describe `.env` as root-level.

- [ ] **Step 4: Add update log entries to modified README files**

Each modified README must get a `Nhật Ký Cập Nhật` line with actual Vietnam time.

---

## Task 9: Final Verification

**Files:**
- Verify entire workspace.

**Interfaces:**
- Consumes: completed move, path fixes, docs updates.
- Produces: final proof and a concise handoff summary.

- [ ] **Step 1: Verify required layout**

Run from root:

```bash
for d in api config core data embedding ingestion llm logs reranking retrieval scoring vectorstore tests; do test -d "backend/$d" || exit 1; done
for d in api config core data embedding ingestion llm logs reranking retrieval scoring vectorstore tests; do test ! -e "$d" || exit 1; done
for p in frontend report tai_lieu docker-compose.yml pyproject.toml uv.lock qdrant_storage; do test -e "$p" || exit 1; done
```

Expected: command exits `0`.

- [ ] **Step 2: Verify no backend package imports were converted to `backend.*`**

Run:

```bash
rg -n "from backend\\.|import backend\\." backend
```

Expected: no matches.

- [ ] **Step 3: Verify no docs still instruct old root backend commands**

Run:

```bash
rg -n "uv run python -m api\\.app|uv run python -m ingestion\\.pipeline|uv run pytest tests" README.md RUN_GUIDE.md report backend -g "*.md"
```

Expected: any matches either appear in a `cd backend` context or are explicitly marked as old commands that are no longer supported.

- [ ] **Step 4: Re-run compile**

Run:

```bash
cd backend && uv run python -m py_compile \
  api/app.py api/health.py api/routes/chat.py api/routes/chat_openai.py \
  core/settings_loader.py core/logging_setup.py core/schema.py core/startup.py \
  ingestion/pipeline.py ingestion/load_data.py \
  embedding/embedder.py embedding/batch_embed.py embedding/sparse_embedder.py \
  vectorstore/qdrant.py vectorstore/upsert.py vectorstore/hybrid_index.py \
  retrieval/hybrid_retriever.py retrieval/context_builder.py retrieval/retriever.py \
  scoring/bm25.py \
  reranking/base.py reranking/reranker.py reranking/models/cross_encoder.py \
  llm/prompt.py llm/generator.py llm/generator_openai.py
```

Expected: command exits `0`.

- [ ] **Step 5: Re-run tests**

Run:

```bash
cd backend && uv run pytest tests/ -q
```

Expected: all existing tests pass.

- [ ] **Step 6: Report final state**

Final response should include:

- backend folders moved into `backend/`
- root folders/files intentionally kept at root
- path logic changed for root `.env`
- validation commands and results
- docs updated
- no commit unless explicitly requested
