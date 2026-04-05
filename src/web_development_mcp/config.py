"""Configuration for Web Development MCP."""

import os
import shutil

# Executable settings
WEB_DEVELOPMENT_EXECUTABLE = os.environ.get("WEB_DEVELOPMENT_EXECUTABLE")
DEFAULT_WEB_DEVELOPMENT_EXECUTABLE = shutil.which("web-development") or "web-development"

if not WEB_DEVELOPMENT_EXECUTABLE:
    WEB_DEVELOPMENT_EXECUTABLE = DEFAULT_WEB_DEVELOPMENT_EXECUTABLE
