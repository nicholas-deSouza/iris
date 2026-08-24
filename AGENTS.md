# AGENTS.md

Single source of truth for project-wide agent instructions. This file says what to enforce.

## Project Overview

Iris is an AI-native note-taking app designed for seamless AI integration.

Personal, machine-local agent preferences may be kept in `AGENTS.local.md`. This
file is intentionally gitignored and should contain coaching preferences, not
shared project conventions.

## Stack

- **Frontend**: TypeScript + React — Modern reactive UI with type safety
- **Editor**: BlockNote — Notion-style nested block editing (frontend-owned; backend keeps its own independent schema, see ADR 0002)
- **Backend**: Python + FastAPI — High-performance async API framework
- **Storage**: SQLite — single-user v1, no offline/external-editing support (see ADR 0002)
- **Package Manager**: pnpm (>=10) — Fast, disk-efficient package management (specified in package.json)
- **Node**: >=22 — Required runtime version

## Architecture

Single app layout (not a monorepo).

- `frontend/` — React + Vite application (scaffolded)
  - Domain docs: `frontend/AGENTS.md`, `frontend/CLAUDE.md`
  - Communication with backend via REST API (details TBD)
- `backend/` — FastAPI service (scaffolded)
  - Domain docs: `backend/AGENTS.md`, `backend/CLAUDE.md`

Core data model and storage decisions are documented in [`docs/adr/0001-block-storage-and-reconciliation.md`](docs/adr/0001-block-storage-and-reconciliation.md) (JSON blocks, agent JSON access — decisions #2 and #9 still in effect), [`docs/adr/0002-lean-v1-scope-and-stack-choices.md`](docs/adr/0002-lean-v1-scope-and-stack-choices.md) (SQLite storage, BlockNote editor, single-user v1, one-way markdown export — supersedes ADR 0001's offline/reconciliation scope), and [`docs/adr/0003-agent-architecture.md`](docs/adr/0003-agent-architecture.md) (LangGraph tool-calling agent, single-note block CRUD tools, raw-JSON context, synchronous v1 response delivery).

## Build & Test

**Frontend** (from `frontend/`):

- `pnpm dev` — Vite dev server
- `pnpm build` — typecheck and production build
- `pnpm preview` — preview production build
- `pnpm test` — run Vitest once
- `pnpm test:watch` — Vitest in watch mode
- `pnpm test:coverage` — run with V8 coverage

`pnpm test` also works from the repo root (delegates to `frontend/`).

**Lint & format** (from repo root):

- `pnpm lint` / `pnpm lint:fix` — ESLint on `frontend/`
- `pnpm format` / `pnpm format:check` — Prettier on `frontend/`

Pre-commit hook (Husky + lint-staged) auto-fixes ESLint and Prettier on staged `frontend/**/*.{ts,tsx}` files.

**Backend** (from `backend/`, via `uv`):

- `uv run uvicorn app.main:app --reload` — dev server
- `uv run pytest` — run tests
- `uv run ruff check` — lint

Use `pnpm` (not npm/yarn) for all frontend package operations, and `uv` (not pip/poetry) for all
backend package operations.

## Code Standards

**Frontend**: ESLint (flat config at `eslint.config.mjs`) + Prettier (`.prettierrc`) at repo root, targeting `frontend/**/*.{ts,tsx}`. Configs use recommended TypeScript and React Hooks rules; Prettier handles formatting.

General expectations:

- Follow TypeScript/React best practices for frontend
- Follow Python/FastAPI conventions for backend
- Use existing code as reference for patterns

## Testing Requirements

**Frontend**: Vitest (config lives in `frontend/vite.config.ts` under `test`). Test globals are
disabled — import `describe`/`it`/`expect` from `vitest` explicitly. Colocate tests next to the code
they cover as `*.test.ts` / `*.test.tsx`.

**Backend**: pytest (config in `backend/pyproject.toml`).

Minimum expectations:

- Unit tests for business logic
- Integration tests for API endpoints
- Test coverage for critical user flows

Block-tree operations (create/insert/move/delete) must assert store invariants after every
operation — see [`docs/adr/0001-block-storage-and-reconciliation.md`](docs/adr/0001-block-storage-and-reconciliation.md)
Consequences, which requires multi-location writes to stay consistent.

## Security & Boundaries

- **Never commit secrets**: .env files are gitignored
- **API security**: Add authentication/authorization patterns during backend scaffolding
- **CORS policies**: Configure during frontend-backend integration
- **Input validation**: Validate at system boundaries (user input, external APIs)

## Working Agreement

- **Multi-file changes**: Use Plan Mode first, show plan before implementing
- **Task execution**: One task at a time, complete before moving to next
- **Commits**: Commit after each logical unit of work
- **Documentation**: Update AGENTS.md when architectural decisions are made
- **Domain instructions**: Create nested AGENTS.md + CLAUDE.md when adding backend/ or frontend/ folders

## Cursor Rules

Rules live in `.cursor/rules/` using `NNN-kebab-case` filenames.

- **001-project-guidelines** — always applies; imports this file
- **002-frontend** — `frontend/**/*`; imports `frontend/AGENTS.md`
- **003-backend** — `backend/**/*`; imports `backend/AGENTS.md`
- **000-guidelines-for-rule-creation** — read when creating or editing rules (see that file for full procedure)

**Maintenance**: Edit AGENTS.md for shared project truth; edit `.mdc` files only for Cursor-specific scoping.
