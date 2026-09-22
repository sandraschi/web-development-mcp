"""Tests for scaffolding tools — real registered functions, tmp dirs only."""

from web_development_mcp.tools.scaffolding_tools import (
    _is_valid_project_name,
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


def test_project_name_validation():
    assert _is_valid_project_name("valid-name") is True
    assert _is_valid_project_name("Invalid Name") is False
    assert _is_valid_project_name("valid123") is True
    assert _is_valid_project_name("no_underscores") is False


def test_list_available_frameworks():
    result = _collect()["list_available_frameworks"]()
    assert result["success"] is True
    assert "react" in result["frameworks"]
    assert "vue" in result["frameworks"]


def test_create_react_app_structure(tmp_path):
    result = _collect()["create_react_app"]("test-react-app", str(tmp_path))

    assert result["success"] is True
    assert result["project_name"] == "test-react-app"

    project_path = tmp_path / "test-react-app"
    assert project_path.exists()
    assert (project_path / "package.json").exists()
    assert (project_path / "src").exists()
    assert (project_path / "vite.config.ts").exists()


def test_create_react_app_rejects_bad_name(tmp_path):
    result = _collect()["create_react_app"]("Invalid Name", str(tmp_path))
    assert result["success"] is False


def test_create_vue_app_structure(tmp_path):
    result = _collect()["create_vue_app"]("test-vue-app", str(tmp_path))

    assert result["success"] is True
    assert result["project_name"] == "test-vue-app"

    project_path = tmp_path / "test-vue-app"
    assert project_path.exists()
    assert (project_path / "package.json").exists()
    assert (project_path / "src").exists()
    assert (project_path / "vite.config.ts").exists()
