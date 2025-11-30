"""
Build configuration and development tools.

Handles Vite, TypeScript, ESLint, and other build tool configurations.
"""

import logging
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)

class BuildTools:
    """A collection of build and development tools for web projects."""
    
    def __init__(self, project_path: Union[str, Path]):
        """Initialize BuildTools with the project path.
        
        Args:
            project_path: Path to the project directory
        """
        self.project_path = Path(project_path).resolve()
        self.package_json = self.project_path / "package.json"
        self.node_modules = self.project_path / "node_modules"
        self.dist_dir = self.project_path / "dist"
        
        # Cache for package.json data
        self._package_data = None
    
    @property
    def package_data(self) -> Dict[str, Any]:
        """Lazily load and cache package.json data."""
        if self._package_data is None and self.package_json.exists():
            with open(self.package_json, 'r', encoding='utf-8') as f:
                self._package_data = json.load(f)
        return self._package_data or {}
    
    def _run_command(
        self,
        command: List[str],
        cwd: Optional[Path] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: int = 300,
        capture_output: bool = True
    ) -> Dict[str, Any]:
        """Run a shell command and return the result.
        
        Args:
            command: The command to run as a list of strings
            cwd: Working directory (defaults to project path)
            env: Environment variables to use
            timeout: Command timeout in seconds
            capture_output: Whether to capture stdout/stderr
            
        Returns:
            Dictionary with command results
        """
        cwd = cwd or self.project_path
        env = env or os.environ.copy()
        
        try:
            result = subprocess.run(
                command,
                cwd=str(cwd),
                env=env,
                capture_output=capture_output,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout if capture_output else "",
                "stderr": result.stderr if capture_output else "",
                "command": " ".join(command)
            }
            
        except subprocess.TimeoutExpired as e:
            return {
                "success": False,
                "error": f"Command timed out after {timeout} seconds",
                "command": " ".join(command)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": " ".join(command)
            }
    
    def install_dependencies(self, package_manager: Optional[str] = None) -> Dict[str, Any]:
        """Install project dependencies using the specified package manager.
        
        Args:
            package_manager: Package manager to use (npm, yarn, pnpm) - auto-detect if None
            
        Returns:
            Dictionary with installation results
        """
        if not package_manager:
            # Auto-detect package manager
            if (self.project_path / "yarn.lock").exists():
                package_manager = "yarn"
            elif (self.project_path / "pnpm-lock.yaml").exists():
                package_manager = "pnpm"
            else:
                package_manager = "npm"
        
        if package_manager == "yarn":
            cmd = ["yarn", "install", "--frozen-lockfile"]
        elif package_manager == "pnpm":
            cmd = ["pnpm", "install", "--frozen-lockfile"]
        else:  # npm
            cmd = ["npm", "ci"] if (self.project_path / "package-lock.json").exists() else ["npm", "install"]
        
        return self._run_command(cmd, timeout=600)  # 10 minute timeout
    
    def build_project(self, mode: str = "production") -> Dict[str, Any]:
        """Build the project for production or development.
        
        Args:
            mode: Build mode (production, development, etc.)
            
        Returns:
            Dictionary with build results
        """
        scripts = self.package_data.get("scripts", {})
        
        # Try to determine the build command
        build_script = None
        if "build:{mode}" in scripts:
            build_script = f"build:{mode}"
        elif "build" in scripts:
            build_script = "build"
        elif "vite" in self.package_data.get("devDependencies", {}):
            build_script = "vite build"
        elif "webpack" in self.package_data.get("devDependencies", {}):
            build_script = "webpack --mode {mode}"
        else:
            return {
                "success": False,
                "error": "No build script found in package.json and no build tool detected"
            }
        
        # Prepare environment
        env = os.environ.copy()
        env["NODE_ENV"] = mode
        
        # Run the build command
        if " " in build_script:
            # Handle commands with arguments (e.g., "vite build")
            cmd = ["npx"] + build_script.split()
        else:
            cmd = ["npm", "run", build_script]
        
        if mode != "production" and "vite" in build_script:
            cmd.append(f"--mode {mode}")
        
        result = self._run_command(cmd, env=env, timeout=600)  # 10 minute timeout
        
        # Check if build was successful and output directory exists
        if result["success"] and not self.dist_dir.exists():
            return {
                "success": False,
                "error": "Build completed but output directory not found",
                "output": result["stdout"],
                "command": " ".join(cmd)
            }
        
        # Add build info to the result
        result["build_dir"] = str(self.dist_dir) if self.dist_dir.exists() else None
        result["mode"] = mode
        
        return result
    
    def start_development_server(
        self,
        port: Optional[int] = None,
        host: str = "localhost",
        https: bool = False,
        open_browser: bool = True
    ) -> Dict[str, Any]:
        """Start a development server for the project.
        
        Args:
            port: Port to run the dev server on (auto-select if None)
            host: Host to bind the dev server to
            https: Enable HTTPS for the dev server
            open_browser: Open the browser automatically
            
        Returns:
            Dictionary with server information
        """
        scripts = self.package_data.get("scripts", {})
        
        # Determine the dev command
        dev_script = None
        if "dev" in scripts:
            dev_script = "dev"
        elif "start" in scripts:
            dev_script = "start"
        elif "vite" in self.package_data.get("devDependencies", {}):
            dev_script = "vite"
        elif "webpack" in self.package_data.get("devDependencies", {}):
            dev_script = "webpack serve --mode development"
        else:
            return {
                "success": False,
                "error": "No development server script found in package.json"
            }
        
        # Prepare the command
        if " " in dev_script:
            cmd = ["npx"] + dev_script.split()
        else:
            cmd = ["npm", "run", dev_script]
        
        # Add additional options
        if port:
            if "vite" in dev_script or "webpack" in dev_script:
                cmd.extend(["--port", str(port)])
        
        if host != "localhost":
            if "vite" in dev_script or "webpack" in dev_script:
                cmd.extend(["--host", host])
        
        if https:
            if "vite" in dev_script or "webpack" in dev_script:
                cmd.append("--https")
        
        if open_browser:
            if "vite" in dev_script or "webpack" in dev_script:
                cmd.append("--open")
        
        # Start the development server in a separate process
        try:
            process = subprocess.Popen(
                cmd,
                cwd=str(self.project_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Get the actual port being used (if auto-selected)
            actual_port = port
            if not port:
                # Try to extract port from the output (this is a bit fragile)
                for _ in range(10):  # Wait up to 10 seconds for the port to be printed
                    line = process.stdout.readline()
                    if not line:
                        time.sleep(1)
                        continue
                    
                    # Try to find port in the output
                    port_match = re.search(r'(?::|port:|https?://[^:]+:)(\d+)', line)
                    if port_match:
                        actual_port = int(port_match.group(1))
                        break
            
            return {
                "success": True,
                "process_id": process.pid,
                "host": host,
                "port": actual_port,
                "https": https,
                "url": f"{'https' if https else 'http'}://{host}:{actual_port}" if actual_port else None,
                "command": " ".join(cmd)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": " ".join(cmd)
            }
    
    def run_tests(
        self,
        watch: bool = False,
        coverage: bool = False,
        update_snapshots: bool = False
    ) -> Dict[str, Any]:
        """Run tests in the project.
        
        Args:
            watch: Run tests in watch mode
            coverage: Generate code coverage report
            update_snapshots: Update test snapshots
            
        Returns:
            Dictionary with test results
        """
        scripts = self.package_data.get("scripts", {})
        
        # Determine the test command
        test_script = None
        if "test" in scripts:
            test_script = "test"
        elif "vitest" in self.package_data.get("devDependencies", {}):
            test_script = "vitest"
        elif "jest" in self.package_data.get("devDependencies", {}):
            test_script = "jest"
        else:
            return {
                "success": False,
                "error": "No test script found in package.json and no test runner detected"
            }
        
        # Prepare the command
        if " " in test_script:
            cmd = ["npx"] + test_script.split()
        else:
            cmd = ["npm", "test"]
        
        # Add additional options
        if watch:
            cmd.append("--watch")
        
        if coverage:
            cmd.append("--coverage")
        
        if update_snapshots:
            if "vitest" in test_script or "jest" in test_script:
                cmd.append("-u")
        
        # Run tests
        result = self._run_command(cmd, timeout=600)  # 10 minute timeout
        
        # Parse test results
        test_results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "total": 0,
            "coverage": None
        }
        
        # Try to extract test results from the output
        if result.get("stdout"):
            # Look for test summary in the output
            test_summary = re.search(
                r'Tests?:\s+(\d+) failed(?:, (\d+) passed)?(?:, (\d+) skipped)?(?:, (\d+) total)?',
                result["stdout"]
            )
            
            if test_summary:
                test_results["failed"] = int(test_summary.group(1) or 0)
                test_results["passed"] = int(test_summary.group(2) or 0)
                test_results["skipped"] = int(test_summary.group(3) or 0)
                test_results["total"] = int(test_summary.group(4) or 0)
            
            # Look for coverage information
            coverage_match = re.search(
                r'All files\s+\|\s+([\d.]+)\s+\|\s+([\d.]+)',
                result["stdout"]
            )
            
            if coverage_match:
                test_results["coverage"] = {
                    "statements": float(coverage_match.group(1)),
                    "branches": float(coverage_match.group(2))
                }
        
        result["test_results"] = test_results
        return result
    
    def lint_code(self, fix: bool = False) -> Dict[str, Any]:
        """Lint the project code.
        
        Args:
            fix: Automatically fix fixable issues
            
        Returns:
            Dictionary with linting results
        """
        # Check for ESLint configuration
        eslint_configs = list(self.project_path.glob("{.eslintrc*,.eslintrc/**/*}"))
        if not eslint_configs:
            return {
                "success": False,
                "error": "No ESLint configuration found in the project"
            }
        
        # Prepare ESLint command
        cmd = ["npx", "eslint", ".", "--ext", ".js,.jsx,.ts,.tsx"]
        
        if fix:
            cmd.append("--fix")
        
        # Run ESLint
        result = self._run_command(cmd, timeout=300)  # 5 minute timeout
        
        # Parse ESLint output
        issues = []
        if result.get("stdout"):
            for line in result["stdout"].split('\n'):
                if line.strip() and ':' in line:
                    parts = line.split(':', 3)
                    if len(parts) >= 4:
                        file_path = parts[0].strip()
                        line_num = parts[1].strip()
                        col_num = parts[2].split()[0].strip()
                        message = parts[3].strip()
                        
                        # Determine if it's a warning or error
                        is_error = 'error' in line.lower()
                        
                        issues.append({
                            'file': file_path,
                            'line': int(line_num) if line_num.isdigit() else None,
                            'column': int(col_num) if col_num.isdigit() else None,
                            'message': message,
                            'severity': 'error' if is_error else 'warning'
                        })
        
        result["issues"] = issues
        result["issues_found"] = len(issues)
        result["errors"] = len([i for i in issues if i['severity'] == 'error'])
        result["warnings"] = len([i for i in issues if i['severity'] == 'warning'])
        
        return result
    
    def format_code(self, check: bool = False) -> Dict[str, Any]:
        """Format code using Prettier.
        
        Args:
            check: Check formatting without making changes
            
        Returns:
            Dictionary with formatting results
        """
        # Check for Prettier configuration
        prettier_configs = list(self.project_path.glob("{.prettierrc*,.prettierrc/**/*,.prettier.config.*}"))
        if not prettier_configs:
            return {
                "success": False,
                "error": "No Prettier configuration found in the project"
            }
        
        # Prepare Prettier command
        cmd = ["npx", "prettier"]
        
        if check:
            cmd.append("--check")
        else:
            cmd.append("--write")
        
        cmd.extend([
            ".",
            "--ignore-path",
            ".gitignore"
        ])
        
        # Run Prettier
        result = self._run_command(cmd, timeout=300)  # 5 minute timeout
        
        # Parse Prettier output
        formatted_files = []
        if result.get("stdout"):
            for line in result["stdout"].split('\n'):
                if line.strip() and ('code' in line.lower() or 'wrote' in line.lower() or 'unchanged' in line.lower()):
                    formatted_files.append(line.strip())
        
        result["formatted_files"] = formatted_files
        result["check_only"] = check
        
        return result
    
    def analyze_bundle(self, output_file: Optional[str] = None) -> Dict[str, Any]:
        """Analyze bundle size and dependencies.
        
        Args:
            output_file: Path to save the analysis report (HTML format)
            
        Returns:
            Dictionary with analysis results
        """
        # Check for build output directory
        if not self.dist_dir.exists():
            return {
                "success": False,
                "error": "No 'dist' directory found. Build the project first."
            }
        
        # Use source-map-explorer or webpack-bundle-analyzer
        if "webpack" in self.package_data.get("devDependencies", {}):
            # Generate stats file first
            stats_file = self.dist_dir / "stats.json"
            webpack_cmd = ["npx", "webpack", "--profile", "--json=dist/stats.json"]
            
            result = self._run_command(webpack_cmd)
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": f"Failed to generate webpack stats: {result.get('stderr')}"
                }
            
            # Run webpack-bundle-analyzer
            analyzer_cmd = ["npx", "webpack-bundle-analyzer", str(stats_file)]
            
            # If output file is specified, generate HTML report
            if output_file:
                output_path = self.project_path / output_file
                analyzer_cmd.extend(["--mode", "static", "--report", str(output_path)])
            
            result = self._run_command(analyzer_cmd)
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": f"Failed to analyze bundle: {result.get('stderr')}"
                }
            
            return {
                "success": True,
                "analysis_type": "webpack-bundle-analyzer",
                "report_path": str(output_path) if output_file else None,
                "output": result.get("stdout", "")
            }
        
        # Fall back to source-map-explorer
        else:
            # Find the main bundle file
            bundle_files = list(self.dist_dir.glob("*.js"))
            if not bundle_files:
                return {
                    "success": False,
                    "error": "No JavaScript bundle files found in the dist directory"
                }
            
            # Use the largest JS file as the main bundle
            main_bundle = max(bundle_files, key=lambda f: f.stat().st_size)
            
            # Generate analysis
            if output_file:
                output_path = self.project_path / output_file
                cmd = ["npx", "source-map-explorer", str(main_bundle), "--html", str(output_path)]
            else:
                cmd = ["npx", "source-map-explorer", str(main_bundle)]
            
            result = self._run_command(cmd)
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": f"Failed to analyze bundle: {result.get('stderr')}"
                }
            
            return {
                "success": True,
                "analysis_type": "source-map-explorer",
                "bundle_file": str(main_bundle),
                "report_path": str(output_path) if output_file else None,
                "output": result.get("stdout", "")
            }

def register_tools(mcp):
    """Register build tools with the MCP server."""
    
    @mcp.tool()
    def build_project_tool(
        project_path: str,
        mode: str = "production"
    ) -> Dict[str, Any]:
        """Build the project for production or development.
        
        Args:
            project_path: Path to the project directory
            mode: Build mode (production, development, etc.)
            
        Returns:
            Dictionary with build results
        """
        tools = BuildTools(project_path)
        return tools.build_project(mode)
    
    @mcp.tool()
    def start_dev_server_tool(
        project_path: str,
        port: Optional[int] = None,
        host: str = "localhost",
        https: bool = False,
        open_browser: bool = True
    ) -> Dict[str, Any]:
        """Start a development server for the project.
        
        Args:
            project_path: Path to the project directory
            port: Port to run the dev server on (auto-select if None)
            host: Host to bind the dev server to
            https: Enable HTTPS for the dev server
            open_browser: Open the browser automatically
            
        Returns:
            Dictionary with server information
        """
        tools = BuildTools(project_path)
        return tools.start_development_server(port, host, https, open_browser)
    
    @mcp.tool()
    def run_tests_tool(
        project_path: str,
        watch: bool = False,
        coverage: bool = False,
        update_snapshots: bool = False
    ) -> Dict[str, Any]:
        """Run tests in the project.
        
        Args:
            project_path: Path to the project directory
            watch: Run tests in watch mode
            coverage: Generate code coverage report
            update_snapshots: Update test snapshots
            
        Returns:
            Dictionary with test results
        """
        tools = BuildTools(project_path)
        return tools.run_tests(watch, coverage, update_snapshots)
    
    @mcp.tool()
    def lint_code_tool(
        project_path: str,
        fix: bool = False
    ) -> Dict[str, Any]:
        """Lint the project code.
        
        Args:
            project_path: Path to the project directory
            fix: Automatically fix fixable issues
            
        Returns:
            Dictionary with linting results
        """
        tools = BuildTools(project_path)
        return tools.lint_code(fix)
    
    @mcp.tool()
    def format_code_tool(
        project_path: str,
        check: bool = False
    ) -> Dict[str, Any]:
        """Format code using Prettier.
        
        Args:
            project_path: Path to the project directory
            check: Check formatting without making changes
            
        Returns:
            Dictionary with formatting results
        """
        tools = BuildTools(project_path)
        return tools.format_code(check)
    
    @mcp.tool()
    def analyze_bundle_tool(
        project_path: str,
        output_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze bundle size and dependencies.
        
        Args:
            project_path: Path to the project directory
            output_file: Path to save the analysis report (HTML format)
            
        Returns:
            Dictionary with analysis results
        """
        tools = BuildTools(project_path)
        return tools.analyze_bundle(output_file)
    
    @mcp.tool()
    def install_dependencies_tool(
        project_path: str,
        package_manager: Optional[str] = None
    ) -> Dict[str, Any]:
        """Install project dependencies.
        
        Args:
            project_path: Path to the project directory
            package_manager: Package manager to use (npm, yarn, pnpm) - auto-detect if None
            
        Returns:
            Dictionary with installation results
        """
        tools = BuildTools(project_path)
        return tools.install_dependencies(package_manager)
