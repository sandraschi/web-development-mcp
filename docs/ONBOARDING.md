# Onboarding — web-development-mcp

## What this server needs from you

No wrappee to install (it scaffolds projects itself). What it needs is an LLM
for the Chat page and a few minutes:

1. **Install a local LLM (free)** — Ollama (`ollama serve`, pull any model,
   serves on `127.0.0.1:11434`) or LM Studio (serves on `127.0.0.1:1234`).
   No account, no credit card, everything stays on your machine.
2. **Or configure cloud (paid)** — put `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
   in the server environment (`.env`, never the browser). Needs an account
   with billing enabled on the provider side.
3. **Start the stack**: `just serve` (backend :10853, frontend :10852).

## Sanity check (2 minutes)

1. Open the dashboard — status dot green, metrics live.
2. `GET /api/llm/discover` (or the Chat page's LLM indicator) shows your
   provider as detected.
3. Chat: ask "scaffold a React app" — with no LLM running you get an honest
   503 telling you exactly what to start (that message IS the check).

## Pitfalls

- Chat without any LLM returns 503 by design — it never fakes an answer.
- Only `react` and `vue` scaffolds exist; `list_available_frameworks` marks
  the rest `"available": false`. Asking for Svelte/Next.js gets an explicit
  refusal, not a broken project.
- If the dashboard shows MOCK-free real data from the first second, onboarding
  succeeded: the under-hero cue disappears once a provider is detected (or
  after you click "Mark onboarded" — stored in `localStorage`).
