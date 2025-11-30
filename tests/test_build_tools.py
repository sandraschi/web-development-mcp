"""
Tests for the BuildTools class.

These tests verify the functionality of the build tools.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directory to the Python path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_development_mcp.tools.build_tools_new import BuildTools

class TestBuildTools(unittest.TestCase):
    """Test cases for the BuildTools class."""
    
    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.project_path = Path(self.test_dir) / "test-project"
        self.project_path.mkdir()
        
        # Create a minimal package.json
        self.package_json = self.project_path / "package.json"
        self.package_json.write_text(json.dumps({
            "name": "test-project",
            "version": "1.0.0",
            "scripts": {
                "test": "echo \"Error: no test specified\" && exit 0",
                "build": "echo \"Building...\" && exit 0",
                "dev": "echo \"Starting dev server...\" && exit 0"
            },
            "devDependencies": {
                "eslint": "^8.0.0",
                "prettier": "^3.0.0"
            }
        }))
        
        # Create a minimal .eslintrc.json
        (self.project_path / ".eslintrc.json").write_text(json.dumps({
            "extends": "eslint:recommended",
            "env": {
                "browser": True,
                "es2021": True
            },
            "parserOptions": {
                "ecmaVersion": "latest",
                "sourceType": "module"
            },
            "rules": {}
        }))
        
        # Create a minimal .prettierrc
        (self.project_path / ".prettierrc").write_text(json.dumps({
            "semi": True,
            "singleQuote": true,
            "tabWidth": 2
        }))
        
        # Create a test source file
        self.src_dir = self.project_path / "src"
        self.src_dir.mkdir()
        (self.src_dir / "index.js").write_text("console.log('Hello, world!');")
        
        # Initialize BuildTools
        self.build_tools = BuildTools(self.project_path)
    
    def tearDown(self):
        """Clean up the temporary directory."""
        shutil.rmtree(self.test_dir)
    
    def test_install_dependencies(self):
        """Test installing dependencies."""
        with patch('subprocess.run') as mock_run:
            # Configure the mock to return a successful result
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "Dependencies installed successfully"
            mock_run.return_value = mock_result
            
            # Call the method
            result = self.build_tools.install_dependencies()
            
            # Verify the result
            self.assertTrue(result["success"])
            self.assertIn("install", result["command"])
    
    def test_build_project(self):
        """Test building the project."""
        with patch('subprocess.run') as mock_run:
            # Configure the mock to return a successful result
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "Build completed successfully"
            mock_run.return_value = mock_result
            
            # Call the method
            result = self.build_tools.build_project()
            
            # Verify the result
            self.assertTrue(result["success"])
            self.assertIn("build", result["command"])
    
    def test_start_development_server(self):
        """Test starting the development server."""
        with patch('subprocess.Popen') as mock_popen:
            # Configure the mock process
            mock_process = MagicMock()
            mock_process.pid = 12345
            mock_process.stdout.readline.return_value = "Server running at http://localhost:3000"
            mock_popen.return_value = mock_process
            
            # Call the method
            result = self.build_tools.start_development_server(port=3000)
            
            # Verify the result
            self.assertTrue(result["success"])
            self.assertEqual(result["port"], 3000)
            self.assertEqual(result["url"], "http://localhost:3000")
    
    def test_run_tests(self):
        """Test running tests."""
        with patch('subprocess.run') as mock_run:
            # Configure the mock to return a successful result
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "Tests: 1 passed, 1 total"
            mock_run.return_value = mock_result
            
            # Call the method
            result = self.build_tools.run_tests()
            
            # Verify the result
            self.assertTrue(result["success"])
            self.assertEqual(result["test_results"]["passed"], 1)
            self.assertEqual(result["test_results"]["total"], 1)
    
    def test_lint_code(self):
        """Test linting code."""
        with patch('subprocess.run') as mock_run:
            # Configure the mock to return a successful result
            mock_result = MagicMock()
            mock_result.returncode = 1  # Lint issues found
            mock_result.stdout = "src/index.js:1:1: error: Unexpected console statement"
            mock_run.return_value = mock_result
            
            # Call the method
            result = self.build_tools.lint_code()
            
            # Verify the result
            self.assertFalse(result["success"])  # Lint issues found
            self.assertGreater(len(result["issues"]), 0)
            self.assertIn("error", result["issues"][0]["severity"])
    
    def test_format_code(self):
        """Test formatting code."""
        with patch('subprocess.run') as mock_run:
            # Configure the mock to return a successful result
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "src/index.js"
            mock_run.return_value = mock_result
            
            # Call the method
            result = self.build_tools.format_code()
            
            # Verify the result
            self.assertTrue(result["success"])
            self.assertIn("src/index.js", result["formatted_files"][0])

if __name__ == "__main__":
    unittest.main()
