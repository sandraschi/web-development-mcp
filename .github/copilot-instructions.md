# web-development-mcp Copilot instructions

## Session Context (web-development-mcp)

Before starting work: pull skill preprompt via `GET /api/skills` and call `list_available_frameworks` to confirm the scaffold surface. Never claim `create_svelte_app`/`create_next_app` — planned, not implemented.
Build with `configure_typescript` + `configure_vite` + `configure_biome`; components via `generate_react_component`/`generate_vue_component`; packages via `detect_package_manager` + `install_packages`.
At end of work: run `just certify` (ruff + pyright + pytest), sync README/CHANGELOG/llms-full.txt, never commit `.env`, `*.bak`, or `reports/`.
