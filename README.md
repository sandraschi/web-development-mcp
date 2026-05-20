# Web Development MCP 

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>

Universal web development operations MCP server supporting modern frontend frameworks, build tools, and development workflows.

## Austrian Dev Efficiency
One unified interface for entire web development stack - from project creation to deployment!

## Features

###  Project Scaffolding
- **React** - TypeScript + Vite + React Router + Testing Library
- **Vue 3** - TypeScript + Vite + Vue Router + Pinia + Vitest
- **SvelteKit** - TypeScript + SvelteKit routing + Vitest
- **Next.js** - TypeScript + App Router + Server Components
- **Vanilla TypeScript** - Modern TypeScript with Vite

###  Package Management
- **Multi-manager support** - npm, yarn, pnpm auto-detection
- **Dependency analysis** - Security audits and optimization
- **Smart updates** - Conflict resolution and compatibility checks
- **Bundle analysis** - Size optimization and tree-shaking

###  Build & Configuration
- **Vite optimization** - Lightning-fast development and builds
- **TypeScript setup** - Strict mode with path mapping
- **ESLint configuration** - Austrian dev standards with framework-specific rules
- **Testing setup** - Vitest + Testing Library + JSDOM

###  Code Generation
- **Smart components** - React/Vue components with TypeScript
- **Custom hooks** - State, effect, fetch, and storage hooks
- ** practices** - Consistent patterns and Austrian dev standards

##  Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

###  Quick Start
Run immediately via `uvx`:
```bash
uvx web-development-mcp
```

###  Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "web-development-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/web-development-mcp", "run", "web-development-mcp"]
  }
}
```
### For Cursor IDE

**Important:** Cursor uses system Python. Install dependencies in the Python that Cursor uses:

```powershell
# Find system Python path (check Cursor error logs if needed)
# Example: C:\Users\sandr\AppData\Local\Programs\Python\Python310\python.exe
python -m uv pip install -r requirements.txt
python -m uv pip install -e .
```

See `CURSOR_SETUP.md` for detailed Cursor configuration instructions.

### For Development

```powershell
cd d:\Dev\repos\web-development-mcp
uv venv
venv\Scripts\activate
uv pip install -r requirements.txt
uv pip install -e .
```

## Quick Start

```powershell
git clone https://github.com/sandraschi/web-development-mcp
cd web-development-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:
### 1. Create a New React Project
# List available frameworks
list_available_frameworks()
# Create React app with TypeScript
create_react_app(
project_name="my--app",
target_directory="./projects",
options={
"router": True,
"testing": True,
"eslint_strict": True
}
)
### 2. Package Management
# Auto-detect package manager
detect_package_manager("./my--app")
# Install packages
install_packages(
project_path="./my--app",
packages=["axios", "@tanstack/react-query"],
dev_dependencies=False
)
# Analyze project
analyze_package_json("./my--app")
### 3. Configure Development Tools
# Setup TypeScript with strict rules
configure_typescript(
project_path="./my--app",
strict_mode=True,
include_react=True
)
# Configure ESLint with Austrian standards
configure_eslint(
project_path="./my--app",
framework="react",
typescript=True,
strict_rules=True
)
# Optimize Vite configuration
configure_vite(
project_path="./my--app",
framework="react",
port=5173
)
### 4. Generate Components
# Generate React component
generate_react_component(
project_path="./my--app",
component_name="UserCard",
include_styles=True,
include_tests=True,
props_interface={
"name": "string",
"email": "string",
"avatar": "string"
}
)
# Generate custom hook
generate_custom_hook(
project_path="./my--app",
hook_name="useUserData",
hook_type="fetch"
)

## Available Tools

### Scaffolding Tools
- `list_available_frameworks` - Show supported frameworks and features
- `create_react_app` - Create React + TypeScript + Vite project
- `create_vue_app` - Create Vue 3 + TypeScript + Vite project  
- `create_svelte_app` - Create SvelteKit + TypeScript project (planned)
- `create_next_app` - Create Next.js + TypeScript project (planned)

### Package Tools  
- `detect_package_manager` - Auto-detect npm/yarn/pnpm
- `install_packages` - Install dependencies with smart defaults
- `update_packages` - Update packages with conflict resolution
- `analyze_package_json` - Security and compatibility analysis

### Build Tools
- `configure_typescript` - TypeScript setup with strict rules
- `configure_eslint` - ESLint + Austrian dev standards
- `configure_vite` - Vite optimization and development server
- `setup_testing_config` - Vitest + Testing Library setup

### Component Tools
- `generate_react_component` - Smart React component generation
- `generate_vue_component` - Vue 3 Composition API components  
- `generate_custom_hook` - React hooks (state, fetch, storage)

## Austrian Dev Standards

All generated code follows Austrian development efficiency principles:

- **TypeScript-first** - Strict typing by default
- **Modern tooling** - Vite, ESM, latest framework versions
- **Quality enforcement** - ESLint, Prettier, testing built-in
- **Performance focus** - Bundle optimization and tree-shaking
- **Developer experience** - Hot reload, source maps, debugging

## Framework Support Matrix

| Framework | Scaffolding | Components | Testing | Build Config |
|-----------|-------------|------------|---------|--------------|
| React     |           |          |       |            |
| Vue 3     |           |          |       |            |
| SvelteKit |  Planned  |  Planned |  Planned |  Planned |
| Next.js   |  Planned  |          |       |  Planned |

## Development

Built with FastMCP 3.1.0 for maximum compatibility and performance.


## 🛡️ Industrial Quality Stack

This project adheres to **SOTA 14.1** industrial standards for high-fidelity agentic orchestration:

- **Python (Core)**: [Ruff](https://astral.sh/ruff) for linting and formatting. Zero-tolerance for `print` statements in core handlers (`T201`).
- **Webapp (UI)**: [Biome](https://biomejs.dev/) for sub-millisecond linting. Strict `noConsoleLog` enforcement.
- **Protocol Compliance**: Hardened `stdout/stderr` isolation to ensure crash-resistant JSON-RPC communication.
- **Automation**: [Justfile](./justfile) recipes for all fleet operations (`just lint`, `just fix`, `just dev`).
- **Security**: Automated audits via `bandit` and `safety`.

## License

MIT License - See LICENSE file for details.


##  Webapp Dashboard

This MCP server includes a free, premium web interface for monitoring and control.
By default, the web dashboard runs on port **10852**.
*(Assigned ports: **10852** (Web dashboard frontend), **10853** (Web dashboard backend (API)))*

To start the webapp:
1. Navigate to the `webapp` (or `web`, `frontend`) directory.
2. Run `start.bat` (Windows) or `./start.ps1` (PowerShell).
3. Open `http://localhost:10852` in your browser.
