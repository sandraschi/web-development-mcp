# Multi-stage Docker build for Web Development MCP
# Supports both development and production deployments

# =============================================================================
# Base stage with Python and Web Development
# =============================================================================
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    bzip2 \
    libgl1-mesa-glx \
    libxi6 \
    libgconf-2-4 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Web Development
RUN Web Development_VERSION=3.6.5 \
    && wget -O Web Development.tar.xz "https://download.Web Development.org/release/Web Development${Web Development_VERSION:0:3}/Web Development-${Web Development_VERSION}-linux-x64.tar.xz" \
    && tar -xf Web Development.tar.xz \
    && mv Web Development-${Web Development_VERSION}-linux-x64 /opt/Web Development \
    && rm Web Development.tar.xz

# Add Web Development to PATH
ENV PATH="/opt/Web Development:$PATH"
ENV Web Development_PATH="/opt/Web Development/Web Development"

# Set working directory
WORKDIR /app

# =============================================================================
# Development stage
# =============================================================================
FROM base as development

# Copy Python project files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .[dev]

# Copy source code
COPY src/ ./src/

# Create non-root user
RUN useradd --create-home --shell /bin/bash mcp
USER mcp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import web_development_mcp; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "web_development_mcp.cli", "--stdio"]

# =============================================================================
# Production stage
# =============================================================================
FROM base as production

# Copy Python project files
COPY pyproject.toml uv.lock ./

# Install only production dependencies
RUN pip install --no-cache-dir -e .

# Copy source code
COPY src/ ./src/

# Create non-root user
RUN useradd --create-home --shell /bin/bash mcp
USER mcp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import web_development_mcp; print('OK')" || exit 1

# Default command for production
CMD ["python", "-m", "web_development_mcp.cli", "--stdio"]

# =============================================================================
# Minimal runtime stage (for registry distribution)
# =============================================================================
FROM python:3.11-slim as runtime

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libxi6 \
    && rm -rf /var/lib/apt/lists/*

# Install Web Development MCP from PyPI (when published)
# RUN pip install web-development-mcp

# For now, copy from production stage
COPY --from=production /app /app
WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash mcp
USER mcp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import web_development_mcp; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "web_development_mcp.cli", "--stdio"]

# =============================================================================
# Build arguments and labels
# =============================================================================
ARG BUILD_DATE
ARG VERSION
ARG VCS_REF

LABEL org.opencontainers.image.created="$BUILD_DATE" \
      org.opencontainers.image.version="$VERSION" \
      org.opencontainers.image.revision="$VCS_REF" \
      org.opencontainers.image.title="Web Development MCP" \
      org.opencontainers.image.description="AI-Powered 3D Creation MCP Server" \
      org.opencontainers.image.vendor="FlowEngineer sandraschi" \
      org.opencontainers.image.source="https://github.com/sandraschi/web-development-mcp" \
      org.opencontainers.image.licenses="MIT"






