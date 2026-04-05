import pytest
import os
import shutil
from pathlib import Path
from web_development_mcp.tools.scaffolding_tools import (
    create_react_app,
    create_vue_app,
    _is_valid_project_name,
)


def test_project_name_validation():
    assert _is_valid_project_name("valid-name") is True
    assert _is_valid_project_name("Invalid Name") is False
    assert _is_valid_project_name("valid123") is True
    assert _is_valid_project_name("no_underscores") is False


def test_create_react_app_structure(tmp_path):
    project_name = "test-react-app"
    result = create_react_app(project_name, str(tmp_path))

    assert result["success"] is True
    assert result["project_name"] == project_name

    project_path = tmp_path / project_name
    assert project_path.exists()
    assert (project_path / "package.json").exists()
    assert (project_path / "src").exists()
    assert (project_path / "vite.config.ts").exists()


def test_create_vue_app_structure(tmp_path):
    project_name = "test-vue-app"
    result = create_vue_app(project_name, str(tmp_path))

    assert result["success"] is True
    assert result["project_name"] == project_name

    project_path = tmp_path / project_name
    assert project_path.exists()
    assert (project_path / "package.json").exists()
    assert (project_path / "src").exists()
    assert (project_path / "vite.config.ts").exists()


def test_duplicate_project_error(tmp_path):
    project_name = "duplicate-app"
    project_path = tmp_path / project_name
    project_path.mkdir()

    result = create_react_app(project_name, str(tmp_path))
    assert result["success"] is False
    assert "already exists" in result["error"]
