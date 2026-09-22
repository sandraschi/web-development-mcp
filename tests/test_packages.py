"""Tests for package tools — real module-level functions, tmp dirs only."""

import json

from web_development_mcp.tools.package_tools import (
    _detect_build_tool,
    _detect_framework,
    analyze_package_json,
    detect_package_manager,
)


def test_detect_package_manager_bun(tmp_path):
    (tmp_path / "package.json").write_text("{}")
    (tmp_path / "bun.lock").write_text("")
    result = detect_package_manager(str(tmp_path))
    assert result["success"] is True
    assert result["primary_manager"] == "bun"
    assert result["package_json_exists"] is True


def test_detect_package_manager_empty(tmp_path):
    result = detect_package_manager(str(tmp_path))
    assert result["success"] is True
    assert result["primary_manager"] is None
    assert result["package_json_exists"] is False


def test_analyze_package_json_missing(tmp_path):
    result = analyze_package_json(str(tmp_path))
    assert result["success"] is False
    assert "not found" in result["error"].lower()


def test_analyze_package_json_valid(tmp_path):
    pkg_data = {
        "name": "demo",
        "version": "1.0.0",
        "dependencies": {"react": "^18.0.0"},
        "devDependencies": {"typescript": "^5.0.0", "vitest": "^1.0.0"},
    }
    (tmp_path / "package.json").write_text(json.dumps(pkg_data))

    result = analyze_package_json(str(tmp_path))
    assert result["success"] is True
    assert result["dependencies"]["production"] == 1
    assert result["dependencies"]["development"] == 2
    assert result["analysis"]["framework_detected"] == "React"
    assert result["analysis"]["has_typescript"] is True
    assert result["analysis"]["has_testing"] is True


def test_detect_framework_helpers():
    assert _detect_framework({"react": "^18.0.0"}, {}) == "React"
    assert _detect_framework({"vue": "^3.0.0"}, {}) == "Vue"
    assert _detect_framework({}, {}) is None


def test_detect_build_tool_helpers():
    assert _detect_build_tool({}, {"vite": "^5.0.0"}) == "Vite"
    assert _detect_build_tool({}, {}) is None
