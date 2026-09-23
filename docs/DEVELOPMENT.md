# Development — web-development-mcp

## Setup

```powershell
uv sync --group dev   # or: just bootstrap  (also installs the pre-commit hook)
```

Python 3.12+, `uv` for deps, `just` for recipes, `ruff` + `pyright` for Python,
`npm` + Biome + `tsc` for `web_sota/`.

## Recipes (`justfile`)

| Recipe | What it runs |
|---|---|
| `just serve` | Full stack via `start.ps1` (backend :10853 + frontend :10852) |
| `just lint` | `ruff check` + `ruff format --check` + `biome ci web_sota` |
| `just fix` / `just fmt` | Auto-fix + format (Python and web) |
| `just test` | `pytest tests/ -q` |
| `just certify` | ruff + format-check + pyright + pytest (mirrors CI) |
| `just e2e` | Browser walk (`scripts/just/cua-webapp-test.ps1`, needs `just serve`) |
| `just build-native` | Tauri NSIS pipeline |

Recipe bodies are single-line with absolute paths: `just` runs each line as
its own process, so `Set-Location` on its own line never persists.

## Testing

```powershell
uv run pytest tests/ -q
```

Tests call the REAL registered tool functions (via a minimal `FakeMCP`
collector) into `tmp_path` — no mocks of tool behavior. Coverage: scaffolding,
packages, build-config, agentic planner.

## Conventions

- Tool docstrings: `Annotated[..., Field(description=...)]` params (no `Args:`
  blocks), `## Return Format`, `## Examples` sections.
- Dialogic returns: every tool returns `{success, message, ...}`.
- Annotations on `@mcp.tool()`: `{"readonly": True}` / `{}` / `{"destructive": True}`.
- Jinja templates vs JSX: `{{ }}` collides with framer-motion props — use
  `{% raw %}` blocks; templates render under `StrictUndefined`, so every
  `{{name}}` must exist in the context (see `process_template_file`).
- Commits: max 5 files each; 3+ file edits need timestamped `.bak` first
  (gitignored); never commit `.env`, `*.bak`, `reports/`.
