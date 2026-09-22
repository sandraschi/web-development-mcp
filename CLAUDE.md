# CLAUDE.md — web-development-mcp

Per-repo agent instructions (fleet standard). Claude Code and opencode both read this.

## What this repo is

Standard MCP server (FastMCP `>=3.4.4,<4`) for web development operations:
project scaffolding (React/Vue), package management (npm/yarn/pnpm/bun),
build configuration (TypeScript/Vite/Biome/Vitest), component generation,
plus a `web_sota` React dashboard and a Tauri `native/` shell.

## Entry points

- MCP server: `src/web_development_mcp/mcp_server.py` (`main()`), transports in `transport.py`
- CLI: `src/web_development_mcp/cli.py`
- Dashboard backend: `web_sota/backend/server.py` (`server:app`, port 10853)
- Dashboard frontend: `web_sota/src` (Vite, port 10852, `VITE_API_TARGET` env)
- Tools: `src/web_development_mcp/tools/` — 21 tools across 7 modules

## Must-know standards

- `mcp-central-docs/standards/TOOL_DESIGN_STANDARDS.md` — portmanteau pattern, dialogic returns
- `mcp-central-docs/standards/rules/docstrings_sota.md` — Annotated+Field, Return Format, Examples
- `mcp-central-docs/standards/CORS_STANDARD.md` — explicit origins + regex, never `["*"]`
- Port registry: `mcp-central-docs/operations/WEBAPP_PORTS.md` (10852/10853)

## Key files

`justfile` (`serve|lint|fix|fmt|test|certify|e2e`) · `start.ps1` · `fleet-start.config.ps1` ·
`pyproject.toml` (ruff T20 enforced; S110/S112 never ignored) · `glama.json` (tool list) ·
`skills/webdev-expert/SKILL.md` (chat preprompt source) · `reports/assess-*.md` (audit trail)

## Gotchas

- Jinja templates vs JSX: `{{ }}` collides with framer-motion props — use `{% raw %}` blocks
  (see `templates/react/src/App.tsx.template`); template context needs `project_name` (StrictUndefined)
- `just` runs each recipe line as its own process — single-line recipe bodies with absolute paths
- SvelteKit/Next.js scaffolds are planned, NOT implemented — never advertise them as working
