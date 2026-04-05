"""
Validation utilities for the Web Development MCP.

Provides functions for validating project names, paths, and other inputs.
"""

import platform
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

# Regular expressions for validation
PROJECT_NAME_PATTERN = r"^[a-z][a-z0-9\-_\.]{0,213}$"
PACKAGE_NAME_PATTERN = r"^(@[a-z0-9-~][a-z0-9-._~]*/)?[a-z0-9-~][a-z0-9-._~]*$"
NODE_VERSION_PATTERN = r"^v?\d+\.\d+\.\d+$"


def is_valid_project_name(name: str) -> Tuple[bool, str]:
    """
    Validate a project name according to npm naming conventions.

    Args:
        name: The project name to validate

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not name:
        return False, "Project name cannot be empty"

    if not re.match(PROJECT_NAME_PATTERN, name):
        return False, (
            "Project name must be lowercase, start with a letter, and only contain "
            "alphanumeric characters, hyphens, underscores, or dots"
        )

    if len(name) > 214:
        return False, "Project name cannot be longer than 214 characters"

    if name.startswith(".") or name.startswith("_") or name.startswith("-") or name.startswith("@"):
        return False, "Project name cannot start with '.', '_', '-', or '@'"

    if name == "node_modules" or name == "favicon.ico":
        return False, f"Project name cannot be '{name}'"

    if not re.match(r"^[a-z]", name):
        return False, "Project name must start with a letter"

    return True, ""


def validate_project_path(path: Union[str, Path], create: bool = False) -> Tuple[bool, str]:
    """
    Validate a project directory path.

    Args:
        path: The path to validate
        create: If True, create the directory if it doesn't exist

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    path = Path(path).resolve()

    if path.exists():
        if not path.is_dir():
            return False, f"Path exists but is not a directory: {path}"

        try:
            # Check if directory is empty
            if any(path.iterdir()):
                return False, f"Directory is not empty: {path}"
        except PermissionError:
            return False, f"Permission denied when accessing: {path}"
    else:
        if create:
            try:
                path.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                return False, f"Failed to create directory: {e}"
        else:
            return False, f"Directory does not exist: {path}"

    # Check if we have write permissions
    try:
        test_file = path / ".permission_test"
        test_file.touch()
        test_file.unlink()
    except (OSError, PermissionError):
        return False, f"No write permissions in directory: {path}"

    return True, ""


def validate_package_name(name: str) -> Tuple[bool, str]:
    """
    Validate an npm package name.

    Args:
        name: The package name to validate

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not name:
        return False, "Package name cannot be empty"

    if len(name) > 214:
        return False, "Package name cannot be longer than 214 characters"

    if name.startswith(".") or name.startswith("_"):
        return False, "Package name cannot start with '.' or '_'"

    if name.startswith("@"):
        # Handle scoped packages
        parts = name.split("/")
        if len(parts) != 2 or not parts[1]:
            return False, "Invalid scoped package name format. Expected: @scope/name"

        scope = parts[0][1:]  # Remove @
        pkg_name = parts[1]  # noqa: F841

        if not re.match(PACKAGE_NAME_PATTERN, scope):
            return False, "Invalid scope name"
    else:
        if not re.match(PACKAGE_NAME_PATTERN, name):
            return False, "Invalid package name"

    # Check for node.js core module names
    core_modules = [
        "assert",
        "buffer",
        "child_process",
        "cluster",
        "crypto",
        "dgram",
        "dns",
        "domain",
        "events",
        "fs",
        "http",
        "https",
        "net",
        "os",
        "path",
        "punycode",
        "querystring",
        "readline",
        "stream",
        "string_decoder",
        "tls",
        "tty",
        "url",
        "util",
        "v8",
        "vm",
        "zlib",
    ]

    if name.lower() in core_modules:
        return False, f"'{name}' is a core Node.js module name"

    return True, ""


def validate_node_version(version: str) -> Tuple[bool, str]:
    """
    Validate a Node.js version string.

    Args:
        version: The version string to validate (e.g., '14.17.0' or 'v14.17.0')

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not version:
        return False, "Version cannot be empty"

    if not re.match(NODE_VERSION_PATTERN, version):
        return False, "Invalid version format. Expected: X.Y.Z or vX.Y.Z"

    # Remove 'v' prefix if present
    version = version[1:] if version.startswith("v") else version

    try:
        major, minor, patch = map(int, version.split("."))

        # Basic version validation
        if major < 0 or minor < 0 or patch < 0:
            return False, "Version components cannot be negative"

        if major == 0 and minor == 0 and patch == 0:
            return False, "Version cannot be 0.0.0"

    except ValueError:
        return False, "Version components must be integers"

    return True, ""


def check_node_installed() -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Check if Node.js is installed and get version information.

    Returns:
        Tuple[bool, str, Optional[Dict[str, Any]]]:
            (is_installed, message, version_info)
    """
    try:
        # Get Node.js version
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            shell=platform.system() == "Windows",
        )

        if result.returncode != 0:
            return False, "Node.js is not installed or not in PATH", None

        version = result.stdout.strip()

        # Get npm version
        npm_result = subprocess.run(
            ["npm", "--version"],
            capture_output=True,
            text=True,
            shell=platform.system() == "Windows",
        )

        npm_version = npm_result.stdout.strip() if npm_result.returncode == 0 else "unknown"

        version_info = {
            "node": version,
            "npm": npm_version,
            "platform": platform.platform(),
            "system": platform.system(),
            "machine": platform.machine(),
        }

        return True, f"Node.js {version} is installed", version_info

    except Exception as e:
        return False, f"Error checking Node.js installation: {str(e)}", None
