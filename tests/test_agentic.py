"""Tests for agentic tools — real planner output and guard state."""

import asyncio

from web_development_mcp.tools.agentic_tools import (
    is_safety_guard_enabled,
    register_tools,
)


def _collect():
    fns = {}

    class FakeMCP:
        def tool(self, *args, **kwargs):
            def deco(fn):
                fns[fn.__name__] = fn
                return fn

            return deco

    register_tools(FakeMCP())
    return fns


def test_workflow_plans_real_tools():
    fns = _collect()
    result = asyncio.run(fns["agentic_workflow_tool"]("Scaffold a React app and install axios"))
    assert result["success"] is True
    assert result["mode"] == "plan"
    tools = [s["tool"] for s in result["steps"]]
    assert "create_react_app" in tools
    assert "install_packages" in tools


def test_workflow_fallback_plan():
    fns = _collect()
    result = asyncio.run(fns["agentic_workflow_tool"]("do something utterly unrelated xyz"))
    assert result["success"] is True
    assert len(result["steps"]) > 0


def test_safety_guard_state_roundtrip():
    fns = _collect()
    try:
        assert asyncio.run(fns["toggle_safety_guard"](False))["safety_guard_active"] is False
        assert is_safety_guard_enabled() is False
    finally:
        assert asyncio.run(fns["toggle_safety_guard"](True))["safety_guard_active"] is True
        assert is_safety_guard_enabled() is True
