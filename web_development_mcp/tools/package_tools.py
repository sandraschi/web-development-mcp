"""
Package management tools for npm, yarn, and pnpm.

Handles dependency installation, updates, auditing, and optimization.
"""

import logging
import subprocess
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

# ====================
# Core Tool Functions
# ====================

def detect_package_manager(project_path: str) -> Dict[str, Any]:
    """Detect which package manager is being used in a project.
    
    Args:
        project_path: Path to the project directory
        
    Returns:
        Dictionary containing package manager information
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
            "package_managers": package_managers,
            "primary": primary,
            "package_json_exists": package_json_exists,
            "package_json_path": str(path / "package.json") if package_json_exists else None
        }
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

def _run_package_command(project_path: str, command: list, timeout: int = 300) -> Dict[str, Any]:
    """Run a package manager command and return the result.
    
    Args:
        project_path: Path to the project directory
        command: List of command parts to execute
        timeout: Maximum time to wait for command completion in seconds
        
    Returns:
        Dictionary with command results
    """
    try:
        result = subprocess.run(
            command,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Command timed out after {timeout} seconds",
            "command": " ".join(command)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "command": " ".join(command)
        }

def _get_package_manager_command(package_manager: str, subcommand: str, *args) -> list:
    """Get the appropriate package manager command.
    
    Args:
        package_manager: One of 'npm', 'yarn', or 'pnpm'
        subcommand: The subcommand to run (e.g., 'install', 'audit')
        *args: Additional arguments to pass to the command
        
    Returns:
        List of command parts to execute
    """
    if package_manager == "yarn":
        cmd = ["yarn", subcommand]
    elif package_manager == "pnpm":
        cmd = ["pnpm", subcommand]
    else:  # Default to npm
        cmd = ["npm", subcommand]
    
    cmd.extend(args)
    return cmd

def audit_dependencies(project_path: str, package_manager: Optional[str] = None) -> Dict[str, Any]:
    """Audit project dependencies for known vulnerabilities.
    
    Args:
        project_path: Path to the project directory
        package_manager: Package manager to use (auto-detect if None)
        
    Returns:
        Dictionary with audit results
    """
    try:
        # Auto-detect package manager
        if not package_manager:
            detection = detect_package_manager(project_path)
            if not detection["success"]:
                return detection
            package_manager = detection["primary_manager"] or "npm"
        
        # Build and run audit command
        cmd = _get_package_manager_command(package_manager, "audit")
        result = _run_package_command(project_path, cmd)
        
        if not result["success"]:
            return {
                "success": False,
                "error": result.get("stderr", "Unknown error during audit"),
                "package_manager": package_manager
            }
        
        # Parse audit results
        return {
            "success": True,
            "package_manager": package_manager,
            "vulnerabilities_found": "found \d+ vulnerabilities" in result["stdout"],
            "output": result["stdout"],
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "package_manager": package_manager or "unknown"
        }

def clean_install(project_path: str, package_manager: Optional[str] = None) -> Dict[str, Any]:
    """Perform a clean installation of all dependencies.
    
    Args:
        project_path: Path to the project directory
        package_manager: Package manager to use (auto-detect if None)
        
    Returns:
        Dictionary with installation results
    """
    try:
        # Auto-detect package manager
        if not package_manager:
            detection = detect_package_manager(project_path)
            if not detection["success"]:
                return detection
            package_manager = detection["primary_manager"] or "npm"
        
        # Clean node_modules and lock files
        import shutil
        node_modules = Path(project_path) / "node_modules"
        if node_modules.exists():
            shutil.rmtree(node_modules)
        
        # Remove lock files
        lock_files = ["package-lock.json", "yarn.lock", "pnpm-lock.yaml"]
        for lock_file in lock_files:
            lock_path = Path(project_path) / lock_file
            if lock_path.exists():
                lock_path.unlink()
        
        # Install dependencies
        cmd = _get_package_manager_command(package_manager, "install")
        result = _run_package_command(project_path, cmd, timeout=600)  # 10 min timeout
        
        if not result["success"]:
            return {
                "success": False,
                "error": result.get("stderr", "Unknown error during installation"),
                "package_manager": package_manager
            }
        
        return {
            "success": True,
            "package_manager": package_manager,
            "output": result["stdout"],
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "package_manager": package_manager or "unknown"
        }

def list_dependencies(project_path: str, package_manager: Optional[str] = None) -> Dict[str, Any]:
    """List all installed dependencies.
    
    Args:
        project_path: Path to the project directory
        package_manager: Package manager to use (auto-detect if None)
        
    Returns:
        Dictionary with dependency information
    """
    try:
        # Auto-detect package manager
        if not package_manager:
            detection = detect_package_manager(project_path)
            if not detection["success"]:
                return detection
            package_manager = detection["primary_manager"] or "npm"
        
        # Build and run list command
        if package_manager == "yarn":
            cmd = ["yarn", "list", "--json"]
        elif package_manager == "pnpm":
            cmd = ["pnpm", "list", "--json"]
        else:  # npm
            cmd = ["npm", "list", "--json", "--depth=0"]
        
        result = _run_package_command(project_path, cmd)
        
        if not result["success"]:
            return {
                "success": False,
                "error": result.get("stderr", "Unknown error listing dependencies"),
                "package_manager": package_manager
            }
        
        # Parse and format the output
        try:
            if package_manager == "yarn":
                # Yarn outputs newline-delimited JSON
                lines = [line for line in result["stdout"].split('\n') if line.strip()]
                data = [json.loads(line) for line in lines if line.strip()]
                deps = {}
                for item in data:
                    if item.get('type') == 'tree':
                        deps.update({
                            dep['name'].split('@')[0]: dep['name'].split('@')[-1]
                            for dep in item.get('data', {}).get('trees', [])
                        })
            else:
                # npm and pnpm output a single JSON object
                data = json.loads(result["stdout"])
                deps = data.get('dependencies', {})
                if deps:
                    deps = {name: dep.get('version', 'unknown') for name, dep in deps.items()}
            
            return {
                "success": True,
                "package_manager": package_manager,
                "dependencies": deps,
                "command": " ".join(cmd)
            }
        except (json.JSONDecodeError, AttributeError) as e:
            return {
                "success": False,
                "error": f"Failed to parse dependency list: {str(e)}",
                "package_manager": package_manager,
                "raw_output": result["stdout"]
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "package_manager": package_manager or "unknown"
        }

def run_script(project_path: str, script_name: str, args: Optional[List[str]] = None,
              package_manager: Optional[str] = None) -> Dict[str, Any]:
    """Run an npm/yarn/pnpm script.
    
    Args:
        project_path: Path to the project directory
        script_name: Name of the script to run (from package.json)
        args: Additional arguments to pass to the script
        package_manager: Package manager to use (auto-detect if None)
        
    Returns:
        Dictionary with script execution results
    """
    try:
        # Auto-detect package manager
        if not package_manager:
            detection = detect_package_manager(project_path)
            if not detection["success"]:
                return detection
            package_manager = detection["primary_manager"] or "npm"
        
        # Build and run script command
        if package_manager == "yarn":
            cmd = ["yarn", "run", script_name]
        elif package_manager == "pnpm":
            cmd = ["pnpm", "run", script_name]
        else:  # npm
            cmd = ["npm", "run", script_name]
        
        if args:
            cmd.extend(args)
        
        result = _run_package_command(project_path, cmd, timeout=1800)  # 30 min timeout for scripts
        
        return {
            "success": result["returncode"] == 0,
            "package_manager": package_manager,
            "script": script_name,
            "args": args or [],
            "exit_code": result["returncode"],
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "package_manager": package_manager or "unknown",
            "script": script_name
        }

def dedupe_dependencies(project_path: str, package_manager: Optional[str] = None) -> Dict[str, Any]:
    """Deduplicate dependencies in the project.
    
    Args:
        project_path: Path to the project directory
        package_manager: Package manager to use (auto-detect if None)
        
    Returns:
        Dictionary with deduplication results
    """
    try:
        # Auto-detect package manager
        if not package_manager:
            detection = detect_package_manager(project_path)
            if not detection["success"]:
                return detection
            package_manager = detection["primary_manager"] or "npm"
        
        # Build and run dedupe command
        if package_manager == "yarn":
            # Yarn dedupe is available in Yarn 2+
            cmd = ["yarn", "dedupe"]
        elif package_manager == "pnpm":
            # pnpm dedupe is available in pnpm 6+
            cmd = ["pnpm", "dedupe"]
        else:  # npm
            cmd = ["npm", "dedupe"]
        
        result = _run_package_command(project_path, cmd, timeout=600)  # 10 min timeout
        
        return {
            "success": result["returncode"] == 0,
            "package_manager": package_manager,
            "output": result["stdout"],
            "error": result["stderr"] if result["returncode"] != 0 else None,
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "package_manager": package_manager or "unknown"
        }

def check_for_updates(project_path: str, package_manager: Optional[str] = None) -> Dict[str, Any]:
    """Check for outdated packages.
    
    Args:
        project_path: Path to the project directory
        package_manager: Package manager to use (auto-detect if None)
        
    Returns:
        Dictionary with update information
    """
    try:
        # Auto-detect package manager
        if not package_manager:
            detection = detect_package_manager(project_path)
            if not detection["success"]:
                return detection
            package_manager = detection["primary_manager"] or "npm"
        
        # Build and run outdated command
        if package_manager == "yarn":
            cmd = ["yarn", "outdated", "--json"]
        elif package_manager == "pnpm":
            cmd = ["pnpm", "outdated", "--json"]
        else:  # npm
            cmd = ["npm", "outdated", "--json"]
        
        result = _run_package_command(project_path, cmd)
        
        if not result["success"] and "No matching versions" not in result.get("stderr", ""):
            return {
                "success": False,
                "error": result.get("stderr", "Unknown error checking for updates"),
                "package_manager": package_manager
            }
        
        # Parse the output
        try:
            if package_manager == "yarn":
                # Yarn outputs newline-delimited JSON
                lines = [line for line in result["stdout"].split('\n') if line.strip()]
                data = [json.loads(line) for line in lines if line.strip()]
                updates = {}
                for item in data:
                    if item.get('type') == 'table':
                        # Yarn 2+ format
                        for row in item.get('data', {}).get('body', []):
                            if len(row) >= 5:
                                name = row[0]
                                current = row[1]
                                wanted = row[2]
                                latest = row[3]
                                updates[name] = {
                                    'current': current,
                                    'wanted': wanted,
                                    'latest': latest,
                                    'needs_update': current != latest
                                }
            else:
                # npm and pnpm output a single JSON object
                data = json.loads(result["stdout"])
                updates = {}
                for name, info in data.items():
                    if isinstance(info, dict):
                        updates[name] = {
                            'current': info.get('current', 'unknown'),
                            'wanted': info.get('wanted', 'unknown'),
                            'latest': info.get('latest', 'unknown'),
                            'needs_update': info.get('current') != info.get('latest')
                        }
            
            needs_update = any(pkg.get('needs_update', False) for pkg in updates.values())
            
            return {
                "success": True,
                "package_manager": package_manager,
                "updates_available": needs_update,
                "packages": updates,
                "command": " ".join(cmd)
            }
        except (json.JSONDecodeError, AttributeError) as e:
            return {
                "success": False,
                "error": f"Failed to parse update information: {str(e)}",
                "package_manager": package_manager,
                "raw_output": result["stdout"]
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "package_manager": package_manager or "unknown"
        }

def add_dependency(project_path: str, package_name: str, version: Optional[str] = None,
                 dev: bool = False, package_manager: Optional[str] = None) -> Dict[str, Any]:
    """Add a dependency to the project.
    
    Args:
        project_path: Path to the project directory
        package_name: Name of the package to add
        version: Specific version to install (latest if None)
        dev: Whether to add as a dev dependency
        package_manager: Package manager to use (auto-detect if None)
        
    Returns:
        Dictionary with installation results
    """
    try:
        # Auto-detect package manager
        if not package_manager:
            detection = detect_package_manager(project_path)
            if not detection["success"]:
                return detection
            package_manager = detection["primary_manager"] or "npm"
        
        # Build package spec
        pkg_spec = package_name
        if version:
            if version.startswith(('^', '~', '>', '<', '=', '||')):
                pkg_spec = f"{package_name}{version}"
            else:
                pkg_spec = f"{package_name}@{version}"
        
        # Build and run add command
        if package_manager == "yarn":
            cmd = ["yarn", "add", pkg_spec]
            if dev:
                cmd.append("--dev")
        elif package_manager == "pnpm":
            cmd = ["pnpm", "add", pkg_spec]
            if dev:
                cmd.append("--save-dev")
        else:  # npm
            cmd = ["npm", "install", "--save"]
            if dev:
                cmd.append("--save-dev")
            cmd.append(pkg_spec)
        
        result = _run_package_command(project_path, cmd, timeout=600)  # 10 min timeout
        
        return {
            "success": result["returncode"] == 0,
            "package_manager": package_manager,
            "package": package_name,
            "version": version or "latest",
            "dev_dependency": dev,
            "output": result["stdout"],
            "error": result["stderr"] if result["returncode"] != 0 else None,
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "package_manager": package_manager or "unknown",
            "package": package_name
        }

def remove_dependency(project_path: str, package_name: str,
                   package_manager: Optional[str] = None) -> Dict[str, Any]:
    """Remove a dependency from the project.
    
    Args:
        project_path: Path to the project directory
        package_name: Name of the package to remove
        package_manager: Package manager to use (auto-detect if None)
        
    Returns:
        Dictionary with removal results
    """
    try:
        # Auto-detect package manager
        if not package_manager:
            detection = detect_package_manager(project_path)
            if not detection["success"]:
                return detection
            package_manager = detection["primary_manager"] or "npm"
        
        # Build and run remove command
        if package_manager == "yarn":
            cmd = ["yarn", "remove", package_name]
        elif package_manager == "pnpm":
            cmd = ["pnpm", "remove", package_name]
        else:  # npm
            cmd = ["npm", "uninstall", "--save", package_name]
        
        result = _run_package_command(project_path, cmd, timeout=300)  # 5 min timeout
        
        return {
            "success": result["returncode"] == 0,
            "package_manager": package_manager,
            "package": package_name,
            "output": result["stdout"],
            "error": result["stderr"] if result["returncode"] != 0 else None,
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "package_manager": package_manager or "unknown",
            "package": package_name
        }

# Register the additional tools with the MCP server
def register_additional_tools(mcp):
    """Register additional package management tools with the MCP server."""
    
    @mcp.tool()
    def audit_dependencies_tool(project_path: str, package_manager: Optional[str] = None) -> Dict[str, Any]:
        """Audit project dependencies for known vulnerabilities."""
        return audit_dependencies(project_path, package_manager)
    
    @mcp.tool()
    def clean_install_tool(project_path: str, package_manager: Optional[str] = None) -> Dict[str, Any]:
        """Perform a clean installation of all dependencies."""
        return clean_install(project_path, package_manager)
    
    @mcp.tool()
    def list_dependencies_tool(project_path: str, package_manager: Optional[str] = None) -> Dict[str, Any]:
        """List all installed dependencies."""
        return list_dependencies(project_path, package_manager)
    
    @mcp.tool()
    def run_script_tool(project_path: str, script_name: str, 
                       args: Optional[List[str]] = None,
                       package_manager: Optional[str] = None) -> Dict[str, Any]:
        """Run an npm/yarn/pnpm script."""
        return run_script(project_path, script_name, args, package_manager)
    
    @mcp.tool()
    def dedupe_dependencies_tool(project_path: str, package_manager: Optional[str] = None) -> Dict[str, Any]:
        """Deduplicate dependencies in the project."""
        return dedupe_dependencies(project_path, package_manager)
    
    @mcp.tool()
    def check_for_updates_tool(project_path: str, package_manager: Optional[str] = None) -> Dict[str, Any]:
        """Check for outdated packages."""
        return check_for_updates(project_path, package_manager)
    
    @mcp.tool()
    def add_dependency_tool(project_path: str, package_name: str, 
                          version: Optional[str] = None,
                          dev: bool = False,
                          package_manager: Optional[str] = None) -> Dict[str, Any]:
        """Add a dependency to the project."""
        return add_dependency(project_path, package_name, version, dev, package_manager)
    
    @mcp.tool()
    def remove_dependency_tool(project_path: str, package_name: str,
                             package_manager: Optional[str] = None) -> Dict[str, Any]:
        """Remove a dependency from the project."""
        return remove_dependency(project_path, package_name, package_manager)

# ====================
# Tool Registration
# ====================

def register_tools(mcp):
    """Register all package management tools with the MCP server."""
    # Register core tools
    mcp.tool()(detect_package_manager)
    mcp.tool()(audit_dependencies)
    mcp.tool()(clean_install)
    mcp.tool()(list_dependencies)
    mcp.tool()(run_script)
    mcp.tool()(dedupe_dependencies)
    mcp.tool()(check_for_updates)
    mcp.tool()(add_dependency)
    mcp.tool()(remove_dependency)
    
    # Register additional tools
    register_additional_tools(mcp)
