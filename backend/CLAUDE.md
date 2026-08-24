# CLAUDE.md

@AGENTS.md

## Claude-specific

- For multi-file backend changes (new models, new endpoints touching several routers/services):
  use Plan Mode first when scope is unclear.
- Keep routers thin; put logic in service functions so agent tools (ADR 0003) can call the same
  code paths.
