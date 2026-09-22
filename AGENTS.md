# web-development-mcp Agent Context

Fleet Standard MCP server (FastMCP 3.4): React/Vue scaffolding, package
management, Vite/TS/Biome config, component generation + `web_sota` dashboard.

## Quick Ref

```powershell
just serve      # backend :10853 + frontend :10852
just lint       # ruff + biome ci
just test       # pytest tests/ -q
just certify    # ruff + format-check + pyright + pytest (mirrors CI)
uv run pytest tests/ -q
```

## Entry points

- `src/web_development_mcp/mcp_server.py` — FastMCP instance + tool registration (`main()`)
- `src/web_development_mcp/transport.py` — stdio/http/sse runner (fleet CORS + uvicorn)
- `src/web_development_mcp/server.py` — stdio entry + ASGI app for uvicorn
- `src/web_development_mcp/cli.py` — CLI (prints allowed here via ruff per-file-ignores)
- `src/web_development_mcp/tools/` — 7 modules, 21 tools (register via `register_tools(mcp)`)
- `web_sota/backend/server.py` — dashboard REST backend (`server:app`: health, status,
  capabilities, metrics, logs, skills, llm/*, diagnostics, shutdown)
- `web_sota/src/` — React + Vite + Tailwind dashboard (API via `VITE_API_TARGET`)

## Standards

- Ports: backend 10853, frontend 10852 (registry: `mcp-central-docs/operations/WEBAPP_PORTS.md`)
- CORS: explicit origins + unconditional tailnet/LAN/Tauri regex — never `["*"]`
- Tool docstrings: `Annotated[..., Field(description=...)]` params, `## Return Format`, `## Examples`
- No stubs: every advertised op works; `create_svelte_app`/`create_next_app` are NOT implemented — never claim them
- Session context: `.cursorrules` / `.windsurfrules` / `.github/copilot-instructions.md` /
  `.claude-plugin/plugin.json` + `hooks/hooks.json` (keep tool names in sync with `glama.json`)
- ≤5 files per commit; 3+ file edits need timestamped `.bak` first (gitignored)
