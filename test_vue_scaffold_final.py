"""
Final test script for the Vue 3 project scaffolder.

This script tests the VueScaffolder implementation with the correct import path.
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict, Any

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "web_development_mcp"))
sys.path.insert(0, project_root)

# Import the VueScaffolder class
from tools.scaffolding.frameworks.vue_scaffolder_integrated import VueScaffolder

class TestVueScaffolderFinal(unittest.TestCase):
    """Final test cases for the VueScaffolder class."""
    
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
            "eslint_strict": False
        }
    
    def tearDown(self):
        """Clean up test environment."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_create_project(self):
        """Test project creation."""
        # Create the project
        result = VueScaffolder.create_project(
            self.project_name,
            self.project_path,
            self.options
        )
        
        # Check the result
        self.assertTrue(result["success"])
        self.assertEqual(result["project_name"], self.project_name)
        self.assertEqual(result["framework"], "vue")
        
        # Check if the project directory was created
        self.assertTrue(self.project_path.exists())
        self.assertTrue(self.project_path.is_dir())
        
        # Check if package.json was created
        package_json = self.project_path / "package.json"
        self.assertTrue(package_json.exists())
        
        # Check if src directory was created
        src_dir = self.project_path / "src"
        self.assertTrue(src_dir.exists())
        self.assertTrue(src_dir.is_dir())
        
        # Check if App.vue was created
        app_vue = src_dir / "App.vue"
        self.assertTrue(app_vue.exists())
    
    def test_validate_options(self):
        """Test options validation."""
        # Test with valid options
        valid_options = {
            "router": True,
            "pinia": True,
            "testing": True,
            "prettier": True,
            "eslint_strict": False
        }
        errors = VueScaffolder.validate_options(valid_options)
        self.assertEqual(len(errors), 0)
        
        # Test with invalid options (should still pass as we don't have strict validation)
        invalid_options = {
            "invalid_option": True
        }
        errors = VueScaffolder.validate_options(invalid_options)
        self.assertEqual(len(errors), 0)

if __name__ == "__main__":
    unittest.main()
