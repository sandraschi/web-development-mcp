"""Tests for component tools — real registered functions, tmp dirs only."""

from web_development_mcp.tools.component_tools import (
    _is_valid_component_name,
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


def test_component_name_validation():
    assert _is_valid_component_name("UserCard") is True
    assert _is_valid_component_name("userCard") is False
    assert _is_valid_component_name("user-card") is False


def test_generate_react_component(tmp_path):
    result = _collect()["generate_react_component"](project_path=str(tmp_path), component_name="UserCard")
    assert result["success"] is True
    assert result["message"]
    assert (tmp_path / "src" / "components" / "UserCard").exists()


def test_generate_react_component_rejects_bad_name(tmp_path):
    result = _collect()["generate_react_component"](project_path=str(tmp_path), component_name="user-card")
    assert result["success"] is False
    assert result["message"]


def test_generate_vue_component(tmp_path):
    result = _collect()["generate_vue_component"](project_path=str(tmp_path), component_name="UserCard")
    assert result["success"] is True
    assert (tmp_path / "src" / "components" / "UserCard.vue").exists()


def test_generate_vue_component_refuses_options_api(tmp_path):
    result = _collect()["generate_vue_component"](
        project_path=str(tmp_path), component_name="UserCard", composition_api=False
    )
    assert result["success"] is False
    assert "composition_api" in result["message"]


def test_generate_custom_hook(tmp_path):
    result = _collect()["generate_custom_hook"](project_path=str(tmp_path), hook_name="useUserData", hook_type="fetch")
    assert result["success"] is True
    assert (tmp_path / "src" / "hooks" / "useUserData.ts").exists()


def test_generate_custom_hook_refuses_unknown_type(tmp_path):
    result = _collect()["generate_custom_hook"](project_path=str(tmp_path), hook_name="useMagic", hook_type="teleport")
    assert result["success"] is False
    assert "teleport" in result["message"]
