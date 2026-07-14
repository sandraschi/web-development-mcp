"""
Server entry point for web-development-mcp.

Exposes main_stdio and app for pyproject.scripts and MCP entry points.
"""

from .mcp_server import main, mcp


# Stdio entry point used by CLI and by web-development-mcp-server script
def main_stdio():
    """Run the MCP server in stdio mode (for Claude Desktop / Cursor)."""
    main()


# ASGI app for HTTP mode (uvicorn)
def create_server():
    """Return the FastMCP instance for MCP entry point."""
    return mcp


# FastAPI/ASGI app when running with uvicorn (e.g. cli --http)
try:
    app = mcp.http_app(path="/")
except AttributeError:
    app = None  # older FastMCP may not have http_app
