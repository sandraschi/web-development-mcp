"""
Agentic orchestration tools for web development operations (SEP-1577).

The workflow tool is a deterministic planner: it maps a high-level goal onto
the server's real registered tools and returns an ordered, reviewable plan.
It does not execute anything by itself — each planned step is a concrete tool
call the agent (or user) runs individually. Destructive steps stay gated
behind the session safety guard.
"""

from fastmcp import FastMCP

_safety_guard_enabled = True


def is_safety_guard_enabled() -> bool:
    """Current state of the session safety guard (module-level, real state)."""
    return _safety_guard_enabled


# keyword -> ordered plan steps (real tool names + argument hints)
_PLAN_RULES: list[tuple[tuple[str, ...], list[dict]]] = [
    (
        ("react", "scaffold", "new app", "new project", "vue", "create"),
        [
            {"tool": "list_available_frameworks", "args": {}, "why": "Confirm the framework surface first"},
            {
                "tool": "create_react_app",
                "args": {"project_name": "<name>", "target_directory": "<dir>"},
                "why": "Scaffold React+TS+Vite (or create_vue_app for Vue)",
            },
        ],
    ),
    (
        ("package", "install", "dependenc", "update", "audit"),
        [
            {"tool": "detect_package_manager", "args": {"project_path": "<dir>"}, "why": "Lockfile detection first"},
            {
                "tool": "analyze_package_json",
                "args": {"project_path": "<dir>"},
                "why": "Security/compat pass before changing anything",
            },
            {
                "tool": "install_packages",
                "args": {"project_path": "<dir>", "packages": ["<pkg>"]},
                "why": "Install (destructive — needs guard review)",
            },
        ],
    ),
    (
        ("typescript", "vite", "biome", "eslint", "testing", "vitest", "config"),
        [
            {
                "tool": "configure_typescript",
                "args": {"project_path": "<dir>", "strict_mode": True},
                "why": "Strict TS baseline",
            },
            {
                "tool": "configure_vite",
                "args": {"project_path": "<dir>", "framework": "react"},
                "why": "Dev/build config",
            },
            {
                "tool": "configure_biome",
                "args": {"project_path": "<dir>"},
                "why": "Lint+format (replaces ESLint+Prettier)",
            },
            {"tool": "setup_testing_config", "args": {"project_path": "<dir>"}, "why": "Vitest + Testing Library"},
        ],
    ),
    (
        ("component", "hook", "ui", "shadcn", "tailwind", "dashboard"),
        [
            {
                "tool": "generate_react_component",
                "args": {"project_path": "<dir>", "component_name": "<Name>"},
                "why": "Component with styles+tests",
            },
            {"tool": "setup_tailwind", "args": {"project_path": "<dir>"}, "why": "Styling baseline"},
            {"tool": "setup_shadcn", "args": {"project_path": "<dir>"}, "why": "Component library (optional)"},
        ],
    ),
]

_FALLBACK_PLAN = [
    {"tool": "get_help", "args": {}, "why": "No keyword match — start from the tool catalogue"},
    {"tool": "list_available_frameworks", "args": {}, "why": "See what this server can scaffold"},
]


def _plan_goal(goal: str) -> list[dict]:
    text = goal.lower()
    steps: list[dict] = []
    for keywords, rule_steps in _PLAN_RULES:
        if any(k in text for k in keywords):
            steps.extend(rule_steps)
    return steps or list(_FALLBACK_PLAN)


def register_tools(mcp: FastMCP):
    """Register agentic tools with the FastMCP instance."""

    @mcp.tool()
    async def agentic_workflow_tool(goal: str) -> dict:
        """Plan a multi-step web development workflow for a high-level goal.

        Returns an ordered plan of real tool calls. Nothing is executed here;
        run each planned step as its own tool call and confirm destructive
        steps while the safety guard is on.

        ## Return Format

        `{success, message, mode, safety_guard, steps, note}` — `steps` is a
        list of `{tool, args, why}` with real registered tool names.

        ## Examples

        - goal="Scaffold a React app and install axios" -> plan with
          `create_react_app`, `detect_package_manager`, `install_packages`.
        - goal="Configure TypeScript and Biome" -> plan with
          `configure_typescript`, `configure_biome`.
        """
        steps = _plan_goal(goal)
        return {
            "success": True,
            "message": f"Planned {len(steps)} steps for: {goal}",
            "mode": "plan",
            "safety_guard": _safety_guard_enabled,
            "steps": steps,
            "note": "Planner only — execute each step individually; destructive steps need explicit confirmation.",
        }

    @mcp.tool()
    async def toggle_safety_guard(enabled: bool) -> dict:
        """Enable or disable the session safety guard.

        When enabled, destructive operations require explicit confirmation.
        State is kept module-level for the server session.

        ## Return Format

        `{success, message, safety_guard_active}`.

        ## Examples

        - enabled=True -> guard on, destructive steps ask first.
        - enabled=False -> guard off for a trusted batch run.
        """
        global _safety_guard_enabled
        _safety_guard_enabled = bool(enabled)
        return {
            "success": True,
            "safety_guard_active": _safety_guard_enabled,
            "message": f"Safety Guard {'enabled' if _safety_guard_enabled else 'disabled'}",
        }
