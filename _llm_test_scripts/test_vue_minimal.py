"""
Minimal test script for the Vue 3 project scaffolder.

This script directly tests the VueScaffolder implementation without any dependencies.
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict

# Add the web_development_mcp directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "web_development_mcp")))

# Import the VueScaffolder class directly from the file
from tools.scaffolding.frameworks.vue_scaffolder_integrated import VueScaffolder


class TestVueScaffolderMinimal(unittest.TestCase):
    """Minimal test cases for the VueScaffolder class."""

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
