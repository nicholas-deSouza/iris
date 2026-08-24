# Iris

AI-native note-taking app: nested block editing with an AI agent that can read and edit notes directly.

## Prerequisites

- [Node.js](https://nodejs.org/) >= 22
- [pnpm](https://pnpm.io/) >= 10 (`corepack enable` will pick up the version pinned in `package.json`)
- [Python](https://www.python.org/) >= 3.11
- [uv](https://docs.astral.sh/uv/) for backend dependency management (`brew install uv`)

## Setup

Install frontend dependencies from the repo root:

```bash
pnpm install
```

Install backend dependencies from `backend/`:

```bash
cd backend
uv sync
```

This creates a virtual environment at `backend/.venv`. `uv run <command>` (used throughout this
README) uses it automatically, no activation needed. To activate it directly in your shell
instead (e.g. so `python`/`pip` resolve to it without prefixing `uv run`):

```bash
source .venv/bin/activate   # from backend/; `deactivate` to leave it
```

Backend config is read from `backend/.env` (see `backend/.env.example`); it's optional for local
dev since `DATABASE_URL` defaults to a local SQLite file.

## Running the app

The frontend and backend run as two separate processes. In one terminal:

```bash
cd frontend
pnpm dev
```

Vite serves the app at http://localhost:5173.

In another terminal:

```bash
cd backend
uv run uvicorn app.main:app --reload
```

FastAPI serves the API at http://localhost:8000 (interactive docs at `/docs`).

## Testing

```bash
pnpm test                                    # frontend (Vitest), from repo root or frontend/
cd backend && uv run pytest                  # backend (pytest)
```

## Lint & format

```bash
pnpm lint / pnpm lint:fix                    # ESLint on frontend/, from repo root
pnpm format / pnpm format:check              # Prettier on frontend/, from repo root
cd backend && uv run ruff check              # backend lint
```

## Project structure

Single app layout (not a monorepo) — see [`AGENTS.md`](AGENTS.md) for full conventions:

- `frontend/` — React + Vite app ([`frontend/AGENTS.md`](frontend/AGENTS.md))
- `backend/` — FastAPI + SQLite service ([`backend/AGENTS.md`](backend/AGENTS.md))
- `docs/adr/` — architecture decision records

## Learn more

- [`AGENTS.md`](AGENTS.md) — project-wide conventions, stack, and build/test commands
- [`docs/adr/`](docs/adr/) — recorded architecture decisions (storage, stack, agent design)
