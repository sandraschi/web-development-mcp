"""Tests for dashboard tools — real registered functions, tmp dirs only."""

from web_development_mcp.tools.dashboard_tools import register_tools


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


def test_scaffold_dashboard(tmp_path):
    # NOTE: setup_tailwind / setup_shadcn run real package-manager
    # subprocesses and are intentionally NOT covered here (no network
    # side effects in unit tests).
    result = _collect()["scaffold_dashboard"](project_path=str(tmp_path), project_name="demo", with_chatbot=False)
    assert result["success"] is True
    assert result["message"]
    assert len(result["files_created"]) > 0
    assert (tmp_path / "src" / "components" / "dashboard").exists()
