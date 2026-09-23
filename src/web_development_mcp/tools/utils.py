"""
Shared response helpers for Web Development MCP tools.

Dialogic shape: every payload carries a natural-language `message`.
`_error_response` must be called from inside an `except` block — it logs
the active traceback via `logger.exception` (TOOL_DESIGN_STANDARDS §7.1).
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def _success_response(data: Any, message: str = "OK") -> dict[str, Any]:
    """Return a standard success payload for tool responses."""
    return {"success": True, "message": message, "data": data}


def _error_response(message: str, code: str = "error") -> dict[str, Any]:
    """Return a standard error payload (call from inside `except`)."""
    logger.exception("tool error [%s]: %s", code, message)
    return {"success": False, "error": message, "code": code, "message": message}
