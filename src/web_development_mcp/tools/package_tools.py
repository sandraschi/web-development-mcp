"""
Package management tools for npm, yarn, pnpm, and bun.

Handles dependency installation, updates, auditing, and optimization.
"""

import json
import logging
import subprocess
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _detect_framework(deps: dict, dev_deps: dict) -> str | None:
    """Detect the frontend framework being used.

    Args:
        deps: Production dependencies
        dev_deps: Development dependencies

    Returns:
        Framework name or None
    """
    all_deps = {**deps, **dev_deps}

    if "next" in all_deps:
        return "Next.js"
    elif "nuxt" in all_deps:
        return "Nuxt"
    elif "@angular/core" in all_deps:
        return "Angular"
    elif "vue" in all_deps:
        return "Vue"
    elif "react" in all_deps:
        return "React"
    elif "svelte" in all_deps or "@sveltejs/kit" in all_deps:
        return "Svelte/SvelteKit"
    elif "solid-js" in all_deps:
        return "Solid"
    elif "preact" in all_deps:
        return "Preact"
    return None


def _detect_build_tool(deps: dict, dev_deps: dict) -> str | None:
    """Detect the build tool being used.

    Args:
        deps: Production dependencies
        dev_deps: Development dependencies

    Returns:
        Build tool name or None
    """
    all_deps = {**deps, **dev_deps}

    if "vite" in all_deps:
        return "Vite"
    elif "webpack" in all_deps:
        return "Webpack"
    elif "rollup" in all_deps:
        return "Rollup"
    elif "esbuild" in all_deps:
        return "esbuild"
    elif "parcel" in all_deps:
        return "Parcel"
    elif "turbopack" in all_deps:
        return "Turbopack"
    return None


def detect_package_manager(project_path: str) -> dict[str, Any]:
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
            if (path / "bun.lock").exists():
                package_managers.append("bun")
            if (path / "pnpm-lock.yaml").exists():
            package_managers.append("pnpm")

        # Check for package.json
        package_json_exists = (path / "package.json").exists()

        # Determine primary package manager
        primary = None
        if len(package_managers) == 1:
            primary = package_managers[0]
        elif "bun" in package_managers:
            primary = "bun"  # bun takes precedence
        elif "pnpm" in package_managers:
            primary = "pnpm"  # pnpm takes precedence
        elif "yarn" in package_managers:
            primary = "yarn"  # yarn over npm
        elif "npm" in package_managers:
            primary = "npm"

        return {
            "success": True,
            "project_path": str(project_path),
            "package_managers": package_managers,
            "primary_manager": primary,
            "package_json_exists": package_json_exists,
            "package_json_path": str(path / "package.json") if package_json_exists else None,
            "lock_files": {
                "npm": (path / "package-lock.json").exists(),
                "yarn": (path / "yarn.lock").exists(),
                "bun": (path / "bun.lock").exists(),
                "pnpm": (path / "pnpm-lock.yaml").exists(),
            },
        }

    except Exception as e:
        logger.error(f"Error detecting package manager: {e}")
        return {"success": False, "error": str(e)}


def install_packages(
    project_path: str,
    packages: list[str],
    package_manager: str | None = None,
    dev_dependencies: bool = False,
) -> dict[str, Any]:
    """Install npm packages in a project.

    Args:
        project_path: Path to the project directory
        packages: List of package names to install
        package_manager: Specific package manager to use (auto-detect if None)
        dev_dependencies: Install as dev dependencies

    Returns:
        Dictionary with installation results
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
        elif package_manager == "bun":
            cmd = ["bun", "add"]
            if dev_dependencies:
                cmd.append("-d")
            cmd.extend(packages)
        elif package_manager == "pnpm":
            cmd = ["pnpm", "add"]
            if dev_dependencies:
                cmd.append("--save-dev")
            cmd.extend(packages)
        else:
            return {"success": False, "error": f"Unsupported package manager: {package_manager}"}

        # Execute command
        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

        return {
            "success": result.returncode == 0,
            "package_manager": package_manager,
            "packages_installed": packages if result.returncode == 0 else [],
            "dev_dependencies": dev_dependencies,
            "command": " ".join(cmd),
            "output": result.stdout if result.returncode == 0 else result.stderr,
            "error": result.stderr if result.returncode != 0 else None,
        }

    except Exception as e:
        logger.error(f"Error installing packages: {e}")
        return {"success": False, "error": str(e)}


def analyze_package_json(project_path: str) -> dict[str, Any]:
    """Analyze package.json for insights and potential issues.

    Args:
        project_path: Path to the project directory

    Returns:
        Dictionary with analysis results
    """
    try:
        path = Path(project_path)
        package_json_path = path / "package.json"

        if not package_json_path.exists():
            return {"success": False, "error": "package.json not found"}

        with open(package_json_path, encoding="utf-8") as f:
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
        known_issues = ["node-sass", "request", "bower"]

        for pkg in list(deps.keys()) + list(dev_deps.keys()):
            if pkg in known_issues:
                potentially_vulnerable.append(pkg)

        return {
            "success": True,
            "project_path": str(project_path),
            "package_info": {
                "name": package_data.get("name"),
                "version": package_data.get("version"),
                "description": package_data.get("description"),
                "scripts": list(package_data.get("scripts", {}).keys()),
            },
            "dependencies": {
                "production": len(deps),
                "development": len(dev_deps),
                "peer": len(peer_deps),
                "total": len(deps) + len(dev_deps) + len(peer_deps),
            },
            "analysis": {
                "has_typescript": has_typescript,
                "has_tsconfig": has_ts_config,
                "has_testing": has_testing,
                "framework_detected": _detect_framework(deps, dev_deps),
                "build_tool": _detect_build_tool(deps, dev_deps),
            },
            "issues": issues,
            "warnings": warnings,
            "potentially_vulnerable": potentially_vulnerable,
        }

    except Exception as e:
        logger.error(f"Error analyzing package.json: {e}")
        return {"success": False, "error": str(e)}


def update_packages(
    project_path: str,
    packages: list[str] | None = None,
    package_manager: str | None = None,
    check_only: bool = False,
) -> dict[str, Any]:
    """Update npm packages to latest versions.

    Args:
        project_path: Path to the project directory
        packages: Specific packages to update (update all if None)
        package_manager: Package manager to use (auto-detect if None)
        check_only: Only check for updates without installing

    Returns:
        Dictionary with update results
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
                cmd = ["npm", "outdated", "--json"]
        elif package_manager == "yarn":
            cmd = ["yarn", "outdated", "--json"]
        elif package_manager == "bun":
            cmd = ["bun", "outdated", "--json"]
        elif package_manager == "pnpm":
            cmd = ["pnpm", "outdated", "--json"]
            else:
                return {"success": False, "error": f"Unsupported: {package_manager}"}
        else:
            if package_manager == "npm":
                cmd = ["npm", "update"]
                if packages:
                    cmd.extend(packages)
            elif package_manager == "yarn":
                cmd = ["yarn", "upgrade"]
                if packages:
                    cmd.extend(packages)
            elif package_manager == "bun":
                cmd = ["bun", "update"]
                if packages:
                    cmd.extend(packages)
            elif package_manager == "pnpm":
                cmd = ["pnpm", "update"]
                if packages:
                    cmd.extend(packages)
            else:
                return {"success": False, "error": f"Unsupported: {package_manager}"}

        # Execute command
        result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True, timeout=300)

        # Parse output
        output = {}
        if check_only:
            try:
                output = json.loads(result.stdout)
            except json.JSONDecodeError:
                output = result.stdout

        return {
            "success": result.returncode == 0,
            "package_manager": package_manager,
            "check_only": check_only,
            "packages_updated": packages if not check_only and result.returncode == 0 else [],
            "outdated_packages": output if check_only and result.returncode == 0 else {},
            "command": " ".join(cmd),
            "output": result.stdout if result.returncode == 0 else result.stderr,
            "error": result.stderr if result.returncode != 0 else None,
        }

    except Exception as e:
        logger.error(f"Error updating packages: {e}")
        return {"success": False, "error": str(e)}


def remove_packages(project_path: str, packages: list[str], package_manager: str | None = None) -> dict[str, Any]:
    """Remove npm packages from a project.

    Args:
        project_path: Path to the project directory
        packages: List of package names to remove
        package_manager: Specific package manager to use (auto-detect if None)

    Returns:
        Dictionary with removal results
    """
    try:
        if not package_manager:
            detection = detect_package_manager(project_path)
            if not detection["success"]:
                return detection
            package_manager = detection["primary_manager"] or "npm"

        if package_manager == "npm":
            cmd = ["npm", "uninstall"] + packages
        elif package_manager == "yarn":
            cmd = ["yarn", "remove"] + packages
        elif package_manager == "bun":
            cmd = ["bun", "remove"] + packages
        elif package_manager == "pnpm":
            cmd = ["pnpm", "remove"] + packages
        else:
            return {"success": False, "error": f"Unsupported: {package_manager}"}

        result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True, timeout=300)

        return {
            "success": result.returncode == 0,
            "package_manager": package_manager,
            "packages_removed": packages if result.returncode == 0 else [],
            "command": " ".join(cmd),
            "output": result.stdout if result.returncode == 0 else result.stderr,
            "error": result.stderr if result.returncode != 0 else None,
        }

    except Exception as e:
        logger.error(f"Error removing packages: {e}")
        return {"success": False, "error": str(e)}


def register_tools(mcp):
    """Register all package management tools with the MCP server.

    Args:
        mcp: The MCP server instance to register tools with
    """
    mcp.tool()(detect_package_manager)
    mcp.tool()(install_packages)
    mcp.tool()(analyze_package_json)
    mcp.tool()(update_packages)
    mcp.tool()(remove_packages)

    logger.info("Package management tools registered successfully")
