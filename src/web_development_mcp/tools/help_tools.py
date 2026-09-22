"""
Help and documentation tools for Web Development MCP.
Provides contextual assistance for the entire web development stack.
"""

from typing import Any

from fastmcp import FastMCP

from .utils import _error_response, _success_response


def register_tools(mcp: FastMCP):
    """Register help tools with the FastMCP instance."""

    @mcp.tool()
    async def get_help(
        category: str | None = None,
        tool_name: str | None = None,
        level: str = "basic",
    ) -> dict[str, Any]:
        """Get documentation for Web Development MCP tools.

        ## Return Format

        `{success, data}` where data holds `level`, `categories`, and —
        when a category is given — the real registered tool names in it.

        ## Examples

        - category="scaffolding" -> list_available_frameworks, create_react_app, create_vue_app.
        - category="package" -> detect_package_manager, install_packages, update_packages, ...
        - No args -> the five category summaries.
        """
        try:
            help_info = {
                "level": level,
                "categories": {
                    "scaffolding": "Project creation and framework setup",
                    "package": "Dependency and package management",
                    "build": "Build processes and configuration",
                    "component": "Component generation and templates",
                    "sampling": "Agentic orchestration and autonomous workflows (SEP-1577)",
                },
            }

            if category == "sampling":
                help_info["tools"] = {
                    "agentic_workflow_tool": "Autonomous web development orchestration",
                    "toggle_safety_guard": "Manage agentic safety session",
                }
                help_info["details"] = await _get_sampling_help(level)
            elif category == "scaffolding":
                help_info["tools"] = {
                    "list_available_frameworks": "Show supported frameworks and features",
                    "create_react_app": "Create React + TypeScript + Vite project",
                    "create_vue_app": "Create Vue 3 + TypeScript + Vite project",
                }
            elif category == "package":
                help_info["tools"] = {
                    "detect_package_manager": "Auto-detect npm/yarn/pnpm/bun",
                    "install_packages": "Install dependencies",
                    "update_packages": "Update with conflict resolution",
                    "remove_packages": "Remove dependencies",
                    "analyze_package_json": "Security and compatibility analysis",
                }
            elif category == "build":
                help_info["tools"] = {
                    "configure_typescript": "Strict TypeScript setup",
                    "configure_biome": "Biome lint+format (replaces ESLint+Prettier)",
                    "configure_vite": "Vite dev/build config",
                    "setup_testing_config": "Vitest + Testing Library setup",
                }
            elif category == "component":
                help_info["tools"] = {
                    "generate_react_component": "React component with styles+tests",
                    "generate_vue_component": "Vue 3 Composition API component",
                    "generate_custom_hook": "React hooks (state, fetch, storage)",
                    "setup_tailwind": "Tailwind styling baseline",
                    "setup_shadcn": "shadcn/ui component library",
                    "scaffold_dashboard": "Full dashboard scaffold",
                }

            return _success_response(help_info)
        except Exception as e:
            return _error_response(str(e), "internal_error")


async def _get_sampling_help(level: str) -> str:
    """Get detailed help about sampling and agentic operations in Web Development MCP."""

    if level in ["basic", "intermediate"]:
        return """# Agentic Sampling & Orchestration

## What is Web Development Sampling?

**Web Development Sampling** (SEP-1577) allows the AI to autonomously orchestrate the entire development lifecycle. Instead of giving step-by-step commands for scaffolding, package management, and component creation, you provide a high-level goal and the AI "samples" the best path to achieve it.

## Key Tool: `agentic_workflow_tool`

This tool uses deep orchestration to handle complex tasks:

- **Goal-Oriented**: Focuses on high-level results (e.g., "Build a contact form with email validation").
- **Multi-Tool Orchestration**: Automatically combines `scaffolding_tools`, `package_tools`, and `component_tools`.
- **Autonomous Setup**: The AI selects the framework, installs dependencies, and generates code templates.

## Common Agentic Workflows

- **Application Scaffolding**: "Create a new Next.js project with TailwindCSS and install Shadcn UI."
- **Feature Implementation**: "Add a state-managed shopping cart component to the existing app."
- **Build Optimization**: "Review the package.json and optimize dependencies for production."
"""

    else:  # advanced/expert
        return """# Advanced Agentic Architecture (SEP-1577)

## Orchestration Strategy

The `agentic_workflow_tool` utilizes a **multi-stage sampling process**:

1. **Analysis Stage**: The LLM evaluates the `goal` against available templates and tools.
2. **Strategy Generation**: The LLM creates a plan involving multiple tools (e.g., `create_react_app` -> `install_packages` -> `generate_react_component`).
3. **Execution Stage**: Each tool is called with appropriate parameters, with the output of one informing the next.

## Safety & Ethics Guards

- **Consent Required**: All destructive or external operations (like `install_packages`) require explicit user confirmation.
- **Quota Management**: Limits on tokens and iteration depth to prevent runaway orchestration.
- **Workspace Isolation**: Operations are restricted to the designated project directory.
"""
