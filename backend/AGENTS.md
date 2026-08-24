# backend/AGENTS.md

Backend conventions for the Iris FastAPI service.

## Stack

- **FastAPI** — async API framework
- **SQLAlchemy 2.0** (async) — declarative mapped classes (`Mapped[...]`, `mapped_column`), not
  the older `Column(...)` style
- **aiosqlite** — async SQLite driver
- **uv** — dependency management and virtual environment
- **pytest** / **pytest-asyncio** — tests
- **ruff** — lint

## Layout

```
backend/
├── app/
│   ├── main.py       # FastAPI app instance, middleware, router registration
│   ├── database.py   # async engine, session factory, declarative Base, get_db dependency
│   ├── models/        # SQLAlchemy models (one module per entity)
│   └── routers/        # FastAPI routers (thin, HTTP-shaped)
├── tests/
└── pyproject.toml
```

Service functions (the actual logic behind routers) belong in a sibling `services/` package once
introduced — see IRIS-5 in the backlog: routers stay thin and HTTP-shaped, services stay
plain-Python and agent-callable.

## Commands

Run from `backend/`:

- `uv run uvicorn app.main:app --reload` — dev server
- `uv run pytest` — run tests
- `uv run ruff check` — lint
- `uv add <package>` / `uv add --dev <package>` — add a runtime/dev dependency

## Conventions

- Request-scoped `AsyncSession` via `Depends(get_db)`, not a global session
- Pydantic response/request models kept separate from SQLAlchemy models — never return ORM
  objects directly from a route
- Service functions that agent tools will also call (ADR 0003) take plain arguments and return
  plain data — no `Request`/`Response` in their signatures
- SQLite file (`iris.db`) is gitignored; configure `DATABASE_URL` via `.env` (see `.env.example`)

## Code Standards

- Ruff handles lint (`pyproject.toml` `[tool.ruff]`); no separate formatter configured yet
- Follow existing patterns in `app/` when adding new code
