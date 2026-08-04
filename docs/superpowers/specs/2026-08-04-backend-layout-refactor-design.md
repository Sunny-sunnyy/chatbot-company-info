# Backend Layout Refactor Design

## Purpose

Tái cấu trúc project để gom toàn bộ phần Python backend vào một runtime root mới tên `backend/`, trong khi vẫn giữ frontend, tài liệu toàn dự án, dependency root và Docker Compose ở root workspace.

Tài liệu này là spec để worker khác thực hiện. Tại thời điểm viết spec này, refactor chưa được thực hiện.

## Approved Direction

Chọn hướng 1: move các folder backend vào `backend/`, chạy backend từ bên trong folder `backend/`, và giữ imports nội bộ backend ở dạng top-level hiện tại.

Ví dụ imports vẫn giữ:

```python
from core.settings_loader import load_settings
from retrieval.hybrid_retriever import hybrid_retrieve
from llm.generator_openai import stream_answer_async
```

Không đổi imports sang:

```python
from backend.core.settings_loader import load_settings
```

## Target Structure

Root workspace sau refactor:

```text
llm_rag/
├── backend/
├── frontend/
├── docs/superpowers/specs/
├── docs/superpowers/plans/
├── report/
├── tai_lieu/
├── qdrant_storage/
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── README.md
├── README_docker.md
└── RUN_GUIDE.md
```

`backend/` sau refactor:

```text
backend/
├── api/
├── config/
├── core/
├── data/
├── embedding/
├── ingestion/
├── llm/
├── logs/
├── reranking/
├── retrieval/
├── scoring/
├── vectorstore/
├── tests/
└── README_backend.md
```

## Folders To Move Into `backend/`

Move these root folders into `backend/`:

- `api`
- `config`
- `core`
- `data`
- `embedding`
- `ingestion`
- `llm`
- `logs`
- `reranking`
- `retrieval`
- `scoring`
- `vectorstore`
- `tests`

## Folders And Files That Stay At Root

Do not move:

- `frontend/`
- `docs/`
- `report/`
- `tai_lieu/`
- `qdrant_storage/`
- `.env`
- `.gitignore`
- `docker-compose.yml`
- `pyproject.toml`
- `uv.lock`
- `README.md`
- `README_codegraph.md`
- `README_docker.md`
- `RUN_GUIDE.md`
- `brainstorming.md`

`qdrant_storage/` stays at root because it is a Docker/Qdrant runtime artifact and `docker-compose.yml` also stays at root.

`.env` stays at root. Do not read, print, copy, summarize, or commit `.env`.

## Runtime Commands After Refactor

The standard backend working directory is `backend/`.

Run backend:

```bash
cd backend
uv run python -m api.app
```

Run ingestion:

```bash
cd backend
uv run python -m ingestion.pipeline
```

Run backend tests:

```bash
cd backend
uv run pytest tests/ -q
```

Do not preserve old root commands:

```bash
uv run python -m api.app
uv run python -m ingestion.pipeline
uv run pytest tests/ -q
```

Those old commands are intentionally out of scope after this refactor.

## Path Design

After moving `core/settings_loader.py` to `backend/core/settings_loader.py`, path logic must distinguish root workspace from backend runtime root.

Use this design:

```python
BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent
SETTINGS_PATH = BACKEND_DIR / "config" / "settings.yaml"
ENV_PATH = PROJECT_ROOT / ".env"
```

Expected behavior:

- `settings.yaml` is loaded from `backend/config/settings.yaml`.
- `.env` is loaded from root `.env`.
- Data paths such as `data/raw` and `data/processed` stay valid when commands run from `backend/`.
- Logging path `logs/application.log` stays valid when commands run from `backend/`.

`core/logging_setup.py` also needs path review after being moved. It should read logging config from `backend/config/logging.yaml` and create/write `backend/logs/application.log` when commands run from `backend/`.

## Docker/Qdrant

`docker-compose.yml` stays at root and should keep the existing storage mount:

```yaml
volumes:
  - ./qdrant_storage:/qdrant/storage
```

Do not move `qdrant_storage/` into `backend/`.

Qdrant remains available at:

```text
http://localhost:6333
```

The backend settings may continue using:

```yaml
vector_database.url: http://localhost:6333
```

## Frontend

`frontend/` stays at root.

Do not change frontend API behavior. The frontend should continue using:

```text
NEXT_PUBLIC_API_URL=http://localhost:8000
POST /api/chat/openai
```

The `/api/chat/openai` contract remains SSE streaming through `fetch()` in `frontend/lib/api.ts`.

## Documentation Scope

Update documentation only enough to prevent wrong commands/path claims after the refactor.

Required documentation updates:

- Root `README.md`
- Root `RUN_GUIDE.md`
- `README_docker.md` if it references backend/data/log paths affected by the move
- `report/Project_status.md`
- `report/README_report.md` if it describes `Project_status.md`
- README files inside moved folders if they mention old root paths or old root commands
- Create `backend/README_backend.md`

Do not rewrite the full deep dive as part of this refactor unless a directly relevant command/path would otherwise be clearly wrong.

## Non-Goals

Do not:

- Change RAG business logic.
- Change endpoint paths.
- Change the SSE event contract.
- Change frontend behavior.
- Change the Qdrant collection schema.
- Rebuild Qdrant data.
- Run OpenRouter calls.
- Move `.env`.
- Move `qdrant_storage/`.
- Create compatibility wrappers for old root commands.
- Convert imports to `backend.*`.

## Validation Requirements

After implementation, run from root:

```bash
cd backend
uv run python -m py_compile \
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

Then run:

```bash
uv run pytest tests/ -q
```

Expected result:

- Python files compile.
- Existing tests pass without Qdrant or OpenRouter real calls.

No default requirement to run Docker, Qdrant ingestion, backend server, frontend server, or OpenRouter smoke tests in this refactor.

## Acceptance Criteria

The refactor is complete when:

- All approved backend folders are under `backend/`.
- Root still contains `frontend/`, `report/`, `tai_lieu/`, `.env`, `docker-compose.yml`, `pyproject.toml`, `uv.lock`, and `qdrant_storage/`.
- `cd backend && uv run python -m api.app` imports the app module successfully when dependencies are available.
- `cd backend && uv run python -m ingestion.pipeline` imports the ingestion pipeline successfully when dependencies are available.
- `cd backend && uv run pytest tests/ -q` passes with existing mocked tests.
- Backend loads `.env` from root and settings from `backend/config/settings.yaml`.
- Docs no longer instruct the user to run backend commands from root.
- No secrets are read or exposed.

