# Iris

AI-native note-taking app: nested block editing with an AI agent that can read and edit notes directly.

## Language

**Export**:
A one-way generation of the current block tree to a plain markdown file. Re-importing an exported file always creates a new note; it never updates or syncs back into the note it came from.
_Avoid_: sync, save, round-trip (these imply a bidirectional update, which Export explicitly is not)
