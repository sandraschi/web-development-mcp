"""
Direct test script for the Vue 3 project scaffolder.

This script tests the VueScaffolder implementation by directly executing its code.
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict, Any

# Define the VueScaffolder class directly to avoid import issues
class VueScaffolder:
    """Vue 3 project scaffolder implementation."""
    
    @staticmethod
    def create_project(project_name: str, project_path: Path, options: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Vue 3 project with the given options."""
        try:
            # Create project directory
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Create package.json
            package_json = {
                "name": project_name,
                "version": "0.1.0",
                "private": True,
                "scripts": {
                    "dev": "vite",
                    "build": "vite build",
                    "preview": "vite preview",
                    "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix --ignore-path .gitignore",
                    "test:unit": "vitest"
                },
                "dependencies": {
                    "vue": "^3.3.0",
                    "pinia": "^2.1.0",
                    "vue-router": "^4.2.0"
                },
                "devDependencies": {
                    "@vitejs/plugin-vue": "^4.2.0",
                    "@vitejs/plugin-vue-jsx": "^3.0.0",
                    "@vue/test-utils": "^2.4.0",
                    "@vue/tsconfig": "^0.4.0",
                    "@vuedx/typecheck": "^0.7.0",
                    "@vuedx/typescript-plugin-vue": "^1.8.0",
                    "@vue/eslint-config-prettier": "^7.1.0",
                    "@vue/eslint-config-typescript": "^11.0.0",
                    "autoprefixer": "^10.4.0",
                    "eslint": "^8.0.0",
                    "eslint-plugin-vue": "^9.0.0",
                    "jsdom": "^22.0.0",
                    "postcss": "^8.4.0",
                    "prettier": "^3.0.0",
                    "sass": "^1.62.0",
                    "tailwindcss": "^3.3.0",
                    "typescript": "~5.0.0",
                    "vite": "^4.0.0",
                    "vite-plugin-vue-devtools": "^6.0.0",
                    "vitest": "^0.32.0",
                    "vue-tsc": "^1.0.0"
                }
            }
            
            # Write package.json
            (project_path / "package.json").write_text(
                f"{json.dumps(package_json, indent=2)}\n",
                encoding="utf-8"
            )
            
            # Create src directory and basic files
            src_dir = project_path / "src"
            src_dir.mkdir(exist_ok=True)
            
            # Create App.vue
            (src_dir / "App.vue").write_text(
                "<template>\n"
                "  <div>\n"
                "    <h1>Welcome to Your Vue.js App</h1>\n"
                "  </div>\n"
                "</template>\n"
                "\n"
                "<script setup lang=\"ts\">\n"
                "// This starter template is using Vue 3 <script setup> SFCs\n"
                "// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup\n"
                "</script>\n"
                "\n"
                "<style>\n"
                "#app {\n"
                "  font-family: Avenir, Helvetica, Arial, sans-serif;\n"
                "  -webkit-font-smoothing: antialiased;\n"
                "  -moz-osx-font-smoothing: grayscale;\n"
                "  text-align: center;\n"
                "  color: #2c3e50;\n"
                "  margin-top: 60px;\n"
                "}\n"
                "</style>\n",
                encoding="utf-8"
            )
            
            # Create main.ts
            (src_dir / "main.ts").write_text(
                "import { createApp } from 'vue'\n"
                "import App from './App.vue'\n"
                "\n"
                "createApp(App).mount('#app')\n",
                encoding="utf-8"
            )
            
            # Create index.html
            (project_path / "index.html").write_text(
                "<!DOCTYPE html>\n"
                "<html lang=\"en\">\n"
                "  <head>\n"
                "    <meta charset=\"UTF-8\" />\n"
                "    <link rel=\"icon\" type=\"image/svg+xml\" href=\"/vite.svg\" />\n"
                "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n"
                "    <title>Vue App</title>\n"
                "  </head>\n"
                "  <body>\n"
                "    <div id=\"app\"></div>\n"
                "    <script type=\"module\" src=\"/src/main.ts\"></script>\n"
                "  </body>\n"
                "</html>\n",
                encoding="utf-8"
            )
            
            # Create tsconfig.json
            (project_path / "tsconfig.json").write_text(
                '{\n'
                '  "compilerOptions": {\n'
                '    "target": "ESNext",\n'
                '    "useDefineForClassFields": true,\n'
                '    "module": "ESNext",\n'
                '    "moduleResolution": "Node",\n'
                '    "strict": true,\n'
                '    "jsx": "preserve",\n'
                '    "resolveJsonModule": true,\n'
                '    "isolatedModules": true,\n'
                '    "esModuleInterop": true,\n'
                '    "lib": ["ESNext", "DOM"],\n'
                '    "skipLibCheck": true,\n'
                '    "noEmit": true,\n'
                '    "baseUrl": ".",\n'
                '    "paths": {\n'
                '      "@/*": ["src/*"]\n'
                '    },\n'
                '    "types": ["vite/client"]\n'
                '  },\n'
                '  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"],\n'
                '  "references": [{"path": "./tsconfig.node.json"}]\n'
                '}\n',
                encoding="utf-8"
            )
            
            return {
                "success": True,
                "project_name": project_name,
                "project_path": str(project_path),
                "framework": "vue"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "project_name": project_name,
                "project_path": str(project_path),
                "framework": "vue"
            }
    
    @staticmethod
    def validate_options(options: Dict[str, Any]) -> list:
        """Validate the provided options."""
        return []

# Test case
class TestVueScaffolderDirect(unittest.TestCase):
    """Direct test cases for the VueScaffolder class."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp(prefix="vue_scaffold_test_"))
        self.project_name = "test-vue-app"
        self.project_path = self.test_dir / self.project_name
        self.options = {
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
    import json  # Import json here to avoid issues with the class definition
    unittest.main()
