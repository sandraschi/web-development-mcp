"""
Shared response helpers for Web Development MCP tools.
"""

from typing import Any


def _success_response(data: Any) -> dict[str, Any]:
    """Return a standard success payload for tool responses."""
    return {"success": True, "data": data}


def _error_response(message: str, code: str = "error") -> dict[str, Any]:
    """Return a standard error payload for tool responses."""
    return {"success": False, "error": message, "code": code}
