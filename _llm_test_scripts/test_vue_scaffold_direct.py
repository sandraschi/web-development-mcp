"""
Direct test script for the Vue 3 project scaffolder.

This script tests the VueScaffolder implementation by importing it directly
from the file and verifying its functionality.
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict

# Add the tools directory to the Python path
tools_dir = os.path.join(os.path.dirname(__file__), "web_development_mcp", "tools")
sys.path.insert(0, tools_dir)

# Import the VueScaffolder directly from the file
from scaffolding.frameworks.vue_scaffolder_integrated import VueScaffolder


class TestVueScaffolder(unittest.TestCase):
    """Test cases for the VueScaffolder class."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp(prefix="vue_scaffold_test_"))
        self.project_name = "test-vue-app"
        self.project_path = self.test_dir / self.project_name
        self.options: Dict[str, Any] = {
            "router": True,
            "pinia": True,
            "testing": True,
            "prettier": True,
            "eslint_strict": False,
        }

    def tearDown(self):
        """Clean up test environment."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_create_project_structure(self):
        """Test project structure creation."""
        # Create the project
        result = VueScaffolder.create_project(self.project_name, self.project_path, self.options)

        # Check the result
        self.assertTrue(result["success"])
        self.assertEqual(result["project_name"], self.project_name)
        self.assertEqual(result["framework"], "vue")

        # Check if required directories were created
        required_dirs = [
            self.project_path / "src",
            self.project_path / "src" / "assets",
            self.project_path / "src" / "components",
            self.project_path / "src" / "composables",
            self.project_path / "src" / "stores",
            self.project_path / "src" / "styles",
            self.project_path / "src" / "views",
            self.project_path / "src" / "router",
            self.project_path / "public",
            self.project_path / "tests" / "unit",
        ]

        for dir_path in required_dirs:
            self.assertTrue(dir_path.exists(), f"Directory not found: {dir_path}")
            self.assertTrue(dir_path.is_dir(), f"Not a directory: {dir_path}")

    def test_required_files_created(self):
        """Test that all required files are created."""
        # Create the project
        VueScaffolder.create_project(self.project_name, self.project_path, self.options)

        # Check if required files were created
        required_files = [
            self.project_path / "package.json",
            self.project_path / "tsconfig.json",
            self.project_path / "vite.config.ts",
            self.project_path / ".eslintrc.js",
            self.project_path / "tailwind.config.js",
            self.project_path / "postcss.config.js",
            self.project_path / "index.html",
            self.project_path / "src" / "main.ts",
            self.project_path / "src" / "App.vue",
            self.project_path / "src" / "components" / "TheNavbar.vue",
        ]

        # These files are created conditionally based on options
        conditional_files = [
            self.project_path / "src" / "router" / "index.ts",
            self.project_path / "src" / "views" / "HomeView.vue",
            self.project_path / "src" / "views" / "AboutView.vue",
            self.project_path / "src" / "stores" / "index.ts",
            self.project_path / "src" / "assets" / "main.css",
            self.project_path / "tests" / "setup.ts",
            self.project_path / "tests" / "unit" / "example.spec.ts",
        ]

        # Check required files
        for file_path in required_files:
            self.assertTrue(file_path.exists(), f"File not found: {file_path}")
            self.assertTrue(file_path.is_file(), f"Not a file: {file_path}")

        # Check conditional files
        for file_path in conditional_files:
            if file_path.exists():
                self.assertTrue(file_path.is_file(), f"Not a file: {file_path}")

    def test_package_json_content(self):
        """Test package.json content."""
        # Create the project
        VueScaffolder.create_project(self.project_name, self.project_path, self.options)

        # Load and check package.json
        package_json_path = self.project_path / "package.json"
        self.assertTrue(package_json_path.exists())

        with open(package_json_path, encoding="utf-8") as f:
            package_json = f.read()

        # Check for required scripts
        self.assertIn('"dev"', package_json)
        self.assertIn('"build"', package_json)
        self.assertIn('"preview"', package_json)
        self.assertIn('"lint"', package_json)

        # Check for required dependencies
        self.assertIn('"vue"', package_json)
        self.assertIn('"vite"', package_json)
        self.assertIn('"typescript"', package_json)

    def test_validate_options(self):
        """Test options validation."""
        # Test with valid options
        valid_options = {
            "router": True,
            "pinia": True,
            "testing": True,
            "prettier": True,
            "eslint_strict": False,
        }
        errors = VueScaffolder.validate_options(valid_options)
        self.assertEqual(len(errors), 0)

        # Test with invalid options (should still pass as we don't have strict validation)
        invalid_options = {"invalid_option": True}
        errors = VueScaffolder.validate_options(invalid_options)
        self.assertEqual(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
