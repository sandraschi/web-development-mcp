"""
Web Development MCP - FastMCP 2.10 Implementation

Universal web development operations server supporting:
- Frontend frameworks: React, Vue, Svelte, Next.js
- Package management: npm, yarn, pnpm operations
- Build tools: Vite, TypeScript, ESLint configuration
- Code generation: Components, templates, best practices

Austrian dev efficiency: One unified interface for entire web development stack.
"""

__version__ = "1.0.0"
__author__ = "Sandra"

from .mcp_server import mcp

__all__ = ["mcp"]
