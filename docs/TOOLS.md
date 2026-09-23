# Tools — web-development-mcp (22 tools)

Scaffolding (`scaffolding_tools`):

| Tool | Args | Effect |
|---|---|---|
| `list_available_frameworks` | — | Framework catalogue with `available` flags (react/vue work; svelte/next/vanilla do NOT) |
| `create_react_app` | `project_name, target_directory, options?` | Scaffolds React+TS+Vite (+router/testing by default) |
| `create_vue_app` | `project_name, target_directory, options?` | Scaffolds Vue 3+TS+Vite (+router/pinia/testing) |

Packages (`package_tools`):

| Tool | Args | Effect |
|---|---|---|
| `detect_package_manager` | `project_path` | Lockfile detection, bun > pnpm > yarn > npm (read-only) |
| `install_packages` | `project_path, packages, package_manager?, dev_dependencies?` | Runs the real install subprocess |
| `update_packages` | `project_path, packages?, package_manager?, check_only?` | Updates (or `check_only` outdated report, read-only) |
| `remove_packages` | `project_path, packages, package_manager?` | Uninstalls (DESTRUCTIVE) |
| `analyze_package_json` | `project_path` | Dep counts, framework/build-tool detection, vuln flags (read-only) |

Build (`build_tools`):

| Tool | Args | Effect |
|---|---|---|
| `configure_typescript` | `project_path, strict_mode?, target?, include_react?` | Writes `tsconfig.json` |
| `configure_biome` | `project_path, framework?, typescript?, strict_rules?` | Writes `biome.json` (replaces ESLint+Prettier) |
| `configure_vite` | `project_path, framework?, port?, enable_https?` | Writes `vite.config.ts` (pass the project's own port) |
| `setup_testing_config` | `project_path, framework?, test_runner?` | Writes `vitest.config.ts` + `src/test/setup.ts` |

Components (`component_tools`):

| Tool | Args | Effect |
|---|---|---|
| `generate_react_component` | `project_path, component_name, ...` | React component + styles + tests |
| `generate_vue_component` | `project_path, component_name, composition_api?, ...` | Vue SFC (Composition API only) |
| `generate_custom_hook` | `project_path, hook_name, hook_type?` | React hook (`state`, `effect`, `fetch`, `storage` only) |
| `setup_tailwind` | `project_path, ...` | Tailwind baseline |
| `setup_shadcn` | `project_path, ...` | shadcn/ui library |
| `scaffold_dashboard` | `project_path, ...` | Full dashboard scaffold |

Agentic / maintenance / meta:

| Tool | Args | Effect |
|---|---|---|
| `agentic_workflow_tool` | `goal` | Deterministic plan of real tool calls (mode=plan, executes nothing) |
| `toggle_safety_guard` | `enabled` | Session safety-guard state |
| `shutdown_server` | `delay_seconds?` | Graceful process exit (DESTRUCTIVE) |
| `get_help` | `category?, tool_name?, level?` | Tool documentation by category |

Unknown enum values (bad `hook_type`, `composition_api=False`, bad project
names) return explicit `{success: False, error, message}` — never a crash,
never fake success.
