
## [Unreleased] — 2026-09-23 (assfix pass)

### Fixed
- CORS `allow_origins=["*"]` replaced with fleet standard (explicit origins +
  unconditional tailnet/LAN/Tauri regex) in both backends; MCP HTTP now serves
  the CORS-wrapped app via uvicorn instead of `mcp.run()` (which dropped middleware)
- Webapp backend route bundle: `/api/status`, `/api/capabilities`, `/api/metrics`,
  `/api/skills` (file-backed), `/api/llm/discover|providers|models|onboarding`,
  `POST /api/llm/chat` + `/stream` (Ollama proxy, honest 503 without LLM),
  `/api/v1/diagnostics`, `POST /api/shutdown`; hardcoded port 8000 removed
- Chat page uses the backend proxy + skill-first preprompt + LLM status indicator
- Dashboard reads real `/api/metrics` + `/api/logs` with loading/error/empty states
- Tests rewritten against the real tool API (18 pass, was 3 collection errors);
  fixed real bugs: missing `project_name` template context, Jinja/JSX `{{ }}`
  collision in `App.tsx.template`, unbound `pages_dir`/`component_code`/`hook_code`
- Agentic stub replaced with a deterministic planner; `get_help` lists real tools;
  safety guard has real session state
- Ruff: removed S110/S112 ignores (caught a silent bridge-proxy swallow), added T20;
  pyright 0 errors (was 20); removed dead `tools/scaffolding/` subtree
- Fleet-standard `start.ps1` (zombie clear, TCP readiness poll, WorkingDirectory);
  justfile core recipes (`serve|test|fmt|certify|e2e`) with single-line bodies
- Session injection: `.cursorrules` context, `.windsurfrules`, copilot instructions,
  `.claude-plugin` + `hooks/`; real AGENTS.md/CLAUDE.md; `.gitattributes` (LF)
- Five-gate CI (uv, ruff, pyright, pytest, biome, tsc) + renovate; pre-commit hook
  installed with scoped Biome gate; `.env.example`; glama.json refreshed

## [Unreleased] — 2026-06-14

### Added
- Tauri native wrapper (native/ directory) with bundle.resources + std::process::Command
- CUA-NSIS: just cua-nsis-test recipe, scripts/cua-smoke.py, scripts/cua-nsis-config.json
- Tauri CORS: tauri://localhost origins for WebView API access
- NSIS installer at dist/ and native/target/release/bundle/nsis/

### Changed
- Frontend API calls use absolute http://127.0.0.1:{port} URLs in production build
- CORS middleware includes allow_origin_regex for tauri.localhost
# Changelog

All notable changes to **Web Development MCP** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] / [0.2.0] — WITHDRAWN (cross-repo contamination)

> The 0.3.0 ("AI Construction System", `manage_object_construction`) and 0.2.0
> ("VR avatar tools", VRChat/VRM) entries previously listed here belonged to
> other repos' histories (Blender/avatar pipelines) and were never part of this
> web-scaffolding server. They were removed on 2026-09-23 rather than preserved
> as false history. If version archaeology is ever needed, consult git history,
> not this file.

## [0.1.0] - 2025-12-24

### Added
- Initial alpha release
- Basic Web Development connectivity
- Core MCP server implementation
- Development infrastructure (CI/CD, testing, documentation)

### Changed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- Basic security scanning implementation
- Input validation for MCP commands

---

## Release Process

### For Contributors
1. Update version in `src/web_development_mcp/__init__.py`
2. Update `CHANGELOG.md` with changes
3. Create pull request
4. CI/CD will handle the rest

### Automated Release
- Push to `main` triggers CI/CD pipeline
- Automatic version bumping available
- MCPB packages built and signed
- GitHub releases created with assets

### Version Types
- **PATCH** (`0.0.X`): Bug fixes, small improvements
- **MINOR** (`0.X.0`): New features, backwards compatible
- **MAJOR** (`X.0.0`): Breaking changes

---

## Types of Changes
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities

---

*This changelog follows the principles of [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).*
