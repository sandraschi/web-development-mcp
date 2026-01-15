# Web Development MCP - Cursor IDE Setup Guide

**Quick setup guide for running Web Development MCP in Cursor IDE.**

## Prerequisites

1. **Python 3.9+** installed and in PATH
2. **Node.js** installed (for web development operations)
3. **Web Development MCP** installed in editable mode

## Installation

**Important:** Cursor uses the system Python, so dependencies must be installed globally or in the Python that Cursor uses.

```powershell
cd d:\Dev\repos\web-development-mcp

# Option 1: Install in system Python (recommended for Cursor)
# Find your system Python path (usually shown in Cursor error logs)
# Example: C:\Users\sandr\AppData\Local\Programs\Python\Python310\python.exe
python -m pip install -r requirements.txt
python -m pip install -e .

# Option 2: Install in virtual environment (if using venv in config)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## Cursor Configuration

Add to your Cursor MCP configuration file:
**Location**: `%APPDATA%\Cursor\User\globalStorage\cursor-storage\mcp_config.json`

```json
{
  "mcpServers": {
    "web-development-mcp": {
      "command": "python",
      "args": [
        "-m",
        "web_development_mcp.__main__"
      ],
      "env": {
        "PYTHONPATH": "D:/Dev/repos/web-development-mcp/src",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Note:** Some JSON linters object to `cwd` parameter. Using `-m` module execution with `PYTHONPATH` avoids this issue.

### Using Virtual Environment

If using a virtual environment:

```json
{
  "mcpServers": {
    "web-development-mcp": {
      "command": "d:\\Dev\\repos\\web-development-mcp\\venv\\Scripts\\python.exe",
      "args": [
        "-m",
        "web_development_mcp.__main__"
      ],
      "env": {
        "PYTHONPATH": "D:/Dev/repos/web-development-mcp/src",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### Alternative: Using main.py with Absolute Path

If you prefer using `main.py` directly (avoids `cwd` which some linters reject):

```json
{
  "mcpServers": {
    "web-development-mcp": {
      "command": "python",
      "args": [
        "D:/Dev/repos/web-development-mcp/main.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

## Verification

1. **Check Python import:**
   ```powershell
   python -c "import sys; sys.path.insert(0, 'src'); from web_development_mcp.mcp_server import mcp; print('SUCCESS')"
   ```

2. **Test MCP server startup:**
   ```powershell
   python main.py
   ```
   Should start without errors and wait for JSON-RPC messages on stdin.

3. **Check Cursor logs:**
   - Location: `%APPDATA%\Cursor\logs\`
   - Look for `web-development-mcp` in log files
   - Check for any import errors or startup failures

## Troubleshooting

### ImportError: No module named 'jinja2' / ModuleNotFoundError: No module named 'semver'

**Solution:**
1. **Critical:** Cursor uses system Python, not your current shell's Python
2. Find system Python path from Cursor error logs (e.g., `C:\Users\sandr\AppData\Local\Programs\Python\Python310\python.exe`)
3. Install dependencies in system Python:
   ```powershell
   C:\Users\sandr\AppData\Local\Programs\Python\Python310\python.exe -m pip install -r requirements.txt
   C:\Users\sandr\AppData\Local\Programs\Python\Python310\python.exe -m pip install -e .
   ```
4. Or install globally: `python -m pip install -r requirements.txt` (if `python` points to system Python)

### ModuleNotFoundError: No module named 'web_development_mcp'

**Solution:**
1. Ensure package is installed in the Python that Cursor uses: `python -m pip install -e .`
2. Set PYTHONPATH in Cursor config: `"PYTHONPATH": "D:/Dev/repos/web-development-mcp/src"`
3. Use absolute path to Python executable in venv if using virtual environment

### Server starts but tools don't appear

**Solution:**
1. Check Cursor logs for JSON-RPC errors
2. Verify FastMCP version: `pip show fastmcp` (should be >=2.13.0)
3. Restart Cursor after configuration changes

## Available Tools

Web Development MCP provides tools for:
- **Project Scaffolding**: React, Vue, SvelteKit, Next.js, Vanilla TypeScript
- **Package Management**: npm, yarn, pnpm operations
- **Build Tools**: Vite, TypeScript, ESLint configuration
- **Component Generation**: React/Vue components with TypeScript
- **Dashboard Scaffolding**: Tailwind CSS + shadcn/ui dashboards

## Reference

- **Generalized Setup Guide**: `mcp-central-docs/docs/patterns/WEBAPP_SETUP_GUIDE.md`
- **Cursor Standards**: `mcp-central-docs/docs/ecosystem/cursor/README.md`
- **MCP Standards**: `mcp-central-docs/STANDARDS.md`
