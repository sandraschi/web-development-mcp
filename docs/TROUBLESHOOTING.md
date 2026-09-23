# Troubleshooting — web-development-mcp

## Dashboard shows "Backend unreachable"

1. Is the backend up? `Invoke-WebRequest http://127.0.0.1:10853/api/health -UseBasicParsing`
2. Port zombie? `Get-NetTCPConnection -LocalPort 10853` → `Stop-Process -Id <pid> -Force`.
   `start.ps1` clears zombies itself — prefer `just serve`.
3. Browser CORS error ("Failed to fetch") but curl works: CORS is browser-only.
   Check the request `Origin` against `_CORS_ORIGINS`/`_CORS_REGEX` in
   `web_sota/backend/server.py` (fleet CORS standard).

## Chat answers "No local LLM detected"

Start Ollama (`ollama serve`, models on :11434) or LM Studio (:1234), then
re-check `GET /api/llm/discover`. Cloud keys go in the server env
(`OPENAI_API_KEY` / `ANTHROPIC_API_KEY`), never in the browser.

## Scaffolding fails with "project_name is undefined" (or Jinja errors)

Fixed in 2026-09: the render context always carries `project_name`, and
`App.tsx.template` wraps framer-motion `{{ }}` in `{% raw %}`. If you add a
template, remember: Jinja `{{ }}` collides with JSX double braces, and
`StrictUndefined` raises on any missing variable.

## `pytest` collection errors after adding a tool

Tests import the REAL functions: module-level helpers directly, closure tools
via the `FakeMCP` collector pattern (see `tests/test_build_tools.py`). If you
move a tool, update the corresponding test import.

## Biome CI fails on untouched pages

Tree-wide Biome debt is being cleaned file by file. The pre-commit hook only
gates files YOU changed — run `just fix` (scoped) rather than reformatting
the world in one commit (5-file rule).

## `git push` rejected on `.github/workflows/ci.yml`

GitHub refuses workflow updates from tokens without the `workflow` scope:
`gh auth refresh -s workflow`, then push again.
