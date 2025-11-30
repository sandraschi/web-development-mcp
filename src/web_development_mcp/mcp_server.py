"""
Web Development MCP Server - FastMCP 2.10 Implementation

Universal web development operations server with modular tool organization.
Austrian dev efficiency: One unified interface for entire web development stack.
"""

import logging
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Web Development")

# Import and register tool modules
from .tools import (
    scaffolding_tools,
    package_tools,
    build_tools,
    component_tools
)

# Register all tool groups
scaffolding_tools.register_tools(mcp)
package_tools.register_tools(mcp)
build_tools.register_tools(mcp)
component_tools.register_tools(mcp)

logger.info("Web Development MCP server initialized with all tool modules")
