"""
Server maintenance tools for Web Development MCP.

Self-termination for agents and the fleet launcher (the matching REST
endpoint is POST /api/shutdown on the webapp backend).
"""

import os
import threading
import time
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

_DESTRUCTIVE = {"destructive": True}


def register_tools(mcp: FastMCP):
    """Register maintenance tools with the FastMCP instance."""

    @mcp.tool(annotations=_DESTRUCTIVE)
    def shutdown_server(
        delay_seconds: Annotated[float, Field(description="Grace period before process exit (seconds)")] = 0.5,
    ) -> dict:
        """Shut the MCP server process down after a grace period.

        DESTRUCTIVE: the process exits via os._exit — in-flight work that
        has not checkpointed is lost. Prefer this over killing the process
        externally so the 200 response confirms the request landed.

        ## Return Format

        `{success, message, delay_seconds}`.

        ## Examples

        - shutdown_server() -> `{success: True, ...}`, process exits ~0.5 s later.
        - shutdown_server(delay_seconds=5) -> 5 s grace period.
        """
        delay = max(0.0, float(delay_seconds))

        def _exit() -> None:
            time.sleep(delay)
            os._exit(0)

        threading.Thread(target=_exit, daemon=True).start()
        return {
            "success": True,
            "message": f"Shutting down in {delay} s.",
            "delay_seconds": delay,
        }
