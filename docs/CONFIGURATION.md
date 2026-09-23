# Configuration — web-development-mcp

All configuration is environment variables (see `.env.example`; never commit `.env`).

## MCP transport

| Variable | Default | Meaning |
|---|---|---|
| `MCP_TRANSPORT` | `stdio` | `stdio` (Claude Desktop), `http`, or `sse` (deprecated) |
| `MCP_HOST` | `127.0.0.1` | Bind address for http/sse |
| `MCP_PORT` | `10853` | Port for http/sse |
| `MCP_PATH` | `/mcp` | HTTP endpoint path |
| `MCP_BRIDGE_URLS` | _(empty)_ | Comma-separated URLs of other MCP servers to proxy tools from |

CLI flags (`--stdio`, `--http`, `--sse`, `--host`, `--port`, `--path`, `--debug`)
override the environment. See `src/web_development_mcp/transport.py`.

## Webapp ports (fleet registry: `mcp-central-docs/operations/WEBAPP_PORTS.md`)

| Variable | Default | Meaning |
|---|---|---|
| `WEB_PORT` | `10853` | Uvicorn backend (`web_sota/backend`, `server:app`) |
| `VITE_PORT` / `WEB_FRONTEND_PORT` | `10852` | Vite frontend (`web_sota`) |
| `VITE_API_TARGET` | `http://127.0.0.1:10853` | Backend URL baked into the frontend |

`fleet-start.config.ps1` is the source of truth for the fleet launcher
(`Kind = 'uvicorn-web-app'`, `UvicornTarget = 'server:app'`, `HealthPath = '/health'`).

## LLM providers (server-side only)

| Variable | Meaning |
|---|---|
| `OPENAI_API_KEY` | Enables the OpenAI `configured` flag in `/api/llm/providers` |
| `ANTHROPIC_API_KEY` | Enables the Anthropic `configured` flag |

Local providers need no keys: Ollama (`127.0.0.1:11434`) and LM Studio
(`127.0.0.1:1234`) are probed live by `GET /api/llm/discover`. Keys never
leave the server — the frontend only talks to the backend proxy.

## CORS

Explicit origins (frontend/backend localhost ports + Tauri schemes) plus an
unconditional tailnet/LAN/Tauri regex — see `mcp-central-docs/standards/CORS_STANDARD.md`.
Never `allow_origins=["*"]` (browsers reject it with `allow_credentials=True`).
