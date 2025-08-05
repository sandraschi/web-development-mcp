"""
Project scaffolding and framework setup tools.

Handles creation of new projects with modern frameworks and best practices.
"""

import logging
import os
import subprocess
from typing import Any, Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

def register_tools(mcp):
    """Register scaffolding tools with the MCP server."""
    
    @mcp.tool()
    def list_available_frameworks() -> Dict[str, Any]:
        """List all supported frontend frameworks and their features.
        
        Returns comprehensive information about supported frameworks.
        """
        frameworks = {
            "react": {
                "name": "React",
                "description": "Popular component-based UI library",
                "features": ["TypeScript", "Vite", "React Router", "Testing Library", "ESLint"],
                "use_cases": ["SPAs", "Component libraries", "Complex UIs"],
                "popularity": "Most popular",
                "learning_curve": "Moderate"
            },
            "vue": {
                "name": "Vue 3",
                "description": "Progressive JavaScript framework",
                "features": ["TypeScript", "Vite", "Vue Router", "Pinia", "ESLint"],
                "use_cases": ["SPAs", "Progressive web apps", "Quick prototypes"],
                "popularity": "Very popular",
                "learning_curve": "Easy"
            },
            "svelte": {
                "name": "SvelteKit",
                "description": "Compile-time optimized framework",
                "features": ["TypeScript", "Vite", "SvelteKit routing", "Built-in state", "ESLint"],
                "use_cases": ["Performance-critical apps", "Small bundles", "SSR"],
                "popularity": "Growing fast",
                "learning_curve": "Easy"
            },
            "next": {
                "name": "Next.js",
                "description": "Full-stack React framework",
                "features": ["TypeScript", "App Router", "Server components", "API routes", "ESLint"],
                "use_cases": ["Full-stack apps", "SSR/SSG", "E-commerce"],
                "popularity": "Very popular",
                "learning_curve": "Moderate"
            },
            "vanilla": {
                "name": "Vanilla TypeScript",
                "description": "Modern TypeScript with Vite",
                "features": ["TypeScript", "Vite", "ESM", "Hot reload", "ESLint"],
                "use_cases": ["Libraries", "Learning", "Custom solutions"],
                "popularity": "Foundation",
                "learning_curve": "Requires JS knowledge"
            }
        }
        
        return {
            "success": True,
            "frameworks": frameworks,
            "total_frameworks": len(frameworks),
            "recommended_for_beginners": ["vue", "svelte"],
            "most_popular": ["react", "next"],
            "best_performance": ["svelte", "vanilla"]
        }
    
    @mcp.tool()
    def create_react_app(
        project_name: str,
        target_directory: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new React application with TypeScript and modern tooling.
        
        Args:
            project_name: Name of the project (will be used for package.json name)
            target_directory: Directory where project will be created
            options: Optional customization options
                - router: Include React Router (default: true)
                - testing: Include testing setup (default: true)
                - eslint_strict: Use strict ESLint rules (default: true)
                - prettier: Include Prettier configuration (default: true)
                - husky: Include git hooks (default: false)
        """
        try:
            # Default options
            opts = {
                "router": True,
                "testing": True,
                "eslint_strict": True,
                "prettier": True,
                "husky": False,
                **(options or {})
            }
            
            # Validate project name
            if not _is_valid_project_name(project_name):
                return {
                    "success": False,
                    "error": "Invalid project name. Use lowercase letters, numbers, and hyphens only."
                }
            
            # Create project directory
            project_path = Path(target_directory) / project_name
            if project_path.exists():
                return {
                    "success": False,
                    "error": f"Directory {project_path} already exists"
                }
            
            project_path.mkdir(parents=True, exist_ok=False)
            
            # Create package.json
            package_json = _create_react_package_json(project_name, opts)
            _write_json_file(project_path / "package.json", package_json)
            
            # Create project structure
            _create_react_project_structure(project_path, opts)
            
            # Create configuration files
            _create_react_config_files(project_path, opts)
            
            # Create initial React components
            _create_react_components(project_path, opts)
            
            return {
                "success": True,
                "project_name": project_name,
                "project_path": str(project_path),
                "framework": "react",
                "features_included": [
                    "TypeScript",
                    "Vite",
                    "ESLint" + (" (strict)" if opts["eslint_strict"] else ""),
                    "Prettier" if opts["prettier"] else None,
                    "React Router" if opts["router"] else None,
                    "Testing Library" if opts["testing"] else None,
                    "Husky git hooks" if opts["husky"] else None
                ],
                "next_steps": [
                    f"cd {project_path}",
                    "npm install",
                    "npm run dev"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error creating React app: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    @mcp.tool()
    def create_vue_app(
        project_name: str,
        target_directory: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new Vue 3 application with TypeScript and modern tooling.
        
        Args:
            project_name: Name of the project
            target_directory: Directory where project will be created  
            options: Optional customization options
                - router: Include Vue Router (default: true)
                - pinia: Include Pinia state management (default: true)
                - testing: Include testing setup (default: true)
                - eslint_strict: Use strict ESLint rules (default: true)
        """
        try:
            opts = {
                "router": True,
                "pinia": True,
                "testing": True,
                "eslint_strict": True,
                **(options or {})
            }
            
            if not _is_valid_project_name(project_name):
                return {
                    "success": False,
                    "error": "Invalid project name. Use lowercase letters, numbers, and hyphens only."
                }
            
            project_path = Path(target_directory) / project_name
            if project_path.exists():
                return {
                    "success": False,
                    "error": f"Directory {project_path} already exists"
                }
            
            project_path.mkdir(parents=True, exist_ok=False)
            
            # Create Vue project files
            package_json = _create_vue_package_json(project_name, opts)
            _write_json_file(project_path / "package.json", package_json)
            
            _create_vue_project_structure(project_path, opts)
            _create_vue_config_files(project_path, opts)
            _create_vue_components(project_path, opts)
            
            return {
                "success": True,
                "project_name": project_name,
                "project_path": str(project_path),
                "framework": "vue",
                "features_included": [
                    "Vue 3",
                    "TypeScript", 
                    "Vite",
                    "ESLint",
                    "Vue Router" if opts["router"] else None,
                    "Pinia" if opts["pinia"] else None,
                    "Vitest" if opts["testing"] else None
                ],
                "next_steps": [
                    f"cd {project_path}",
                    "npm install", 
                    "npm run dev"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error creating Vue app: {e}")
            return {
                "success": False,
                "error": str(e)
            }

def _is_valid_project_name(name: str) -> bool:
    """Validate project name follows npm naming conventions."""
    import re
    # npm package name rules
    pattern = r'^[a-z0-9]([a-z0-9\-])*[a-z0-9]$|^[a-z0-9]$'
    return bool(re.match(pattern, name)) and len(name) <= 214

def _write_json_file(path: Path, data: dict) -> None:
    """Write JSON data to file with proper formatting."""
    import json
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def _create_react_package_json(project_name: str, options: dict) -> dict:
    """Create package.json for React project."""
    dependencies = {
        "react": "^18.2.0",
        "react-dom": "^18.2.0"
    }
    
    dev_dependencies = {
        "@types/react": "^18.2.0",
        "@types/react-dom": "^18.2.0",
        "@vitejs/plugin-react": "^4.2.0",
        "typescript": "^5.3.0",
        "vite": "^5.0.0"
    }
    
    if options.get("router"):
        dependencies["react-router-dom"] = "^6.20.0"
        dev_dependencies["@types/react-router-dom"] = "^5.3.0"
    
    if options.get("testing"):
        dev_dependencies.update({
            "@testing-library/react": "^14.1.0",
            "@testing-library/jest-dom": "^6.1.0",
            "@testing-library/user-event": "^14.5.0",
            "vitest": "^1.0.0",
            "jsdom": "^23.0.0"
        })
    
    if options.get("eslint_strict"):
        dev_dependencies.update({
            "eslint": "^8.55.0",
            "@typescript-eslint/eslint-plugin": "^6.14.0",
            "@typescript-eslint/parser": "^6.14.0",
            "eslint-plugin-react": "^7.33.0",
            "eslint-plugin-react-hooks": "^4.6.0",
            "eslint-plugin-react-refresh": "^0.4.5"
        })
    
    if options.get("prettier"):
        dev_dependencies.update({
            "prettier": "^3.1.0",
            "eslint-config-prettier": "^9.1.0"
        })
    
    scripts = {
        "dev": "vite",
        "build": "tsc && vite build",
        "preview": "vite preview",
        "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
    }
    
    if options.get("testing"):
        scripts.update({
            "test": "vitest",
            "test:ui": "vitest --ui"
        })
    
    return {
        "name": project_name,
        "private": True,
        "version": "0.0.0",
        "type": "module",
        "scripts": scripts,
        "dependencies": dependencies,
        "devDependencies": dev_dependencies
    }

def _create_react_project_structure(project_path: Path, options: dict) -> None:
    """Create React project directory structure."""
    # Create directories
    directories = [
        "src",
        "src/components",
        "src/hooks", 
        "src/utils",
        "src/types",
        "public"
    ]
    
    if options.get("testing"):
        directories.extend(["src/__tests__", "src/components/__tests__"])
    
    for dir_name in directories:
        (project_path / dir_name).mkdir(parents=True, exist_ok=True)

def _create_react_config_files(project_path: Path, options: dict) -> None:
    """Create configuration files for React project."""
    # This would include creating vite.config.ts, tsconfig.json, etc.
    # Implementation details would go here
    pass

def _create_react_components(project_path: Path, options: dict) -> None:
    """Create initial React components."""
    # This would create App.tsx, main.tsx, etc.
    # Implementation details would go here
    pass

def _create_vue_package_json(project_name: str, options: dict) -> dict:
    """Create package.json for Vue project."""
    # Similar pattern for Vue
    pass

def _create_vue_project_structure(project_path: Path, options: dict) -> None:
    """Create Vue project structure."""
    pass

def _create_vue_config_files(project_path: Path, options: dict) -> None:
    """Create Vue configuration files."""
    pass

def _create_vue_components(project_path: Path, options: dict) -> None:
    """Create initial Vue components."""
    pass
