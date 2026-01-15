import asyncio
import logging
import sys
from pathlib import Path

# Add src to path if not already there
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from web_development_mcp.mcp_server import mcp

def main():
    """Main entry point for Web Development MCP server."""
    try:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logging.info("Starting Web Development MCP server")
        mcp.run()  # FastMCP 2.10 handles stdio automatically
    except KeyboardInterrupt:
        logging.info("\nWeb Development MCP server stopped")
    except Exception as e:
        logging.error(f"Server error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
