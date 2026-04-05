"""Command-line interface for Web Development MCP."""

import argparse
import logging
import sys
from pathlib import Path

from web_development_mcp.server import main_stdio

logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Web Development MCP - Professional Web Development Automation Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Web Development MCP Server provides professional web development automation through natural language.
Supports project scaffolding, dependency management, build processes, and more.

EXAMPLES:
  # Run MCP server for Claude Desktop integration
  web-development-mcp --stdio

  # Run HTTP server for web clients
  web-development-mcp --http --host 0.0.0.0 --port 8001

  # Install Claude Desktop configuration
  web-development-mcp --install-config

  # Check Web Development environment and compatibility
  web-development-mcp --check-web-development

  # Run with debug logging
  web-development-mcp --stdio --debug

ENVIRONMENT VARIABLES:
  WEB_DEVELOPMENT_EXECUTABLE    Path to Web Development executable (auto-detected if not set)

For more information, visit: https://github.com/sandraschi/web-development-mcp
        """,
    )

    parser.add_argument(
        "--stdio", action="store_true", help="Run in stdio mode for MCP clients (default)"
    )

    parser.add_argument("--http", action="store_true", help="Run in HTTP mode for web clients")

    parser.add_argument(
        "--host", default="127.0.0.1", help="Host to bind HTTP server to (default: 127.0.0.1)"
    )

    parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind HTTP server to (default: 8000)"
    )

    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    parser.add_argument(
        "--install-config", action="store_true", help="Install Claude Desktop configuration"
    )

    parser.add_argument(
        "--check-web-development",
        action="store_true",
        help="Check Web Development environment and compatibility",
    )

    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="List all available MCP tools and their descriptions",
    )

    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Show current configuration and environment settings",
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    try:
        if args.install_config:
            install_claude_config()
            return

        if args.check_web_development:
            check_web_development_installation()
            return

        if args.list_tools:
            list_available_tools()
            return

        if args.show_config:
            show_configuration()
            return

        if args.http:
            # Run HTTP server
            logger.info(f"Starting HTTP server on {args.host}:{args.port}")
            import uvicorn

            from web_development_mcp.server import app

            uvicorn.run(
                app, host=args.host, port=args.port, log_level="debug" if args.debug else "info"
            )
        else:
            # Run stdio mode (default for MCP clients)
            logger.info("Starting MCP server in stdio mode")
            main_stdio()

    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {e}")
        if args.debug:
            import traceback

            traceback.print_exc()
        sys.exit(1)


def install_claude_config():
    """Install Claude Desktop configuration."""
    import json
    import platform

    system = platform.system().lower()

    if system == "windows":
        config_dir = Path.home() / "AppData" / "Roaming" / "Claude"
    elif system == "darwin":  # macOS
        config_dir = Path.home() / "Library" / "Application Support" / "Claude"
    elif system == "linux":
        config_dir = Path.home() / ".config" / "Claude"
    else:
        logger.warning(f"Unsupported platform: {system}")
        return

    config_file = config_dir / "claude_desktop_config.json"

    # Create config directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)

    # Load existing config or create new one
    if config_file.exists():
        try:
            with open(config_file) as f:
                config = json.load(f)
        except json.JSONDecodeError:
            logger.warning("Existing config file is corrupted, creating new one")
            config = {"mcpServers": {}}
    else:
        config = {"mcpServers": {}}

    # Add Web Development MCP configuration
    import sys

    python_executable = sys.executable

    config["mcpServers"]["web-development-mcp"] = {
        "command": python_executable,
        "args": ["-c", "from web_development_mcp.server import main_stdio; main_stdio()"],
        "env": {"PYTHONPATH": str(Path(__file__).parent.parent)},
    }

    # Write config file
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

    print("✅ Claude Desktop configuration installed!")
    print(f"📁 Config file: {config_file}")
    print("🔄 Restart Claude Desktop to load the new MCP server")
    print()
    print("To verify installation:")
    print("1. Open Claude Desktop")
    print("2. Ask: 'What Web Development operations can you perform?'")


def check_web_development_installation():
    """Check Web Development environment and compatibility."""
    import shutil
    import subprocess

    print("🔍 Checking Web Development installation...")

    # Check if web-development command is available
    web_development_path = shutil.which("web-development")
    if web_development_path:
        print(f"✅ Web Development found at: {web_development_path}")

        # Try to get version
        try:
            result = subprocess.run(
                [web_development_path, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                # Extract version from first line
                version_line = result.stdout.strip().split("\n")[0]
                print(f"📦 {version_line}")

                # Check if version is compatible
                if "Web Development 3." in version_line or "Web Development 4." in version_line:
                    print("✅ Compatible version detected")
                else:
                    print("⚠️  Version might not be fully compatible (recommended: 3.0+)")
            else:
                print("⚠️  Could not determine Web Development version")

        except subprocess.TimeoutExpired:
            print("⚠️  Web Development command timed out")
        except Exception as e:
            print(f"⚠️  Error checking version: {e}")
    else:
        print("❌ Web Development not found in PATH")
        print()
        print("To install Web Development:")
        print("1. Download from: https://www.web-development.org/download/")
        print("2. Add Web Development to your system PATH")
        print("3. Or set WEB_DEVELOPMENT_EXECUTABLE environment variable")

    # Check Python integration
    try:
        import bpy  # noqa: F401

        print("✅ Web Development Python API (bpy) available")
    except ImportError:
        print("ℹ️  Web Development Python API not available (normal for external MCP usage)")

    print()
    print("🎯 Web Development MCP is ready to use with external Web Development installations!")


def list_available_tools():
    """List all available MCP tools and their descriptions."""
    print("Available Web Development MCP Tools")
    print("=" * 50)

    try:
        # Try to get the app and list tools directly
        from web_development_mcp.app import get_app

        app = get_app()
        if app and hasattr(app, "list_tools"):
            tools = app.list_tools()
            print(f"\nFound {len(tools)} registered tools:")
            for tool in tools:
                print(f"\n- {tool.name}")
                if hasattr(tool, "description") and tool.description:
                    print(f"  {tool.description}")
        else:
            print("MCP server not initialized. Run the server first to see available tools.")
    except Exception as e:
        print(f"Error retrieving tool information: {e}")
        print("Try running 'web-development-mcp --stdio' first to initialize the server.")


def show_configuration():
    """Show current configuration and environment settings."""
    import os

    from web_development_mcp.config import (
        DEFAULT_WEB_DEVELOPMENT_EXECUTABLE,
        WEB_DEVELOPMENT_EXECUTABLE,
    )

    print("Web Development MCP Configuration")
    print("=" * 40)

    print("Web Development Executable:")
    print(f"   Configured: {WEB_DEVELOPMENT_EXECUTABLE}")
    print(f"   Default:    {DEFAULT_WEB_DEVELOPMENT_EXECUTABLE}")
    print(
        f"   From env:   {'WEB_DEVELOPMENT_EXECUTABLE' if os.environ.get('WEB_DEVELOPMENT_EXECUTABLE') else 'auto-detected'}"
    )

    print("\nEnvironment Variables:")
    relevant_env_vars = ["WEB_DEVELOPMENT_EXECUTABLE", "WEB_DEVELOPMENT_PATH", "PYTHONPATH"]
    for var in relevant_env_vars:
        value = os.environ.get(var, "Not set")
        print(f"   {var}: {value}")

    print("\nSystem Information:")
    import platform

    print(f"   Platform: {platform.platform()}")
    print(f"   Python:   {platform.python_version()}")

    print("\nMCP Server Status:")
    try:
        from web_development_mcp.app import get_app

        app = get_app()
        if app:
            print("   Server: Ready")
            print(
                f"   Tools registered: {len(app.list_tools()) if hasattr(app, 'list_tools') else 'Unknown'}"
            )
        else:
            print("   Server: Not initialized")
    except Exception as e:
        print(f"   Server: Error - {e}")


if __name__ == "__main__":
    main()
