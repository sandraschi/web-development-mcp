"""
Web Development MCP Server - FastMCP 2.10 Implementation

Universal web development operations server with modular tool organization.
Austrian dev efficiency: One unified interface for entire web development stack.
"""

import logging
import os

from fastmcp import FastMCP
from fastmcp.server import create_proxy
from starlette.requests import Request
from starlette.responses import JSONResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("web-development")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"status": "healthy", "server": "web-development-mcp"})


# MCP Bridge: proxy tools from other MCP servers via MCP_BRIDGE_URLS
_bridge_proxies: list[str] = []
bridge_urls = os.getenv("MCP_BRIDGE_URLS", "")
if bridge_urls:
    for url in bridge_urls.split(","):
        url = url.strip()
        if url:
            try:
                mcp.add_provider(create_proxy(url))
                _bridge_proxies.append(url)
            except Exception:
                pass

# Import and register tool modules
from .tools import (
    agentic_tools,
    build_tools,
    component_tools,
    dashboard_tools,
    help_tools,
    package_tools,
    scaffolding_tools,
)
from .transport import run_server

# Register all tool groups
scaffolding_tools.register_tools(mcp)
package_tools.register_tools(mcp)
build_tools.register_tools(mcp)
component_tools.register_tools(mcp)
dashboard_tools.register_tools(mcp)
agentic_tools.register_tools(mcp)
help_tools.register_tools(mcp)

logger.info("Web Development MCP server initialized with all tool modules")


def main():
    """Run the MCP server."""
    run_server(mcp, server_name="web-development")
