# ADR: Agent Architecture — LangGraph Tool-Calling Loop for the v1 Agent

**Status:** Accepted
**Date:** 2026-08-23
**Resolves:** ADR 0001's original open question (agent context shape) and ADR 0002's carried-forward deferred items (agent context shape, RAG/embedding strategy). ADR 0001 decision #9 (agent operates on JSON via defined tool functions, not markdown) remains in effect and is made concrete here.

## Context

ADR 0002 deferred the agent's own architecture to a dedicated design session, since it's a distinct design surface from block storage/editor choices. This ADR settles that: how the agent talks to the note, what it's allowed to do, and how results get back to the frontend. It also reflects a deliberate, stated goal — this piece is being built for hands-on LangChain/LangGraph experience relevant to job interviews, which shaped several choices below toward "idiomatic and representative of current practice" over "fastest to ship."

## Decisions

### 1. Autonomous execution, no human-in-the-loop approval

The agent calls its tools and they execute against the `blocks` table immediately; there is no approval/preview step before a tool call takes effect.

**Rationale:** An approval flow is a real feature but adds its own UI and state machine to build before the core loop is even proven to work. BlockNote's undo stack is the accepted safety net for v1, not an app-level confirmation gate.

### 2. LangGraph, not the legacy LangChain `AgentExecutor`

The tool-calling loop is built with LangGraph (e.g. a `create_react_agent`-style graph), hand-written rather than delegated to a black-box executor.

**Rationale:** LangChain's own guidance has moved tool-calling agents to LangGraph; `AgentExecutor` is legacy. Since the explicit goal is demonstrable, current LangChain-ecosystem experience, LangGraph is the more representative choice. Hand-writing the graph/nodes/tool-bindings (rather than using a higher-level executor) keeps the loop itself as hands-on learning rather than framework-provided plumbing.

### 3. Tool scope: single-note block CRUD only

The agent's tools for v1 are `createBlock`, `updateBlock`, `deleteBlock`, and `moveBlock`, all scoped to the note currently open in the frontend. No cross-note tools (e.g. `createNote`, `searchNotes`).

**Rationale:** Matches the v1 agent slice already committed to (agent reads and edits blocks). Cross-note tools would pull in the search/RAG question, which is explicitly out of scope (decision #5).

### 4. Context shape: raw JSON of the full note (resolves ADR 0001's open question)

The agent receives the full block tree of the currently open note as raw JSON — no scoping, windowing, or summarization.

**Rationale:** Notes are small enough for v1 that full-tree context is cheap. Scoped/windowed context solves a problem (large notes, token limits) this project doesn't have yet; revisit if a note grows large enough to make full-tree context expensive.

### 5. RAG/embeddings remain deferred

No retrieval or embedding infrastructure is built for v1, despite RAG being a common LangChain interview topic.

**Rationale:** Reconfirmed deliberately even given the interview-prep motivation: building RAG against a single-note agent with no cross-note search need would be a shallow implementation with no real design constraints (chunking strategy, re-indexing triggers, what to embed). The tool-calling loop itself already provides substantial, more differentiating LangGraph practice. Revisit once cross-note search is a genuine feature.

### 6. Stateless per-message handling

Each user message is handled independently — the message text plus the note's current block tree — with no LangGraph checkpointing or persisted conversation memory across turns.

**Rationale:** Same reasoning as RAG: memory/checkpointing is a separable LangGraph concept worth learning against an already-working baseline, not bundled into the first version.

### 7. Synchronous response delivery for v1

The full agent loop (LLM calls, tool execution) runs server-side per request; the response returns only once everything is done, containing all tool calls that were executed. The frontend applies them to BlockNote in one batch (e.g. via `editor.transact`).

**Rationale:** Avoids building a streaming transport (SSE/WebSocket) before the core loop is proven. Streaming so the user can watch the agent edit live is an explicit, planned follow-up, not abandoned — just not v1.

## Considered and rejected

- **Human-in-the-loop approval before tool execution** — rejected for v1 for the reason in decision #1; a real future feature, not a rejection forever.
- **Legacy `AgentExecutor`** — superseded by LangGraph in LangChain's own direction; less representative of current practice for the stated interview-prep goal.
- **Hand-rolled tool-calling loop against a raw provider SDK, bypassing LangChain** — rejected: the explicit goal is LangChain/LangGraph experience specifically, not just "an agent loop."
- **RAG pulled into v1 for practice value** — rejected per decision #5.
- **Streaming (SSE/WebSocket) for v1** — rejected for v1 per decision #7; planned as the next iteration once synchronous works end-to-end.

## Deferred

- **Streaming response delivery** — planned v2; transport (SSE vs. WebSocket) and event shape not decided here.
- **LLM provider/model selection** — a configuration detail, not an architectural one; decide at implementation time.
- **Multi-turn persisted memory / LangGraph checkpointing** — revisit if conversation continuity across turns becomes a real need.
- **RAG/embedding strategy** — still open, carried forward again; only becomes relevant alongside real cross-note search.

## Consequences

- Sending the full block tree on every message will not scale indefinitely; this is an accepted, revisitable trade-off, not an oversight.
- Because execution is autonomous and unapproved, the only recovery path for an unwanted agent edit is BlockNote's undo — there is no server-side "pending change" state to reject.
- Because the loop is stateless, every message must carry whatever context it needs; the agent has no memory of what it said or did in earlier turns of the same conversation.
- Choosing LangGraph and deliberately avoiding shortcuts (like `AgentExecutor` or a provider-agnostic abstraction) was optimized for learning/interview relevance specific to this project's purpose, not for minimizing implementation time — a different project without that goal might reasonably choose differently.
