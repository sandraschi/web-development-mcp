"""Tests for build-config tools — real registered functions, tmp dirs only."""

import json

from web_development_mcp.tools.build_tools import register_tools


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


def test_configure_typescript_strict_react(tmp_path):
    result = _collect()["configure_typescript"](project_path=str(tmp_path), strict_mode=True, include_react=True)
    assert result["success"] is True
    tsconfig = json.loads((tmp_path / "tsconfig.json").read_text(encoding="utf-8"))
    assert tsconfig["compilerOptions"]["strict"] is True
    assert tsconfig["compilerOptions"]["jsx"] == "react-jsx"


def test_configure_biome(tmp_path):
    result = _collect()["configure_biome"](project_path=str(tmp_path))
    assert result["success"] is True
    assert "biome.json" in result["config_files"]
    assert (tmp_path / "biome.json").exists()


def test_configure_vite_react_port(tmp_path):
    result = _collect()["configure_vite"](project_path=str(tmp_path), framework="react", port=11099)
    assert result["success"] is True
    content = (tmp_path / "vite.config.ts").read_text(encoding="utf-8")
    assert "11099" in content
    assert "react()" in content


def test_setup_testing_config_vitest(tmp_path):
    result = _collect()["setup_testing_config"](project_path=str(tmp_path), framework="react", test_runner="vitest")
    assert result["success"] is True
    assert (tmp_path / "vitest.config.ts").exists()
    assert (tmp_path / "src" / "test" / "setup.ts").exists()
