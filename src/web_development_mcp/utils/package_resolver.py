"""
Package resolution utilities for the Web Development MCP.

Provides functions for resolving package versions and checking compatibility.
"""

import json
import logging
import re
import subprocess
from pathlib import Path
from typing import Any

import requests
from semver import VersionInfo

logger = logging.getLogger(__name__)

# Cache for package versions
_package_cache: dict[str, Any] = {}


def _run_command(cmd: list[str], cwd: str | Path | None = None) -> tuple[bool, str]:
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True, check=False)

        if result.returncode != 0:
            error_msg = result.stderr.strip() or "Unknown error"
            return False, error_msg

        return True, result.stdout.strip()

    except Exception as e:
        return False, str(e)


def get_latest_package_versions(packages: list[str], registry: str = "https://registry.npmjs.org") -> dict[str, str]:
    """
    Get the latest versions of the specified packages from the npm registry.

    Args:
        packages: List of package names to look up
        registry: npm registry URL (default: https://registry.npmjs.org)

    Returns:
        Dict mapping package names to their latest versions
    """
    results = {}

    for pkg in packages:
        if not pkg:
            continue

        cache_key = f"{registry}:{pkg}"

        # Check cache first
        if cache_key in _package_cache:
            results[pkg] = _package_cache[cache_key]
            continue

        try:
            # Try to get the package info from the registry
            url = f"{registry}/{pkg}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            latest_version = data.get("dist-tags", {}).get("latest")

            if latest_version:
                results[pkg] = latest_version
                _package_cache[cache_key] = latest_version
            else:
                logger.warning(f"No latest version found for package: {pkg}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch package info for {pkg}: {e}")
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Invalid response for package {pkg}: {e}")

    return results


def resolve_package_version(
    package_name: str,
    version_constraint: str | None = None,
    registry: str = "https://registry.npmjs.org",
) -> tuple[bool, str, dict[str, Any] | None]:
    """
    Resolve a package version based on the given constraint.

    Args:
        package_name: Name of the package
        version_constraint: Version constraint (e.g., '^1.0.0', 'latest', 'beta')
        registry: npm registry URL

    Returns:
        Tuple[success, message, version_info]
    """
    if not package_name:
        return False, "Package name cannot be empty", None

    try:
        # If no version constraint is provided, get the latest version
        if not version_constraint or version_constraint.lower() == "latest":
            versions = get_latest_package_versions([package_name], registry)
            if package_name in versions:
                version = versions[package_name]
                return (
                    True,
                    f"Resolved {package_name}@{version}",
                    {
                        "package": package_name,
                        "version": version,
                        "constraint": version_constraint or "latest",
                        "resolved": version,
                    },
                )
            else:
                return False, f"Could not find latest version for {package_name}", None

        # Check if the version constraint is a specific version
        if re.match(r"^[0-9]", version_constraint):
            # Try to parse as a semantic version
            try:
                version = VersionInfo.parse(version_constraint)
                return (
                    True,
                    f"Using specified version {version}",
                    {
                        "package": package_name,
                        "version": str(version),
                        "constraint": version_constraint,
                        "resolved": str(version),
                    },
                )
            except ValueError:
                pass

        # For other constraints (^, ~, etc.), we'll need to query the registry
        try:
            url = f"{registry}/{package_name}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            versions = list(data.get("versions", {}).keys())

            if not versions:
                return False, f"No versions found for package: {package_name}", None

            # Sort versions in descending order
            sorted_versions = sorted(
                versions,
                key=lambda v: VersionInfo.parse(v) if VersionInfo.is_valid(v) else VersionInfo(0, 0, 0),
                reverse=True,
            )

            # Find the highest version that satisfies the constraint
            for version in sorted_versions:
                if VersionInfo.is_valid(version):
                    ver = VersionInfo.parse(version)
                    # This is a simplified check - in a real implementation, you'd want to
                    # properly handle all npm version specifiers
                    if version_constraint.startswith("^"):
                        # Caret range (e.g., ^1.2.3)
                        min_ver = VersionInfo.parse(version_constraint[1:])
                        if ver.major == min_ver.major and ver >= min_ver:
                            return (
                                True,
                                f"Resolved {package_name}@{version}",
                                {
                                    "package": package_name,
                                    "version": version,
                                    "constraint": version_constraint,
                                    "resolved": version,
                                },
                            )
                    elif version_constraint.startswith("~"):
                        # Tilde range (e.g., ~1.2.3)
                        min_ver = VersionInfo.parse(version_constraint[1:])
                        if ver.major == min_ver.major and ver.minor == min_ver.minor and ver >= min_ver:
                            return (
                                True,
                                f"Resolved {package_name}@{version}",
                                {
                                    "package": package_name,
                                    "version": version,
                                    "constraint": version_constraint,
                                    "resolved": version,
                                },
                            )
                    elif version_constraint.startswith(">="):
                        # Greater than or equal to
                        min_ver = VersionInfo.parse(version_constraint[2:])
                        if ver >= min_ver:
                            return (
                                True,
                                f"Resolved {package_name}@{version}",
                                {
                                    "package": package_name,
                                    "version": version,
                                    "constraint": version_constraint,
                                    "resolved": version,
                                },
                            )
                    elif version_constraint.startswith(">"):
                        # Greater than
                        min_ver = VersionInfo.parse(version_constraint[1:])
                        if ver > min_ver:
                            return (
                                True,
                                f"Resolved {package_name}@{version}",
                                {
                                    "package": package_name,
                                    "version": version,
                                    "constraint": version_constraint,
                                    "resolved": version,
                                },
                            )
                    elif version_constraint.startswith("<="):
                        # Less than or equal to
                        max_ver = VersionInfo.parse(version_constraint[2:])
                        if ver <= max_ver:
                            return (
                                True,
                                f"Resolved {package_name}@{version}",
                                {
                                    "package": package_name,
                                    "version": version,
                                    "constraint": version_constraint,
                                    "resolved": version,
                                },
                            )
                    elif version_constraint.startswith("<"):
                        # Less than
                        max_ver = VersionInfo.parse(version_constraint[1:])
                        if ver < max_ver:
                            return (
                                True,
                                f"Resolved {package_name}@{version}",
                                {
                                    "package": package_name,
                                    "version": version,
                                    "constraint": version_constraint,
                                    "resolved": version,
                                },
                            )
                    elif version_constraint == version:
                        # Exact match
                        return (
                            True,
                            f"Resolved {package_name}@{version}",
                            {
                                "package": package_name,
                                "version": version,
                                "constraint": version_constraint,
                                "resolved": version,
                            },
                        )

            return False, f"No version found matching constraint: {version_constraint}", None

        except requests.exceptions.RequestException as e:
            return False, f"Failed to fetch package info: {e}", None
        except Exception as e:
            return False, f"Error resolving package version: {e}", None

    except Exception as e:
        logger.exception(f"Unexpected error in resolve_package_version: {e}")
        return False, f"Unexpected error: {e}", None


def get_compatible_versions(
    package_name: str,
    dependency_constraints: dict[str, str],
    registry: str = "https://registry.npmjs.org",
) -> dict[str, str]:
    """
    Find versions of a package that are compatible with the given dependency constraints.

    Args:
        package_name: Name of the package to check
        dependency_constraints: Dictionary of package names to version constraints
        registry: npm registry URL

    Returns:
        Dictionary mapping compatible package versions to their dependency sets
    """
    # This is a simplified implementation. In a real-world scenario, you would:
    # 1. Fetch the package metadata from the registry
    # 2. For each version, check if its dependencies are compatible with the constraints
    # 3. Return a list of compatible versions with their dependency sets

    # For now, we'll just return the latest version that satisfies the constraints
    # and a note that this is a simplified implementation

    latest_versions = get_latest_package_versions([package_name], registry)

    if package_name in latest_versions:
        version = latest_versions[package_name]
        return {
            version: {
                "dependencies": {},
                "devDependencies": {},
                "peerDependencies": {},
                "note": "This is a simplified implementation. Full dependency resolution is not implemented.",
            }
        }

    return {}


def install_package(
    package_name: str,
    version: str | None = None,
    cwd: str | Path | None = None,
    save_dev: bool = False,
    registry: str = "https://registry.npmjs.org",
) -> tuple[bool, str]:
    """
    Install a package using npm or yarn.

    Args:
        package_name: Name of the package to install
        version: Version to install (default: latest)
        cwd: Working directory for the installation
        save_dev: Whether to install as a dev dependency
        registry: npm registry URL

    Returns:
        Tuple[success, message]
    """
    if not package_name:
        return False, "Package name cannot be empty"

    # Check if npm is available
    npm_available = _run_command(["npm", "--version"])[0]
    yarn_available = _run_command(["yarn", "--version"])[0]

    if not (npm_available or yarn_available):
        return False, "Neither npm nor yarn is available. Please install Node.js and try again."

    # Build the package spec (name@version)
    package_spec = package_name
    if version:
        package_spec = f"{package_name}@{version}"

    # Determine the package manager to use
    use_yarn = yarn_available

    try:
        if use_yarn:
            cmd = ["yarn", "add"]
            if save_dev:
                cmd.append("--dev")
            cmd.extend(["--registry", registry, package_spec])
        else:
            cmd = ["npm", "install"]
            if save_dev:
                cmd.append("--save-dev")
            cmd.extend(["--registry", registry, package_spec])

        success, output = _run_command(cmd, cwd)
        if success:
            return True, f"Successfully installed {package_spec}"
        else:
            return False, f"Failed to install {package_spec}: {output}"

    except Exception as e:
        return False, f"Error installing package: {e}"
