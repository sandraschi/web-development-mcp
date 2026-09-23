"""
Package management tools for npm, yarn, pnpm, and bun.

Handles dependency installation, updates, auditing, and optimization.
"""

import json
import logging
import subprocess
from pathlib import Path
from typing import Annotated, Any

from pydantic import Field

logger = logging.getLogger(__name__)

_READ_ONLY = {"readonly": True}
_MUTATING = {}
_DESTRUCTIVE = {"destructive": True}


def _detect_framework(deps: dict, dev_deps: dict) -> str | None:
    """Detect the frontend framework being used."""
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
    """Detect the build tool being used."""
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


def detect_package_manager(
    project_path: Annotated[str, Field(description="Path to the project directory")],
) -> dict[str, Any]:
    """Detect which package manager is being used in a project.

    Inspects lockfiles (package-lock.json, yarn.lock, bun.lock,
    pnpm-lock.yaml) and reports the primary manager by precedence
    bun > pnpm > yarn > npm.

    ## Return Format

    `{success, message, project_path, package_managers, primary_manager,
    package_json_exists, package_json_path, lock_files}`.

    ## Examples

    - detect_package_manager(project_path="D:/proj") ->
      `{success: True, primary_manager: "bun", ...}` when bun.lock exists.
    - Empty directory -> `{success: True, primary_manager: None, ...}`.
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
            "message": f"Detected package manager: {primary or 'none'}",
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
        logger.exception(f"Error detecting package manager: {e}")
        return {"success": False, "error": str(e), "message": f"Package manager detection failed: {e}"}


def install_packages(
    project_path: Annotated[str, Field(description="Path to the project directory")],
    packages: Annotated[list[str], Field(description="List of package names to install")],
    package_manager: Annotated[str | None, Field(description="Package manager to use (auto-detect if None)")] = None,
    dev_dependencies: Annotated[bool, Field(description="Install as dev dependencies")] = False,
) -> dict[str, Any]:
    """Install packages in a project with the detected (or given) manager.

    Runs the real install subprocess (npm/yarn/bun/pnpm) with a 5-minute
    timeout and reports stdout/stderr. Mutates `node_modules` and lockfiles.

    ## Return Format

    `{success, message, package_manager, packages_installed,
    dev_dependencies, command, output, error}`.

    ## Examples

    - install_packages(project_path="D:/proj", packages=["axios"]) ->
      runs `npm install axios` (or the detected manager equivalent).
    - install_packages(..., dev_dependencies=True) -> `npm install --save-dev ...`.
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
            return {
                "success": False,
                "error": f"Unsupported package manager: {package_manager}",
                "message": f"Unsupported package manager: {package_manager}",
            }

        # Execute command
        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

        ok = result.returncode == 0
        return {
            "success": ok,
            "message": f"Installed {packages} with {package_manager}" if ok else f"Install failed: {result.stderr}",
            "package_manager": package_manager,
            "packages_installed": packages if ok else [],
            "dev_dependencies": dev_dependencies,
            "command": " ".join(cmd),
            "output": result.stdout if ok else result.stderr,
            "error": result.stderr if not ok else None,
        }

    except Exception as e:
        logger.exception(f"Error installing packages: {e}")
        return {"success": False, "error": str(e), "message": f"Package install failed: {e}"}


def analyze_package_json(
    project_path: Annotated[str, Field(description="Path to the project directory")],
) -> dict[str, Any]:
    """Analyze package.json for insights and potential issues.

    Read-only: counts dependencies, detects framework/build tool, flags
    outdated React, missing tsconfig, absent testing setup, and known
    vulnerable packages (node-sass, request, bower).

    ## Return Format

    `{success, message, project_path, package_info, dependencies, analysis,
    issues, warnings, potentially_vulnerable}`. Missing package.json ->
    `{success: False, error, message}`.

    ## Examples

    - analyze_package_json(project_path="D:/proj") ->
      `{success: True, analysis: {framework_detected: "React", ...}, ...}`.
    """
    try:
        path = Path(project_path)
        package_json_path = path / "package.json"

        if not package_json_path.exists():
            return {
                "success": False,
                "error": "package.json not found",
                "message": f"No package.json in {project_path}",
            }

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
            "message": f"Analyzed {package_data.get('name', 'package.json')}: {len(deps) + len(dev_deps)} deps",
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
        logger.exception(f"Error analyzing package.json: {e}")
        return {"success": False, "error": str(e), "message": f"package.json analysis failed: {e}"}


def update_packages(
    project_path: Annotated[str, Field(description="Path to the project directory")],
    packages: Annotated[list[str] | None, Field(description="Specific packages to update (all if None)")] = None,
    package_manager: Annotated[str | None, Field(description="Package manager to use (auto-detect if None)")] = None,
    check_only: Annotated[bool, Field(description="Only check for updates without installing")] = False,
) -> dict[str, Any]:
    """Update project packages to latest versions (or just check).

    With check_only=True this is read-only (`npm outdated` et al);
    otherwise it mutates lockfiles and `node_modules`.

    ## Return Format

    `{success, message, package_manager, check_only, packages_updated,
    outdated_packages, command, output, error}`.

    ## Examples

    - update_packages(project_path="D:/proj", check_only=True) ->
      `{success: True, outdated_packages: {...}}` without changing anything.
    - update_packages(project_path="D:/proj", packages=["react"]) ->
      runs the manager's update/upgrade for react.
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
                return {
                    "success": False,
                    "error": f"Unsupported: {package_manager}",
                    "message": f"Unsupported package manager: {package_manager}",
                }
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
                return {
                    "success": False,
                    "error": f"Unsupported: {package_manager}",
                    "message": f"Unsupported package manager: {package_manager}",
                }

        # Execute command
        result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True, timeout=300)

        # Parse output
        output = {}
        if check_only:
            try:
                output = json.loads(result.stdout)
            except json.JSONDecodeError:
                output = result.stdout

        ok = result.returncode == 0
        return {
            "success": ok,
            "message": f"Update check via {package_manager}: {'ok' if ok else 'failed'}"
            if check_only
            else f"Updated {packages or 'all'} with {package_manager}: {'ok' if ok else 'failed'}",
            "package_manager": package_manager,
            "check_only": check_only,
            "packages_updated": packages if not check_only and ok else [],
            "outdated_packages": output if check_only and ok else {},
            "command": " ".join(cmd),
            "output": result.stdout if ok else result.stderr,
            "error": result.stderr if not ok else None,
        }

    except Exception as e:
        logger.exception(f"Error updating packages: {e}")
        return {"success": False, "error": str(e), "message": f"Package update failed: {e}"}


def remove_packages(
    project_path: Annotated[str, Field(description="Path to the project directory")],
    packages: Annotated[list[str], Field(description="List of package names to remove")],
    package_manager: Annotated[str | None, Field(description="Package manager to use (auto-detect if None)")] = None,
) -> dict[str, Any]:
    """Remove packages from a project. DESTRUCTIVE: edits package.json,
    lockfiles, and deletes installed code.

    ## Return Format

    `{success, message, package_manager, packages_removed, command, output,
    error}`.

    ## Examples

    - remove_packages(project_path="D:/proj", packages=["moment"]) ->
      runs `npm uninstall moment` (or the detected manager equivalent).
    """
    try:
        if not package_manager:
            detection = detect_package_manager(project_path)
            if not detection["success"]:
                return detection
            package_manager = detection["primary_manager"] or "npm"

        if package_manager == "npm":
            cmd = ["npm", "uninstall", *packages]
        elif package_manager == "yarn":
            cmd = ["yarn", "remove", *packages]
        elif package_manager == "bun":
            cmd = ["bun", "remove", *packages]
        elif package_manager == "pnpm":
            cmd = ["pnpm", "remove", *packages]
        else:
            return {
                "success": False,
                "error": f"Unsupported: {package_manager}",
                "message": f"Unsupported package manager: {package_manager}",
            }

        result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True, timeout=300)

        ok = result.returncode == 0
        return {
            "success": ok,
            "message": f"Removed {packages} with {package_manager}" if ok else f"Removal failed: {result.stderr}",
            "package_manager": package_manager,
            "packages_removed": packages if ok else [],
            "command": " ".join(cmd),
            "output": result.stdout if ok else result.stderr,
            "error": result.stderr if not ok else None,
        }

    except Exception as e:
        logger.exception(f"Error removing packages: {e}")
        return {"success": False, "error": str(e), "message": f"Package removal failed: {e}"}


def register_tools(mcp):
    """Register all package management tools with the MCP server."""
    mcp.tool(annotations=_READ_ONLY)(detect_package_manager)
    mcp.tool(annotations=_MUTATING)(install_packages)
    mcp.tool(annotations=_READ_ONLY)(analyze_package_json)
    mcp.tool(annotations=_MUTATING)(update_packages)
    mcp.tool(annotations=_DESTRUCTIVE)(remove_packages)

    logger.info("Package management tools registered successfully")
