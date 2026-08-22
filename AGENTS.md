# AGENTS.md

Single source of truth for project-wide agent instructions. This file says what to enforce.

## Project Overview

Iris is an AI-native note-taking app designed for seamless AI integration.

## Stack

- **Frontend**: TypeScript + React — Modern reactive UI with type safety
- **Backend**: Python + FastAPI — High-performance async API framework
- **Package Manager**: pnpm (>=10) — Fast, disk-efficient package management (specified in package.json)
- **Node**: >=22 — Required runtime version

## Architecture

Single app layout (not a monorepo).

- `frontend/` — React + Vite application (scaffolded)
  - Domain docs: `frontend/AGENTS.md`, `frontend/CLAUDE.md`
  - Communication with backend via REST API (details TBD)
- `backend/` — FastAPI service (not yet created)

## Build & Test

**Frontend** (from `frontend/`):

- `pnpm dev` — Vite dev server
- `pnpm build` — typecheck and production build
- `pnpm preview` — preview production build

**Lint & format** (from repo root):

- `pnpm lint` / `pnpm lint:fix` — ESLint on `frontend/`
- `pnpm format` / `pnpm format:check` — Prettier on `frontend/`

Pre-commit hook (Husky + lint-staged) auto-fixes ESLint and Prettier on staged `frontend/**/*.{ts,tsx}` files.

**Backend** (not yet configured):

- `uvicorn app.main:app --reload`, `pytest`, `ruff check`

Use `pnpm` (not npm/yarn) for all frontend package operations.

## Code Standards

**Frontend**: ESLint (flat config at `eslint.config.mjs`) + Prettier (`.prettierrc`) at repo root, targeting `frontend/**/*.{ts,tsx}`. Configs use recommended TypeScript and React Hooks rules; Prettier handles formatting.

General expectations:

- Follow TypeScript/React best practices for frontend
- Follow Python/FastAPI conventions for backend
- Use existing code as reference for patterns

## Testing Requirements

_To be defined during scaffolding._

Minimum expectations:

- Unit tests for business logic
- Integration tests for API endpoints
- Test coverage for critical user flows

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
- **000-guidelines-for-rule-creation** — read when creating or editing rules (see that file for full procedure)

Reserved for scaffolding: `003-backend`.

**Maintenance**: Edit AGENTS.md for shared project truth; edit `.mdc` files only for Cursor-specific scoping.
