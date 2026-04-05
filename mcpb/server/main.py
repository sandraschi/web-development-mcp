#!/usr/bin/env python3
"""
Web Development MCP Server - MCPB Package Entry Point

This is the main entry point for the MCPB-packaged Web Development MCP server.
It provides AI-powered 3D creation and manipulation capabilities.
"""

import os
import sys

# Add the lib directory to Python path for dependencies
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

# Import and run the actual server
from web_development_mcp.server import main  # noqa: E402

if __name__ == "__main__":
    main()
