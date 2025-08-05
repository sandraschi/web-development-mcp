"""
Package management tools for npm, yarn, and pnpm.

Handles dependency installation, updates, auditing, and optimization.
"""

import logging
import subprocess
import json
import os
from typing import Any, Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

def register_tools(mcp):
    """Register package management tools with the MCP server."""
    
    @mcp.tool()
    def detect_package_manager(project_path: str) -> Dict[str, Any]:
        """Detect which package manager is being used in a project.
        
        Args:
            project_path: Path to the project directory
        """
        try:
            path = Path(project_path)
            
            # Check for lock files
            package_managers = []
            
            if (path / "package-lock.json").exists():
                package_managers.append("npm")
            if (path / "yarn.lock").exists():
                package_managers.append("yarn") 
            if (path / "pnpm-lock.yaml").exists():
                package_managers.append("pnpm")
            
            # Check for package.json
            package_json_exists = (path / "package.json").exists()
            
            # Determine primary package manager
            primary = None
            if len(package_managers) == 1:
                primary = package_managers[0]
            elif "pnpm" in package_managers:
                primary = "pnpm"  # pnpm takes precedence
            elif "yarn" in package_managers:
                primary = "yarn"  # yarn over npm
            elif "npm" in package_managers:
                primary = "npm"
            
            return {
                "success": True,
                "project_path": project_path,
                "package_json_exists": package_json_exists,
                "detected_managers": package_managers,
                "primary_manager": primary,
                "lock_files": {
                    "npm": (path / "package-lock.json").exists(),
                    "yarn": (path / "yarn.lock").exists(),
                    "pnpm": (path / "pnpm-lock.yaml").exists()
                }
            }
            
        except Exception as e:
            logger.error(f"Error detecting package manager: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    @mcp.tool()
    def install_packages(
        project_path: str,
        packages: List[str],
        package_manager: Optional[str] = None,
        dev_dependencies: bool = False
    ) -> Dict[str, Any]:
        """Install npm packages in a project.
        
        Args:
            project_path: Path to the project directory
            packages: List of package names to install
            package_manager: Specific package manager to use (auto-detect if None)
            dev_dependencies: Install as dev dependencies
        """
        try:
            # Auto-detect package manager if not specified
            if not package_manager:
                detection = detect_package_manager(project_path)
                if not detection["success"]:
                    return detection
                package_manager = detection["primary_manager"] or "npm"
            
            # Build command
            if package_manager == "npm":
                cmd = ["npm", "install"]
                if dev_dependencies:
                    cmd.append("--save-dev")
                cmd.extend(packages)
            elif package_manager == "yarn":
                cmd = ["yarn", "add"]
                if dev_dependencies:
                    cmd.append("--dev")
                cmd.extend(packages)
            elif package_manager == "pnpm":
                cmd = ["pnpm", "add"]
                if dev_dependencies:
                    cmd.append("--save-dev")
                cmd.extend(packages)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported package manager: {package_manager}"
                }
            
            # Execute command
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                "success": result.returncode == 0,
                "package_manager": package_manager,
                "packages_installed": packages if result.returncode == 0 else [],
                "dev_dependencies": dev_dependencies,
                "command": " ".join(cmd),
                "output": result.stdout if result.returncode == 0 else result.stderr,
                "error": result.stderr if result.returncode != 0 else None
            }
            
        except Exception as e:
            logger.error(f"Error installing packages: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    @mcp.tool()
    def analyze_package_json(project_path: str) -> Dict[str, Any]:
        """Analyze package.json for insights and potential issues.
        
        Args:
            project_path: Path to the project directory
        """
        try:
            path = Path(project_path)
            package_json_path = path / "package.json"
            
            if not package_json_path.exists():
                return {
                    "success": False,
                    "error": "package.json not found"
                }
            
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            # Analyze dependencies
            deps = package_data.get("dependencies", {})
            dev_deps = package_data.get("devDependencies", {})
            peer_deps = package_data.get("peerDependencies", {})
            
            # Check for common issues
            issues = []
            warnings = []
            
            # Check for outdated React patterns
            if "react" in deps:
                react_version = deps["react"]
                if "^16" in react_version or "^17" in react_version:
                    warnings.append(f"React version {react_version} is outdated, consider upgrading to ^18")
            
            # Check for TypeScript setup
            has_typescript = "typescript" in dev_deps
            has_ts_config = (path / "tsconfig.json").exists()
            
            if has_typescript and not has_ts_config:
                issues.append("TypeScript is installed but tsconfig.json is missing")
            
            # Check for testing setup
            testing_libs = ["jest", "vitest", "@testing-library/react", "@testing-library/vue"]
            has_testing = any(lib in dev_deps for lib in testing_libs)
            
            # Security check for known vulnerable packages
            potentially_vulnerable = []
            known_issues = ["node-sass", "request", "bower"]  # Example list
            
            for pkg in list(deps.keys()) + list(dev_deps.keys()):
                if pkg in known_issues:
                    potentially_vulnerable.append(pkg)
            
            return {
                "success": True,
                "project_path": project_path,
                "package_info": {
                    "name": package_data.get("name"),
                    "version": package_data.get("version"),
                    "description": package_data.get("description"),
                    "scripts": list(package_data.get("scripts", {}).keys())
                },
                "dependencies": {
                    "production": len(deps),
                    "development": len(dev_deps),
                    "peer": len(peer_deps),
                    "total": len(deps) + len(dev_deps) + len(peer_deps)
                },
                "analysis": {
                    "has_typescript": has_typescript,
                    "has_tsconfig": has_ts_config,
                    "has_testing": has_testing,
                    "framework_detected": _detect_framework(deps, dev_deps),
                    "build_tool": _detect_build_tool(deps, dev_deps)
                },
                "issues": issues,
                "warnings": warnings,
                "potentially_vulnerable": potentially_vulnerable
            }
            
        except Exception as e:
            logger.error(f"Error analyzing package.json: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    @mcp.tool()
    def update_packages(
        project_path: str,
        packages: Optional[List[str]] = None,
        package_manager: Optional[str] = None,
        check_only: bool = False
    ) -> Dict[str, Any]:
        """Update npm packages to latest versions.
        
        Args:
            project_path: Path to the project directory
            packages: Specific packages to update (update all if None)
            package_manager: Package manager to use (auto-detect if None)
            check_only: Only check for updates without installing
        """
        try:
            # Auto-detect package manager
            if not package_manager:
                detection = detect_package_manager(project_path)
                if not detection["success"]:
                    return detection
                package_manager = detection["primary_manager"] or "npm"
            
            # Build command
            if check_only:
                if package_manager == "npm":
                    cmd = ["npm", "outdated"]
                elif package_manager == "yarn":
                    cmd = ["yarn", "outdated"]
                elif package_manager == "pnpm":
                    cmd = ["pnpm", "outdated"]
            else:
                if package_manager == "npm":
                    cmd = ["npm", "update"]
                    if packages:
                        cmd.extend(packages)
                elif package_manager == "yarn":
                    cmd = ["yarn", "upgrade"]
                    if packages:
                        cmd.extend(packages)
                elif package_manager == "pnpm":
                    cmd = ["pnpm", "update"]
                    if packages:
                        cmd.extend(packages)
            
            # Execute command
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return {
                "success": True,
                "package_manager": package_manager,
                "check_only": check_only,
                "packages": packages or "all",
                "command": " ".join(cmd),
                "output": result.stdout,
                "outdated_info": result.stdout if check_only else None
            }
            
        except Exception as e:
            logger.error(f"Error updating packages: {e}")
            return {
                "success": False,
                "error": str(e)
            }

def _detect_framework(deps: dict, dev_deps: dict) -> Optional[str]:
    """Detect frontend framework from dependencies."""
    if "react" in deps:
        return "react"
    elif "vue" in deps:
        return "vue"
    elif "svelte" in deps or "@sveltejs/kit" in deps:
        return "svelte"
    elif "next" in deps:
        return "next"
    elif "@angular/core" in deps:
        return "angular"
    return None

def _detect_build_tool(deps: dict, dev_deps: dict) -> Optional[str]:
    """Detect build tool from dependencies."""
    if "vite" in dev_deps:
        return "vite"
    elif "webpack" in dev_deps:
        return "webpack"
    elif "rollup" in dev_deps:
        return "rollup"
    elif "parcel" in dev_deps:
        return "parcel"
    return None
