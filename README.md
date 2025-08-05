# Web Development MCP 🌐

Universal web development operations MCP server supporting modern frontend frameworks, build tools, and development workflows.

## Austrian Dev Efficiency
One unified interface for entire web development stack - from project creation to deployment!

## Features

### 🚀 Project Scaffolding
- **React** - TypeScript + Vite + React Router + Testing Library
- **Vue 3** - TypeScript + Vite + Vue Router + Pinia + Vitest
- **SvelteKit** - TypeScript + SvelteKit routing + Vitest
- **Next.js** - TypeScript + App Router + Server Components
- **Vanilla TypeScript** - Modern TypeScript with Vite

### 📦 Package Management
- **Multi-manager support** - npm, yarn, pnpm auto-detection
- **Dependency analysis** - Security audits and optimization
- **Smart updates** - Conflict resolution and compatibility checks
- **Bundle analysis** - Size optimization and tree-shaking

### 🔧 Build & Configuration
- **Vite optimization** - Lightning-fast development and builds
- **TypeScript setup** - Strict mode with path mapping
- **ESLint configuration** - Austrian dev standards with framework-specific rules
- **Testing setup** - Vitest + Testing Library + JSDOM

### ✨ Code Generation
- **Smart components** - React/Vue components with TypeScript
- **Custom hooks** - State, effect, fetch, and storage hooks
- **Best practices** - Consistent patterns and Austrian dev standards

## Quick Start

### 1. Create a New React Project
```python
# List available frameworks
list_available_frameworks()

# Create React app with TypeScript
create_react_app(
    project_name="my-awesome-app",
    target_directory="./projects",
    options={
        "router": True,
        "testing": True,
        "eslint_strict": True
    }
)
```

### 2. Package Management
```python
# Auto-detect package manager
detect_package_manager("./my-awesome-app")

# Install packages
install_packages(
    project_path="./my-awesome-app",
    packages=["axios", "@tanstack/react-query"],
    dev_dependencies=False
)

# Analyze project
analyze_package_json("./my-awesome-app")
```

### 3. Configure Development Tools
```python
# Setup TypeScript with strict rules
configure_typescript(
    project_path="./my-awesome-app",
    strict_mode=True,
    include_react=True
)

# Configure ESLint with Austrian standards
configure_eslint(
    project_path="./my-awesome-app",
    framework="react",
    typescript=True,
    strict_rules=True
)

# Optimize Vite configuration
configure_vite(
    project_path="./my-awesome-app",
    framework="react",
    port=5173
)
```

### 4. Generate Components
```python
# Generate React component
generate_react_component(
    project_path="./my-awesome-app",
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
    project_path="./my-awesome-app",
    hook_name="useUserData",
    hook_type="fetch"
)
```

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
| React     | ✅          | ✅         | ✅      | ✅           |
| Vue 3     | ✅          | ✅         | ✅      | ✅           |
| SvelteKit | 📋 Planned  | 📋 Planned | 📋 Planned | 📋 Planned |
| Next.js   | 📋 Planned  | ✅         | ✅      | 📋 Planned |

## Development

Built with FastMCP 2.10 for maximum compatibility and performance.

## License

MIT License - See LICENSE file for details.
