# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Iris is an AI-native note-taking app.

This repository currently contains no code — it is a fresh project. The intended architecture is:

- **Frontend**: TypeScript + React
- **Backend**: Python + FastAPI
- **Layout**: single app (not a monorepo with multiple deployable apps)

The frontend uses **pnpm** as the package manager (`packageManager` in `package.json`). Use `pnpm` for install and scripts, not npm or yarn.

No build, lint, or test tooling is set up yet. Once the frontend and backend are scaffolded, this file should be updated with the actual commands (dev server, build, lint, test — both `pnpm` scripts for the frontend and the Python tooling used for the backend, e.g. `uvicorn`, `pytest`, `ruff`) and with real architectural notes (how the frontend and backend communicate, where API routes and React components live, any shared types, data storage, etc.).
