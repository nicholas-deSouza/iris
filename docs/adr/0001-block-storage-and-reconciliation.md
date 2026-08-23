# ADR: Block Storage, Markdown Serialization, and Reconciliation Strategy

**Status:** Partially superseded by [ADR 0002](0002-lean-v1-scope-and-stack-choices.md) — decisions #1, #3, #4, #5, #6, #7, #8 below no longer apply; decisions #2 and #9 remain in effect.
**Date:** 2026-08-11
**Context:** Notes app combining Notion-style nested block editing with Obsidian-style local markdown storage and graph linking, designed to be readable/editable by AI agents.

## Context

The app needs to support:
- Rich, nested block structures (toggles, tables, headers, databases) like Notion
- Local-first storage as plain markdown files, editable outside the app, like Obsidian
- Graph-based linking between notes
- AI agents reading and editing notes directly, operating against the app's live JSON block structure rather than markdown, while the app is open

These requirements are partially in tension: a rich nested block tree needs structured relationship data (parent/child, ordering) that plain markdown has no native way to express, and allowing external edits means the app can never fully trust that its stored structure still matches the file on disk.

## Decisions

### 1. Dual representation: JSON as source of truth, markdown as on-disk format

Blocks are stored as JSON internally (the app's structured source of truth for rendering, relationships, and permissions), and serialized to markdown for on-disk storage, portability, and agent readability.

**Rationale:** Matches the requirement that files be plain, portable markdown, while preserving Notion-style nested structure that markdown alone can't express. Reference precedent: SiYuan pairs markdown with JSON metadata, though SiYuan's native storage is actually JSON-AST with markdown as an export format only — we are taking the opposite stance (markdown as the real on-disk source of truth) because agent-readability and external editability are hard requirements for this app.

### 2. Block relationships modeled via parent pointer + content array (tree structure)

Each block has a `parent_id` (upward pointer) in addition to a `content` array of child block IDs (downward pointer), mirroring Notion's own data model.

**Rationale:** A single downward-only pointer structure makes ancestor lookups (e.g., permission resolution) O(n × d) in the worst case (n = total blocks, d = tree depth), since finding a parent requires scanning all blocks. Adding a direct parent pointer reduces ancestor traversal to O(d). This tradeoff costs additional storage per block but is necessary for permission checks and reconciliation to be performant at scale.

### 3. Permission resolution: bottom-up traversal, nearest explicit override wins

To resolve a block's permissions, traverse from the block upward via `parent_id` and stop at the first ancestor with an explicit permission setting. Blocks without their own explicit setting are transparent/pass-through.

**Rationale:** Matches how sharing actually needs to work (e.g., a private workspace can still have one page explicitly shared out). Bottom-up traversal is the only direction that both implements "nearest override wins" correctly and allows early-exit (stopping at the first explicit setting) rather than always walking the full depth.

### 4. Markdown serialization format: Notion's Enhanced Markdown

Adopt Notion's own Enhanced Markdown spec (XML-like tags and attribute lists, e.g. `<details>`/`<summary>` for toggles, `<table>` with attributes) as the block-to-markdown mapping, rather than inventing a custom syntax.

**Rationale:** Since the app's block types are explicitly modeled on Notion's, reusing their existing, documented spec avoids re-deriving a mapping from scratch and provides a reference implementation to build against (developers.notion.com/guides/data-apis/enhanced-markdown).

### 5. Block identity: visible ID marker, not hidden

Each block carries a visible ID (e.g., in an attribute or comment-style marker within its markdown) rather than attempting to hide it. True hiding was determined to be infeasible for a local plain-text file — any marker embedded in a file the user can freely edit is discoverable and editable, whether intentionally or not.

**Rationale:** Instead of trying to prevent ID tampering (not achievable locally), the design accepts that IDs can be lost or corrupted and focuses on detection and recovery.

### 6. Change detection: two-level hashing (file, then block)

Compute a whole-file hash first as a cheap check for whether anything in a file changed at all. Only if the file hash changed, compute per-block hashes to identify which specific block(s) changed.

**Rationale:** Avoids re-parsing and reconciling unchanged files, and avoids reconciling every block in a file when only one changed. Conceptually similar to a Merkle tree / how Git detects changed files in a commit.

### 7. Reconciliation strategy for blocks with unreliable IDs

When a block's ID marker doesn't match its own snapshot (missing, deleted, or changed to collide with a different block's ID), the ID is treated as untrustworthy. The app then searches across known snapshots using two signals:

- **Content similarity** — does this block's text resemble a known snapshot's text?
- **Tree position** (via AST comparison of parsed markdown structure — parent, siblings, depth) — does this block's position in the structure resemble a known snapshot's position?

Decision rule: **for any block with an ID, first check it against that ID's own snapshot (content + position). If it matches, trust it. If it doesn't match, treat the ID as unreliable and run the full content+position search across snapshots instead of trying to distinguish further sub-cases (missing vs. colliding ID).**

This single rule covers what were initially identified as five separate scenarios (missing ID, colliding ID, block moved, block heavily edited, block moved-and-edited) — the two signals compensate for each other's blind spots (content similarity catches moved-but-similar blocks; tree position catches static-but-heavily-edited blocks).

**Rationale:** No existing reference implementation was found solving this exact combination of problems (markdown-as-source-of-truth + rich nested relationships + externally editable files). Apple Notes sync tools (e.g. `stash`) solve a simpler version with no nested relationships. SiYuan has nested relationships but avoids the problem by not exposing markdown as the directly-editable source of truth. This is a novel design decision for this project rather than a borrowed pattern.

### 8. No automatic structural reconstruction on ambiguous match

When neither content nor tree-position signals produce a confident match, the app does not attempt to automatically rebuild structure (e.g., auto-creating a new container block to preserve grouping, or promoting orphaned children to a grandparent). Instead, this is surfaced to the user for resolution.

**Rationale:** Automatic reconstruction (e.g., synthesizing a new toggle to hold orphaned children) adds significant complexity and risks silently altering user-intended structure. Following the precedent of simpler tools (e.g. Apple Notes sync asking the user rather than guessing), ambiguous cases are deferred to explicit user decision rather than automated inference.

### 9. Agent operates directly on JSON, not markdown

While the app is running, the AI agent reads and writes the block structure via the JSON representation directly — not via markdown, and not via a markdown round-trip. The agent is given a defined set of tools/functions mirroring the JSON block schema (e.g. `updateBlock`, `moveBlock`, `createBlock`), consistent with how LLM function calling / tool use works: the model outputs a structured call matching a defined schema, and the app executes it against the real data structure. The model does not parse or generate markdown as an intermediate step for in-app interactions.

**Rationale:** Converting JSON to markdown and back on every agent read/write adds unnecessary latency and an unnecessary lossy round-trip, since the agent is operating inside the app where JSON is already the live source of truth. Markdown's role remains the on-disk/portability/external-editing format (decisions #1, #5–#8); the agent's read/write path is a separate concern from that. Because the agent calls defined functions using the app's real block IDs directly, it does not trigger the ID-loss/collision problem described in decision #7 — that failure mode is specific to direct, unstructured external edits to the markdown file itself, not to agent-driven edits through the app.

**Open question:** when the agent needs read context, does it receive raw JSON, or a lighter serialized view of the JSON (still not markdown) scoped to what's relevant to the query? Not yet decided.

## Deferred / Explicitly Out of Scope for v1

- AST-based tree comparison for reconciliation — full implementation deferred until after the core block editor and markdown serialization are working; treated as infrastructure to build once the core data model is stable.
- Distinguishing "brand new block" (no prior snapshot exists at all) from "ambiguous match to an existing block" as separate handling paths.
- Whether sync should block until the user resolves an ambiguous reconciliation, or proceed with the affected block(s) flagged — not yet decided.
- RAG/embedding update strategy for agent context (incremental re-embedding on file change, using block boundaries as chunk boundaries) — identified as a related but separate problem, not addressed in this ADR.

## Consequences

- Every block move or edit potentially requires multi-location writes (parent pointer + old parent's content array + new parent's content array) that must stay consistent — this mirrors the same consistency requirement Notion's own architecture has, and will need a transaction-like mechanism.
- Because markdown is the real source of truth on disk (not JSON-AST like SiYuan), the app inherently accepts a nonzero risk of unresolvable reconciliation cases and must have a clear UX path for surfacing them to the user.
- Choosing Notion's Enhanced Markdown format ties the app's on-disk format to a spec the team doesn't control; changes to Notion's spec don't need to be followed, but deviating from it later would require a migration story.
