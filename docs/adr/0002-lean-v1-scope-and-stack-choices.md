# ADR: Lean v1 Scope — Drop Offline Editing, Lock In Storage and Frontend Stack

**Status:** Accepted
**Date:** 2026-08-23
**Supersedes:** [ADR 0001](0001-block-storage-and-reconciliation.md) decisions #1, #3, #4, #5, #6, #7, #8. Decisions #2 (parent_id + content-array tree model) and #9 (agent operates on JSON, not markdown) remain in effect unchanged.

## Context

This project is primarily a vehicle for improving frontend engineering skill (with full-stack/backend as a secondary, supporting concern), building toward an AI-native note-taking app. ADR 0001 committed to Obsidian-style local-first markdown as the source of truth, editable outside the app — a requirement that forced a large, novel reconciliation apparatus (ID markers, change hashing, content/position-matching search, no-auto-reconstruction) to handle externally-edited files with unreliable IDs. That apparatus was hard to reverse, non-obvious to a future reader, and the result of a real trade-off, which is exactly why dropping it deserves its own recorded decision rather than a silent rewrite of ADR 0001.

## Decisions

### 1. Backend is the sole source of truth; no offline/external editing (supersedes #1)

The app requires a backend and is not designed to work fully offline or to have its stored notes edited by external tools. SQLite (via FastAPI, async) holds the canonical block tree.

**Rationale:** The offline/external-editability requirement was the sole reason for ADR 0001's reconciliation apparatus. Dropping it removes that entire problem rather than shrinking it, in exchange for requiring a server to use the app — an acceptable trade given the app was never going to be used without one in practice.

### 2. Markdown becomes a one-way, plain-CommonMark export (supersedes #4)

Users can export their notes to plain markdown at any time. Export is one-way generation only: re-importing an exported file always creates a new note, never updates or syncs into the note it came from.

**Rationale:** Notion's Enhanced Markdown spec (ADR 0001 #4) was chosen to support faithful round-tripping of externally-edited files. With round-tripping gone, export is a nice-to-have generation step, not a storage format — plain CommonMark is simpler and sufficient, at the cost of exotic block types (toggles, tables) losing fidelity on export.

### 3. Reconciliation apparatus removed entirely (supersedes #5, #6, #7, #8)

Visible ID markers, two-level file/block hashing for change detection, the content+position reconciliation search, and the no-auto-reconstruction policy are all removed — not simplified. There is no external editing path left for them to guard against.

**Rationale:** Each of these existed only in service of trusting an externally-editable file. Keeping any part of them without that requirement would be unused complexity.

### 4. Permission resolution out of scope for v1 (supersedes #3)

Iris is single-user for v1. Bottom-up permission resolution (nearest explicit override wins) is dropped from scope, not designed against.

**Rationale:** Sharing/collaboration was never a stated goal; permission resolution only matters once multiple users exist. Revisiting this later is a fresh design question, not a resumption of ADR 0001 #3 as-is.

### 5. Storage backend: SQLite (new)

**Rationale:** A real relational data layer via FastAPI gives genuine backend practice without the operational overhead (server process, connection pooling, migrations) of Postgres — appropriate given backend is secondary to the frontend skill focus.

### 6. Data model: normalized `blocks` table (new)

One row per block (`id`, `parent_id`, `position`, `type`, `props`), implementing the tree model from ADR 0001 decision #2 relationally.

**Rationale:** Maps cleanly onto agent tool calls (`createBlock`, `updateBlock`, `moveBlock` as row-level operations) and is a backend-internal choice that doesn't add frontend cost either way.

### 7. Frontend editor: BlockNote, with an independent backend schema (new)

The block editing UI is built on BlockNote (a Notion-style nested block editor for React) rather than hand-rolled or built on lower-level frameworks. The backend does not adopt BlockNote's internal schema: it keeps its own schema (decision #6), with a translation layer at the API boundary converting to/from BlockNote's format.

**Rationale:** BlockNote already implements the nesting/toggle/table primitives ADR 0001's block model calls for, freeing frontend effort for state management, agent-driven UI updates, and custom block rendering — the actual skill target. Keeping the backend schema independent (rather than mirroring BlockNote) preserves ADR 0001 decision #9: the agent's tool-call surface stays stable and defined by this project's own schema, not a frontend library's internal format, and survives a future editor-library swap.

## Considered and rejected

- **Postgres** — more realistic ops practice, but more setup overhead than the (secondary) backend focus justifies.
- **One JSON blob per note** instead of a normalized table — simpler to serialize, but a worse fit for row-level agent tool calls.
- **Tiptap/ProseMirror or Lexical**, hand-rolling nesting — more frontend learning value per line of code, but spends it re-deriving primitives BlockNote already solves, rather than on higher-level frontend work.
- **Mirroring BlockNote's schema in the backend** — less translation code, but couples the API and agent tool-calls to a specific frontend library's internal format.

## Deferred (carried forward from ADR 0001, still unresolved)

- **Agent context shape**: whether the agent reads raw JSON or a lighter, scoped serialized view. This was ADR 0001's own open question and is explicitly rolled into a future dedicated agent-architecture design session, not resolved here.
- **RAG/embedding update strategy** for agent context, carried forward from ADR 0001's deferred list for the same future session.

ADR 0001's other deferred items (AST-based tree comparison, distinguishing new-vs-ambiguous-match blocks, sync-blocking-vs-flagging) are not carried forward: they were only relevant to the reconciliation apparatus removed in decision #3 above, and have no remaining home.

## Consequences

- ADR 0001's reconciliation apparatus (#5–#8) is void, not simplified; none of its design should be resumed without a fresh ADR if offline/external editing is ever reconsidered.
- The block tree model (#2) and the agent's direct JSON read/write path (#9) are the only parts of ADR 0001 still fully in effect, and now sit inside a normalized SQLite table rather than a markdown-backed store.
- Every block edit crossing the BlockNote/backend boundary requires an explicit translation step; this is a deliberate, ongoing cost accepted to keep the agent's tool-call surface independent of the frontend editor library.
- Multi-user sharing is not designed against, just deferred; reintroducing it will need a fresh design pass rather than resuming ADR 0001 #3 unchanged against an SQLite, single-user-shaped schema.
