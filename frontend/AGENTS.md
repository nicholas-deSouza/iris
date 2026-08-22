# frontend/AGENTS.md

Frontend conventions for the Iris React application.

## Stack

- **Vite** — dev server and production build
- **React 19** — UI components
- **TypeScript** — type-safe application code

## Layout

```
frontend/
├── src/           # Application source (components, hooks, pages)
├── index.html     # Vite entry HTML
├── vite.config.ts
└── tsconfig*.json
```

## Commands

Run from `frontend/`:

- `pnpm dev` — start Vite dev server
- `pnpm build` — typecheck and production build
- `pnpm preview` — preview production build locally

Lint and format run from the **repo root** (`pnpm lint`, `pnpm format`).

## Conventions

- Use functional React components with hooks
- Colocate component-specific styles and tests near their components
- Prefer named exports for components; default export only for pages/routes when needed
- Communicate with the backend via REST API (details TBD during integration)

## Code Standards

- ESLint and Prettier configs live at the repo root; they target `frontend/**/*.{ts,tsx}`
- Pre-commit hook auto-fixes lint and format on staged TypeScript files
- Follow existing patterns in `src/` when adding new code
