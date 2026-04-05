from web_development_mcp.tools.package_tools import list_dependencies
import json


def test_list_dependencies_missing_file(tmp_path):
    # Test behavior when package.json is missing
    result = list_dependencies(str(tmp_path))
    assert result["success"] is False
    assert "not found" in result["error"].lower()


def test_list_dependencies_valid(tmp_path):
    pkg_data = {
        "dependencies": {"react": "^18.0.0"},
        "devDependencies": {"typescript": "^5.0.0"},
    }
    pkg_file = tmp_path / "package.json"
    with open(pkg_file, "w") as f:
        json.dump(pkg_data, f)

    result = list_dependencies(str(tmp_path))
    assert result["success"] is True
    assert "react" in result["dependencies"]
    assert "typescript" in result["dev_dependencies"]
