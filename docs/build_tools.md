# Build Tools Documentation

This document provides an overview of the build tools available in the Windsurf MCP server for managing web development projects.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
  - [Initialization](#initialization)
  - [Installing Dependencies](#installing-dependencies)
  - [Building the Project](#building-the-project)
  - [Starting a Development Server](#starting-a-development-server)
  - [Running Tests](#running-tests)
  - [Linting Code](#linting-code)
  - [Formatting Code](#formatting-code)
  - [Analyzing Bundle](#analyzing-bundle)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

The BuildTools class provides a comprehensive set of methods for managing the build and development workflow of web projects. It supports various build tools and frameworks, including Vite, Webpack, ESLint, Prettier, and testing frameworks like Jest and Vitest.

## Installation

The build tools are included in the Windsurf MCP server. No additional installation is required.

## Usage

### Initialization

```python
from web_development_mcp.tools.build_tools import BuildTools

# Initialize with the project path
build_tools = BuildTools("/path/to/your/project")
```

### Installing Dependencies

```python
# Install dependencies (auto-detects package manager)
result = build_tools.install_dependencies()

# Or specify a package manager
result = build_tools.install_dependencies(package_manager="yarn")

if result["success"]:
    print("Dependencies installed successfully!")
else:
    print(f"Error: {result.get('error')}")
```

### Building the Project

```python
# Build for production (default)
result = build_tools.build_project()

# Build for development
result = build_tools.build_project(mode="development")

if result["success"]:
    print(f"Build completed successfully in {result['mode']} mode")
    print(f"Output directory: {result['build_dir']}")
```

### Starting a Development Server

```python
# Start the development server
result = build_tools.start_development_server(
    port=3000,
    host="localhost",
    https=False,
    open_browser=True
)

if result["success"]:
    print(f"Development server started at {result['url']}")
    print(f"Process ID: {result['process_id']}")
```

### Running Tests

```python
# Run tests
result = build_tools.run_tests()

# Run tests with coverage
result = build_tools.run_tests(coverage=True)

# Run tests in watch mode
result = build_tools.run_tests(watch=True)

if result["success"]:
    print(f"Tests passed: {result['test_results']['passed']}/{result['test_results']['total']}")
    if result['test_results']['coverage']:
        print(f"Coverage: {result['test_results']['coverage']['statements']}% statements")
```

### Linting Code

```python
# Lint code
result = build_tools.lint_code()

# Fix linting issues automatically
result = build_tools.lint_code(fix=True)

if result["issues_found"] > 0:
    print(f"Found {result['errors']} errors and {result['warnings']} warnings")
    for issue in result["issues"]:
        print(f"{issue['file']}:{issue.get('line', '?')} - {issue['message']}")
```

### Formatting Code

```python
# Format code
result = build_tools.format_code()

# Check formatting without making changes
result = build_tools.format_code(check=True)

if result["success"]:
    if result["check_only"]:
        print("Code is properly formatted!")
    else:
        print(f"Formatted {len(result['formatted_files'])} files")
```

### Analyzing Bundle

```python
# Analyze bundle size
result = build_tools.analyze_bundle()

# Save analysis to an HTML file
result = build_tools.analyze_bundle(output_file="bundle-analysis.html")

if result["success"]:
    print(f"Bundle analysis complete: {result['report_path']}")
```

## API Reference

### BuildTools Class

#### `__init__(project_path: Union[str, Path])`
Initialize the BuildTools with the project path.

#### `install_dependencies(package_manager: Optional[str] = None) -> Dict[str, Any]`
Install project dependencies.

#### `build_project(mode: str = "production") -> Dict[str, Any]`
Build the project for production or development.

#### `start_development_server(port: Optional[int] = None, host: str = "localhost", https: bool = False, open_browser: bool = True) -> Dict[str, Any]`
Start a development server.

#### `run_tests(watch: bool = False, coverage: bool = False, update_snapshots: bool = False) -> Dict[str, Any]`
Run tests in the project.

#### `lint_code(fix: bool = False) -> Dict[str, Any]`
Lint the project code.

#### `format_code(check: bool = False) -> Dict[str, Any]`
Format code using Prettier.

#### `analyze_bundle(output_file: Optional[str] = None) -> Dict[str, Any]`
Analyze bundle size and dependencies.

## Examples

### Complete Workflow Example

```python
from pathlib import Path
from web_development_mcp.tools.build_tools import BuildTools

def main():
    # Initialize with project path
    project_path = Path("/path/to/your/project")
    tools = BuildTools(project_path)
    
    # Install dependencies
    print("Installing dependencies...")
    result = tools.install_dependencies()
    if not result["success"]:
        print(f"Failed to install dependencies: {result.get('error')}")
        return
    
    # Lint code
    print("\nLinting code...")
    result = tools.lint_code(fix=True)
    if result["issues_found"] > 0:
        print(f"Fixed {result['issues_found']} issues")
    
    # Run tests
    print("\nRunning tests...")
    result = tools.run_tests(coverage=True)
    if not result["success"]:
        print(f"Tests failed: {result.get('error')}")
        return
    
    # Build for production
    print("\nBuilding for production...")
    result = tools.build_project(mode="production")
    if not result["success"]:
        print(f"Build failed: {result.get('error')}")
        return
    
    # Analyze bundle
    print("\nAnalyzing bundle...")
    result = tools.analyze_bundle(output_file="bundle-analysis.html")
    if result["success"]:
        print(f"Bundle analysis saved to {result['report_path']}")
    
    print("\nBuild process completed successfully!")

if __name__ == "__main__":
    main()
```

## Troubleshooting

### Common Issues

1. **Missing package.json**
   - Ensure your project has a valid `package.json` file in the root directory.

2. **Missing build script**
   - Add a `build` script to your `package.json` or specify a custom build command.

3. **ESLint/Prettier not found**
   - Install the required dev dependencies:
     ```bash
     npm install --save-dev eslint prettier
     ```

4. **Port already in use**
   - Specify a different port when starting the development server.

5. **Permission denied**
   - Ensure you have the necessary permissions to write to the project directory.

### Debugging

To enable debug logging, set the `LOG_LEVEL` environment variable to `DEBUG`:

```bash
export LOG_LEVEL=DEBUG
```

### Getting Help

For additional help, please open an issue on the [GitHub repository](https://github.com/your-org/your-repo/issues).
