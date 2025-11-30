"""
Project scaffolding and framework setup tools.

Handles creation of new projects with modern frameworks and best practices.
"""

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, Optional

from ..utils.file_operations import (
    write_file
)

from ..utils.template_engine import process_template_file

logger = logging.getLogger(__name__)

def register_tools(mcp):
    """Register scaffolding tools with the MCP server."""
    
    @mcp.tool()
    def list_available_frameworks() -> Dict[str, Any]:
        """List all supported frontend frameworks and their features.
        
        Returns comprehensive information about supported frameworks.
        """
        frameworks = {
            "react": {
                "name": "React",
                "description": "Popular component-based UI library",
                "features": ["TypeScript", "Vite", "React Router", "Testing Library", "ESLint"],
                "use_cases": ["SPAs", "Component libraries", "Complex UIs"],
                "popularity": "Most popular",
                "learning_curve": "Moderate"
            },
            "vue": {
                "name": "Vue 3",
                "description": "Progressive JavaScript framework",
                "features": ["TypeScript", "Vite", "Vue Router", "Pinia", "ESLint"],
                "use_cases": ["SPAs", "Progressive web apps", "Quick prototypes"],
                "popularity": "Very popular",
                "learning_curve": "Easy"
            },
            "svelte": {
                "name": "SvelteKit",
                "description": "Compile-time optimized framework",
                "features": ["TypeScript", "Vite", "SvelteKit routing", "Built-in state", "ESLint"],
                "use_cases": ["Performance-critical apps", "Small bundles", "SSR"],
                "popularity": "Growing fast",
                "learning_curve": "Easy"
            },
            "next": {
                "name": "Next.js",
                "description": "Full-stack React framework",
                "features": ["TypeScript", "App Router", "Server components", "API routes", "ESLint"],
                "use_cases": ["Full-stack apps", "SSR/SSG", "E-commerce"],
                "popularity": "Very popular",
                "learning_curve": "Moderate"
            },
            "vanilla": {
                "name": "Vanilla TypeScript",
                "description": "Modern TypeScript with Vite",
                "features": ["TypeScript", "Vite", "ESM", "Hot reload", "ESLint"],
                "use_cases": ["Libraries", "Learning", "Custom solutions"],
                "popularity": "Foundation",
                "learning_curve": "Requires JS knowledge"
            }
        }
        
        return {
            "success": True,
            "frameworks": frameworks,
            "total_frameworks": len(frameworks),
            "recommended_for_beginners": ["vue", "svelte"],
            "most_popular": ["react", "next"],
            "best_performance": ["svelte", "vanilla"]
        }
    
    @mcp.tool()
    def create_react_app(
        project_name: str,
        target_directory: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new React application with TypeScript and modern tooling.
        
        Args:
            project_name: Name of the project (will be used for package.json name)
            target_directory: Directory where project will be created
            options: Optional customization options
                - router: Include React Router (default: true)
                - testing: Include testing setup (default: true)
                - eslint_strict: Use strict ESLint rules (default: true)
                - prettier: Include Prettier configuration (default: true)
                - husky: Include git hooks (default: false)
        """
        try:
            # Default options
            opts = {
                "router": True,
                "testing": True,
                "eslint_strict": True,
                "prettier": True,
                "husky": False,
                **(options or {})
            }
            
            # Validate project name
            if not _is_valid_project_name(project_name):
                return {
                    "success": False,
                    "error": "Invalid project name. Use lowercase letters, numbers, and hyphens only."
                }
            
            # Create project directory
            project_path = Path(target_directory) / project_name
            if project_path.exists():
                return {
                    "success": False,
                    "error": f"Directory {project_path} already exists"
                }
            
            project_path.mkdir(parents=True, exist_ok=False)
            
            # Create package.json
            package_json = _create_react_package_json(project_name, opts)
            _write_json_file(project_path / "package.json", package_json)
            
            # Create project structure
            _create_react_project_structure(project_path, opts)
            
            # Create configuration files
            _create_react_config_files(project_path, opts)
            
            # Create initial React components
            _create_react_components(project_path, opts)
            
            return {
                "success": True,
                "project_name": project_name,
                "project_path": str(project_path),
                "framework": "react",
                "features_included": [
                    "TypeScript",
                    "Vite",
                    "ESLint" + (" (strict)" if opts["eslint_strict"] else ""),
                    "Prettier" if opts["prettier"] else None,
                    "React Router" if opts["router"] else None,
                    "Testing Library" if opts["testing"] else None,
                    "Husky git hooks" if opts["husky"] else None
                ],
                "next_steps": [
                    f"cd {project_path}",
                    "npm install",
                    "npm run dev"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error creating React app: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    @mcp.tool()
    def create_vue_app(
        project_name: str,
        target_directory: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new Vue 3 application with TypeScript and modern tooling.
        
        Args:
            project_name: Name of the project
            target_directory: Directory where project will be created  
            options: Optional customization options
                - router: Include Vue Router (default: true)
                - pinia: Include Pinia state management (default: true)
                - testing: Include testing setup (default: true)
                - eslint_strict: Use strict ESLint rules (default: true)
        """
        try:
            opts = {
                "router": True,
                "pinia": True,
                "testing": True,
                "eslint_strict": True,
                **(options or {})
            }
            
            if not _is_valid_project_name(project_name):
                return {
                    "success": False,
                    "error": "Invalid project name. Use lowercase letters, numbers, and hyphens only."
                }
            
            project_path = Path(target_directory) / project_name
            if project_path.exists():
                return {
                    "success": False,
                    "error": f"Directory {project_path} already exists"
                }
            
            project_path.mkdir(parents=True, exist_ok=False)
            
            # Create Vue project files
            package_json = _create_vue_package_json(project_name, opts)
            _write_json_file(project_path / "package.json", package_json)
            
            _create_vue_project_structure(project_path, opts)
            _create_vue_config_files(project_path, opts)
            _create_vue_components(project_path, opts)
            
            return {
                "success": True,
                "project_name": project_name,
                "project_path": str(project_path),
                "framework": "vue",
                "features_included": [
                    "Vue 3",
                    "TypeScript", 
                    "Vite",
                    "ESLint",
                    "Vue Router" if opts["router"] else None,
                    "Pinia" if opts["pinia"] else None,
                    "Vitest" if opts["testing"] else None
                ],
                "next_steps": [
                    f"cd {project_path}",
                    "npm install", 
                    "npm run dev"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error creating Vue app: {e}")
            return {
                "success": False,
                "error": str(e)
            }

def _is_valid_project_name(name: str) -> bool:
    """Validate project name follows npm naming conventions."""
    # npm package name rules
    pattern = r'^[a-z0-9]([a-z0-9\-])*[a-z0-9]$|^[a-z0-9]$'
    return bool(re.match(pattern, name)) and len(name) <= 214

def _write_json_file(path: Path, data: dict) -> None:
    """Write JSON data to file with proper formatting."""
    import json
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def _create_react_package_json(project_name: str, options: dict) -> dict:
    """Create package.json for React project."""
    dependencies = {
        "react": "^18.2.0",
        "react-dom": "^18.2.0"
    }
    
    dev_dependencies = {
        "@types/react": "^18.2.0",
        "@types/react-dom": "^18.2.0",
        "@vitejs/plugin-react": "^4.2.0",
        "typescript": "^5.3.0",
        "vite": "^5.0.0"
    }
    
    if options.get("router"):
        dependencies["react-router-dom"] = "^6.20.0"
        dev_dependencies["@types/react-router-dom"] = "^5.3.0"
    
    if options.get("testing"):
        dev_dependencies.update({
            "@testing-library/react": "^14.1.0",
            "@testing-library/jest-dom": "^6.1.0",
            "@testing-library/user-event": "^14.5.0",
            "vitest": "^1.0.0",
            "jsdom": "^23.0.0"
        })
    
    if options.get("eslint_strict"):
        dev_dependencies.update({
            "eslint": "^8.55.0",
            "@typescript-eslint/eslint-plugin": "^6.14.0",
            "@typescript-eslint/parser": "^6.14.0",
            "eslint-plugin-react": "^7.33.0",
            "eslint-plugin-react-hooks": "^4.6.0",
            "eslint-plugin-react-refresh": "^0.4.5"
        })
    
    if options.get("prettier"):
        dev_dependencies.update({
            "prettier": "^3.1.0",
            "eslint-config-prettier": "^9.1.0"
        })
    
    scripts = {
        "dev": "vite",
        "build": "tsc && vite build",
        "preview": "vite preview",
        "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
    }
    
    if options.get("testing"):
        scripts.update({
            "test": "vitest",
            "test:ui": "vitest --ui"
        })
    
    return {
        "name": project_name,
        "private": True,
        "version": "0.0.0",
        "type": "module",
        "scripts": scripts,
        "dependencies": dependencies,
        "devDependencies": dev_dependencies
    }

def _create_react_project_structure(project_path: Path, options: dict) -> None:
    """Create React project directory structure."""
    # Create directories
    directories = [
        "src",
        "src/components",
        "src/hooks", 
        "src/utils",
        "src/types",
        "public"
    ]
    
    if options.get("testing"):
        directories.extend(["src/__tests__", "src/components/__tests__"])
    
    for dir_name in directories:
        (project_path / dir_name).mkdir(parents=True, exist_ok=True)

def _create_react_config_files(project_path: Path, options: dict) -> None:
    """
    Create configuration files for React project.
    
    Args:
        project_path: Path to the project directory
        options: Project options including framework and tooling choices
    """
    # Get template directory path
    template_dir = Path(__file__).parent.parent / 'templates' / 'react'
    
    # Define config files to process
    config_files = [
        'vite.config.ts.template',
        'tsconfig.json.template',
        '.eslintrc.json.template',
        '.prettierrc.template',
        '.gitignore.template',
        'index.html.template'
    ]
    
    # Process each config file
    for template_file in config_files:
        src_path = template_dir / template_file
        dest_file = template_file.replace('.template', '')
        dest_path = project_path / dest_file
        
        # Skip if source template doesn't exist
        if not src_path.exists():
            logger.warning(f"Template file not found: {src_path}")
            continue
            
        # Process template and write to destination
        try:
            # For JSON files, we'll parse and validate them
            if dest_file.endswith('.json'):
                content = process_template_file(src_path, options)
                try:
                    # Validate JSON by parsing it
                    json.loads(content)
                    write_file(dest_path, content)
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON in template {src_path}: {e}")
                    # Write the file anyway for debugging, but log the error
                    write_file(dest_path, content)
            else:
                # For non-JSON files, just process and write directly
                content = process_template_file(src_path, options)
                write_file(dest_path, content)
                
            logger.debug(f"Created config file: {dest_path}")
            
        except Exception as e:
            logger.error(f"Failed to process template {src_path}: {e}")
            raise
    
    # Create src directory if it doesn't exist
    src_dir = project_path / 'src'
    src_dir.mkdir(exist_ok=True)
    
    # Process and copy App.tsx and main.tsx to src directory
    for component in ['App.tsx.template', 'main.tsx.template', 'App.css.template']:
        src_path = template_dir / 'src' / component
        dest_file = component.replace('.template', '')
        dest_path = src_dir / dest_file
        
        if src_path.exists():
            try:
                content = process_template_file(src_path, options)
                write_file(dest_path, content)
                logger.debug(f"Created component file: {dest_path}")
            except Exception as e:
                logger.error(f"Failed to create component {dest_path}: {e}")
                raise

def _create_react_components(project_path: Path, options: dict) -> None:
    """
    Create initial React components.
    
    Args:
        project_path: Path to the project directory
        options: Project options including framework and tooling choices
    """
    logger.info("Creating React components...")
    
    # Define source directory
    src_dir = project_path / 'src'
    
    # Template context with additional options
    context = {
        'project_name': project_path.name,
        'router': options.get('router', False),
        'with_tailwind': options.get('tailwind', False),
        'with_eslint': options.get('eslint', True),
        'with_prettier': options.get('prettier', True),
        'with_testing': options.get('testing', False),
        'with_vitest': options.get('testing') == 'vitest',
        'with_rtl': options.get('rtl', False),
        'with_gh_pages': options.get('gh_pages', False),
        'with_husky': options.get('husky', False)
    }
    
    # Get the directory where templates are stored
    templates_dir = Path(__file__).parent.parent / 'templates' / 'react' / 'src'
    src_dir = project_path / 'src'
    
    # Ensure source directory exists
    src_dir.mkdir(exist_ok=True)
    
    # List of template files to process with their destinations
    template_files = [
        ('App.tsx.template', 'App.tsx'),
        ('App.css.template', 'App.css'),
        ('main.tsx.template', 'main.tsx'),
        ('vite-env.d.ts.template', 'vite-env.d.ts')
    ]
    
    # Process each template file
    for template_file, output_file in template_files:
        template_path = templates_dir / template_file
        output_path = src_dir / output_file
        
        if not template_path.exists():
            logger.warning(f"Template file not found: {template_path}")
            continue
            
        try:
            process_template_file(
                str(template_path),
                context,
                str(output_path)
            )
            logger.debug(f"Created component: {output_path}")
        except Exception as e:
            logger.error(f"Failed to create component {output_file}: {e}")
            raise
    
    # Create assets directory and copy favicon
    assets_dir = src_dir / 'assets'
    assets_dir.mkdir(exist_ok=True)
    
    # Create components directory
    components_dir = src_dir / 'components'
    components_dir.mkdir(exist_ok=True)
    
    # Create a basic Button component if it doesn't exist
    button_component = components_dir / 'Button.tsx'
    if not button_component.exists():
        button_component.write_text(
            'import { ButtonHTMLAttributes, FC } from \'react\';\n\n' 
            'interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {\n' 
            '  variant?: \'primary\' | \'secondary\' | \'outline\';\n' 
            '  size?: \'sm\' | \'md\' | \'lg\';\n}\n\n' 
            'export const Button: FC<ButtonProps> = ({\n' 
            '  children,\n' 
            '  className = \'\',\n' 
            '  variant = \'primary\',\n' 
            '  size = \'md\',\n' 
            '  ...props\n' 
            '}) => {\n' 
            '  const baseStyles = \'font-medium rounded focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed\';\n' 
            '  const variants = {\n' 
            '    primary: \'bg-indigo-600 text-white hover:bg-indigo-700\',\n' 
            '    secondary: \'bg-gray-200 text-gray-800 hover:bg-gray-300\',\n' 
            '    outline: \'border border-gray-300 text-gray-700 hover:bg-gray-50\'\n' 
            '  };\n' 
            '  const sizes = {\n' 
            '    sm: \'px-2 py-1 text-sm\',\n' 
            '    md: \'px-4 py-2 text-base\',\n' 
            '    lg: \'px-6 py-3 text-lg\'\n' 
            '  };\n\n' 
            '  return (\n' 
            '    <button\n' 
            '      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}\n' 
            '      {...props}\n' 
            '    >\n' 
            '      {children}\n' 
            '    </button>\n' 
            '  );\n' 
            '};\n'
        )
    
    # Create pages if router is enabled
    if options.get('router', False):
        pages_dir = src_dir / 'pages'
        pages_dir.mkdir(exist_ok=True)
        
        # Home page
        home_page = pages_dir / 'HomePage.tsx'
        if not home_page.exists():
            home_page.write_text(
                'import { useState } from \'react\';\n' 
                'import { Button } from \'../components/Button\';\n\n' 
                'export default function HomePage() {\n' 
                '  const [count, setCount] = useState(0);\n\n' 
                '  return (\n' 
                '    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">\n' 
                '      <div className="max-w-4xl mx-auto text-center">\n' 
                '        <h1 className="text-4xl font-bold text-gray-900 mb-8">\n' 
                '          Welcome to {process.env.VITE_APP_NAME || "React App"}\n' 
                '        </h1>\n' 
                '        <div className="bg-white p-8 rounded-lg shadow-md">\n' 
                '          <p className="text-lg text-gray-700 mb-6">\n' 
                '            Get started by editing <code className="bg-gray-100 px-2 py-1 rounded">src/App.tsx</code>\n' 
                '          </p>\n' 
                '          <div className="space-y-4">\n' 
                '            <Button\n' 
                '              variant="primary"\n' 
                '              onClick={() => setCount((count) => count + 1)}\n' 
                '              className="mx-2"\n' 
                '            >\n' 
                '              Count is {count}\n' 
                '            </Button>\n' 
                '            <p className="text-sm text-gray-500 mt-4">\n' 
                '              Click the button to test state management\n' 
                '            </p>\n' 
                '          </div>\n' 
                '        </div>\n' 
                '      </div>\n' 
                '    </div>\n' 
                '  );\n' 
                '}\n'
            )
        
        # About page
        about_page = pages_dir / 'AboutPage.tsx'
        if not about_page.exists():
            about_page.write_text(
                'import { Link } from \'react-router-dom\';\n' 
                'import { Button } from \'../components/Button\';\n\n' 
                'export default function AboutPage() {\n' 
                '  return (\n' 
                '    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">\n' 
                '      <div className="max-w-4xl mx-auto">\n' 
                '        <div className="bg-white p-8 rounded-lg shadow-md">\n' 
                '          <h1 className="text-3xl font-bold text-gray-900 mb-6">About</h1>\n' 
                '          <p className="text-gray-700 mb-6">\n' 
                '            This is a modern React application created with Vite and TypeScript.\n' 
                '            It includes best practices for development and production.\n' 
                '          </p>\n' 
                '          <div className="mt-8 space-x-4">\n' 
                '            <Button as={Link} to="/" variant="primary">\n' 
                '              Back to Home\n' 
                '            </Button>\n' 
                '            <Button\n' 
                '              as="a"\n' 
                '              href="https://vitejs.dev/"\n' 
                '              target="_blank"\n' 
                '              rel="noopener noreferrer"\n' 
                '              variant="outline"\n' 
                '            >\n' 
                '              Learn Vite\n' 
                '            </Button>\n' 
                '            <Button\n' 
                '              as="a"\n' 
                '              href="https://react.dev/"\n' 
                '              target="_blank"\n' 
                '              rel="noopener noreferrer"\n' 
                '              variant="outline"\n' 
                '            >\n' 
                '              Learn React\n' 
                '            </Button>\n' 
                '          </div>\n' 
                '        </div>\n' 
                '      </div>\n' 
                '    </div>\n' 
                '  );\n' 
                '}\n'
            )
        
        # Create a layout component if it doesn't exist
        layout_file = src_dir / 'components' / 'Layout.tsx'
        if not layout_file.exists():
            layout_file.write_text(
                'import { ReactNode } from \'react\';\n' 
                'import { Link } from \'react-router-dom\';\n\n' 
                'interface LayoutProps {\n' 
                '  children: ReactNode;\n' 
                '}\n\n' 
                'export function Layout({ children }: LayoutProps) {\n' 
                '  return (\n' 
                '    <div className="min-h-screen flex flex-col">\n' 
                '      <header className="bg-white shadow">\n' 
                '        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">\n' 
                '          <nav className="flex space-x-8">\n' 
                '            <Link to="/" className="text-gray-900 hover:text-indigo-600 px-3 py-2 text-sm font-medium">\n' 
                '              Home\n' 
                '            </Link>\n' 
                '            <Link to="/about" className="text-gray-500 hover:text-indigo-600 px-3 py-2 text-sm font-medium">\n' 
                '              About\n' 
                '            </Link>\n' 
                '          </nav>\n' 
                '        </div>\n' 
                '      </header>\n' 
                '      <main className="flex-grow">\n' 
                '        {children}\n' 
                '      </main>\n' 
                '      <footer className="bg-white border-t border-gray-200 mt-12">\n' 
                '        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">\n' 
                '          <p className="text-center text-sm text-gray-500">\n' 
                '            &copy; {new Date().getFullYear()} {process.env.VITE_APP_NAME || "My App"}. All rights reserved.\n' 
                '          </p>\n' 
                '        </div>\n' 
                '      </footer>\n' 
                '    </div>\n' 
                '  );\n' 
                '}\n'
            )
    
    # Create a basic test file if testing is enabled
    if options.get('testing'):
        test_dir = src_dir / '__tests__'
        test_dir.mkdir(exist_ok=True)
        
        # Create a basic test for the Button component
        button_test = test_dir / 'Button.test.tsx'
        if not button_test.exists():
            button_test.write_text(
                'import { render, screen, fireEvent } from \'@testing-library/react\';\n' 
                'import { Button } from \'../components/Button\';\n\n' 
                'describe(\'Button\', () => {\n' 
                '  it(\'renders the button with children\', () => {\n' 
                '    render(<Button>Click me</Button>);\n' 
                '    expect(screen.getByText(\'Click me\')).toBeInTheDocument();\n' 
                '  });\n' 
                '  it(\'calls onClick when clicked\', () => {\n' 
                '    const handleClick = jest.fn();\n' 
                '    render(<Button onClick={handleClick}>Click me</Button>);\n' 
                '    fireEvent.click(screen.getByText(\'Click me\'));\n' 
                '    expect(handleClick).toHaveBeenCalledTimes(1);\n' 
                '  });\n' 
                '});\n'
            )

    # Create components directory
    components_dir = src_dir / 'components'
    components_dir.mkdir(exist_ok=True)

    # Create a basic Button component if it doesn't exist
    button_component = components_dir / 'Button.tsx'
    if not button_component.exists():
        button_component.write_text(
            'import { ButtonHTMLAttributes, FC } from \'react\';\n\n' 
            'interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {\n' 
            '  variant?: \'primary\' | \'secondary\' | \'outline\';\n' 
            '  size?: \'sm\' | \'md\' | \'lg\';\n' 
            '  as?: React.ElementType;\n' 
            '  to?: string;\n' 
            '}\n\n' 
            'export const Button: FC<ButtonProps> = ({\n' 
            '  children,\n' 
            '  variant = \'primary\',\n' 
            '  size = \'md\',\n' 
            '  className = \'\',\n' 
            '  as: Component = \'button\',\n' 
            '  ...props\n' 
            '}) => {\n' 
            '  const baseStyles = \'font-medium rounded focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 inline-flex items-center justify-center\';\n' 
            '  const variantStyles = {\n' 
            '    primary: \'bg-indigo-600 text-white hover:bg-indigo-700\',\n' 
            '    secondary: \'bg-gray-100 text-gray-700 hover:bg-gray-200\',\n' 
            '    outline: \'bg-transparent border border-gray-300 text-gray-700 hover:bg-gray-50\'\n' 
            '  };\n\n' 
            '  const sizeStyles = {\n' 
            '    sm: \'px-3 py-1.5 text-sm\',\n' 
            '    md: \'px-4 py-2 text-base\',\n' 
            '    lg: \'px-6 py-3 text-lg\'\n' 
            '  };\n\n' 
            '  return (\n' 
            '    <Component\n' 
            '      className={`${baseStyles} ${variantStyles[variant as keyof typeof variantStyles]} ${sizeStyles[size as keyof typeof sizeStyles]} ${className}`}\n' 
            '      {...props}\n' 
            '    >\n' 
            '      {children}\n' 
            '    </Component>\n' 
            '  );\n' 
            '};\n'
        )

    # Create a Card component if it doesn't exist
    card_component = components_dir / 'Card.tsx'
    if not card_component.exists():
        card_component.write_text(
            'import { FC, ReactNode } from \'react\';\n\n' 
            'interface CardProps {\n' 
            '  children: ReactNode;\n' 
            '  className?: string;\n' 
            '  title?: string;\n' 
            '}\n\n' 
            'export const Card: FC<CardProps> = ({ children, className = \'\', title }) => (\n' 
            '  <div className={`bg-white rounded-lg shadow-md overflow-hidden ${className}`}>\n' 
            '    {title && (\n' 
            '      <div className="px-6 py-4 border-b border-gray-200">\n' 
            '        <h3 className="text-lg font-medium text-gray-900">{title}</h3>\n' 
            '      </div>\n' 
            '    )}\n' 
            '    <div className="p-6">{children}</div>\n' 
            '  </div>\n' 
            ');\n'
        )

    # Create an Input component if it doesn't exist
    input_component = components_dir / 'Input.tsx'
    if not input_component.exists():
        input_component.write_text(
            'import { InputHTMLAttributes, forwardRef } from \'react\';\n\n' 
            'interface InputProps extends InputHTMLAttributes<HTMLInputElement> {\n' 
            '  label?: string;\n' 
            '  error?: string;\n' 
            '}\n\n' 
            'export const Input = forwardRef<HTMLInputElement, InputProps>(({ label, error, className = \'\', ...props }, ref) => (\n' 
            '  <div className="w-full">\n' 
            '    {label && (\n' 
            '      <label className="block text-sm font-medium text-gray-700 mb-1">\n' 
            '        {label}\n' 
            '      </label>\n' 
            '    )}\n' 
            '    <input\n' 
            '      ref={ref}\n' 
            '      className={`block w-full px-3 py-2 border ${error ? \'border-red-500\' : \'border-gray-300\'} rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${className}`}\n' 
            '      {...props}\n' 
            '    />\n' 
            '    {error && <p className="mt-1 text-sm text-red-600">{error}</p>}\n' 
            '  </div>\n' 
            '));\n\n' 
            'Input.displayName = \'Input\';\n'
        )

    # Create pages if router is enabled
    if options.get('router', False):
        pages_dir = src_dir / 'pages'
        pages_dir.mkdir(exist_ok=True)
        
    # Home page
    home_page = pages_dir / 'HomePage.tsx'
    if not home_page.exists():
        home_page.write_text(
            'import { useState } from \'react\';\n' 
            'import { Button } from \'../components/Button\';\n\n' 
            'export default function HomePage() {\n' 
            '  const [count, setCount] = useState(0);\n\n' 
            '  return (\n' 
            '    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">\n' 
            '      <div className="max-w-4xl mx-auto text-center">\n' 
            '        <h1 className="text-4xl font-bold text-gray-900 mb-8">\n' 
            '          Welcome to {process.env.VITE_APP_NAME || "React App"}\n' 
            '        </h1>\n' 
            '        <div className="bg-white p-8 rounded-lg shadow-md">\n' 
            '          <p className="text-lg text-gray-700 mb-6">\n' 
            '            Get started by editing <code className="bg-gray-100 px-2 py-1 rounded">src/App.tsx</code>\n' 
            '          </p>\n' 
            '          <div className="space-y-4">\n' 
            '            <Button\n' 
            '              variant="primary"\n' 
            '              onClick={() => setCount((count) => count + 1)}\n' 
            '              className="mx-2"\n' 
            '            >\n' 
            '              Count is {count}\n' 
            '            </Button>\n' 
            '            <p className="text-sm text-gray-500 mt-4">\n' 
            '              Click the button to test state management\n' 
            '            </p>\n' 
            '          </div>\n' 
            '        </div>\n' 
            '      </div>\n' 
            '    </div>\n' 
            '  );\n' 
            '}\n'
        )
    
    # About page
    about_page = pages_dir / 'AboutPage.tsx'
    if not about_page.exists():
        about_page.write_text(
            'import { Link } from \'react-router-dom\';\n' 
            'import { Button } from \'../components/Button\';\n\n' 
            'export default function AboutPage() {\n' 
            '  return (\n' 
            '    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">\n' 
            '      <div className="max-w-4xl mx-auto">\n' 
            '        <div className="bg-white p-8 rounded-lg shadow-md">\n' 
            '          <h1 className="text-3xl font-bold text-gray-900 mb-6">About</h1>\n' 
            '          <p className="text-gray-700 mb-6">\n' 
            '            This is a modern React application created with Vite and TypeScript.\n' 
            '            It includes best practices for development and production.\n' 
            '          </p>\n' 
            '          <div className="mt-8 space-x-4">\n' 
            '            <Button as={Link} to="/" variant="primary">\n' 
            '              Back to Home\n' 
            '            </Button>\n' 
            '            <Button\n' 
            '              as="a"\n' 
            '              href="https://vitejs.dev/"\n' 
            '              target="_blank"\n' 
            '              rel="noopener noreferrer"\n' 
            '              variant="outline"\n' 
            '            >\n' 
            '              Learn Vite\n' 
            '            </Button>\n' 
            '            <Button\n' 
            '              as="a"\n' 
            '              href="https://react.dev/"\n' 
            '              target="_blank"\n' 
            '              rel="noopener noreferrer"\n' 
            '              variant="outline"\n' 
            '            >\n' 
            '              Learn React\n' 
            '            </Button>\n' 
            '          </div>\n' 
            '        </div>\n' 
            '      </div>\n' 
            '    </div>\n' 
            '  );\n' 
            '}\n'
        )
    
    # Create a layout component if it doesn't exist
    layout_file = src_dir / 'components' / 'Layout.tsx'
    if not layout_file.exists():
        layout_file.write_text(
            'import { ReactNode } from \'react\';\n' 
            'import { Link } from \'react-router-dom\';\n\n' 
            'interface LayoutProps {\n' 
            '  children: ReactNode;\n' 
            '}\n\n' 
            'export function Layout({ children }: LayoutProps) {\n' 
            '  return (\n' 
            '    <div className="min-h-screen flex flex-col">\n' 
            '      <header className="bg-white shadow">\n' 
            '        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">\n' 
            '          <nav className="flex space-x-8">\n' 
            '            <Link to="/" className="text-gray-900 hover:text-indigo-600 px-3 py-2 text-sm font-medium">\n' 
            '              Home\n' 
            '            </Link>\n' 
            '            <Link to="/about" className="text-gray-500 hover:text-indigo-600 px-3 py-2 text-sm font-medium">\n' 
            '              About\n' 
            '            </Link>\n' 
            '          </nav>\n' 
            '        </div>\n' 
            '      </header>\n' 
            '      <main className="flex-grow">\n' 
            '        {children}\n' 
            '      </main>\n' 
            '      <footer className="bg-white border-t border-gray-200 mt-12">\n' 
            '        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">\n' 
            '          <p className="text-center text-sm text-gray-500">\n' 
            '            &copy; {new Date().getFullYear()} {process.env.VITE_APP_NAME || "My App"}. All rights reserved.\n' 
            '          </p>\n' 
            '        </div>\n' 
            '      </footer>\n' 
            '    </div>\n' 
            '  );\n' 
            '}\n'
        )

    if options.get('testing'):
        test_dir = src_dir / '__tests__'
        test_dir.mkdir(exist_ok=True)
        
        # Create a basic test for the Button component
        button_test = test_dir / 'Button.test.tsx'
        if not button_test.exists():
            button_test.write_text(
                'import { render, screen, fireEvent } from \'@testing-library/react\';\n' 
                'import { Button } from \'../components/Button\';\n\n' 
                'describe(\'Button\', () => {\n' 
                '  it(\'renders the button with children\', () => {\n' 
                '    render(<Button>Click me</Button>);\n' 
                '    expect(screen.getByText(\'Click me\')).toBeInTheDocument();\n' 
                '  });\n\n' 
                '  it(\'calls onClick when clicked\', () => {\n' 
                '    const handleClick = jest.fn();\n' 
                '    render(<Button onClick={handleClick}>Click me</Button>);\n' 
                '    fireEvent.click(screen.getByText(\'Click me\'));\n' 
                '    expect(handleClick).toHaveBeenCalledTimes(1);\n' 
                '  });\n' 
                '});\n'
            )

    logger.info("React components created successfully")

def _create_vue_package_json(project_name: str, options: dict) -> Dict[str, Any]:
    """
    Create package.json for a Vue 3 project with TypeScript and Vite.
    
    Args:
        project_name: Name of the Vue project
        options: Project configuration options
        
    Returns:
        Dict containing the package.json data
    """
    # Base dependencies
    dependencies = {
        "vue": "^3.3.0",
        "pinia": "^2.1.0",
        "vue-router": "^4.2.0"
    }
    
    # Development dependencies
    dev_dependencies = {
        "@vitejs/plugin-vue": "^4.0.0",
        "@vitejs/plugin-vue-jsx": "^3.0.0",
        "@vue/compiler-sfc": "^3.3.0",
        "@vue/eslint-config-typescript": "^12.0.0",
        "@vue/tsconfig": "^0.4.0",
        "typescript": "^5.0.0",
        "vite": "^4.0.0",
        "vite-plugin-vue-devtools": "^7.0.0",
        "eslint": "^8.0.0",
        "eslint-plugin-vue": "^9.0.0",
        "@types/node": "^20.0.0",
        "@vitejs/plugin-legacy": "^4.0.0"
    }
    
    # Add testing dependencies if enabled
    if options.get("with_tests", True):
        dev_dependencies.update({
            "@vue/test-utils": "^2.4.0",
            "@vue/vue3-jest": "^29.0.0",
            "jest": "^29.0.0",
            "ts-jest": "^29.0.0",
            "@types/jest": "^29.0.0",
            "jsdom": "^22.0.0"
        })
    
    # Add E2E testing if enabled
    if options.get("with_e2e", False):
        dev_dependencies.update({
            "@cypress/vue": "^5.0.0",
            "cypress": "^12.0.0",
            "cypress-axe": "^1.0.0"
        })
    
    # Configure scripts
    scripts = {
        "dev": "vite",
        "build": "vue-tsc --noEmit && vite build",
        "preview": "vite preview",
        "type-check": "vue-tsc --noEmit",
        "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix --ignore-path .gitignore"
    }
    
    # Add test scripts if testing is enabled
    if options.get("with_tests", True):
        scripts.update({
            "test:unit": "jest",
            "test:unit:watch": "jest --watch",
            "test:coverage": "jest --coverage"
        })
    
    # Add E2E test scripts if enabled
    if options.get("with_e2e", False):
        scripts.update({
            "test:e2e": "cypress run",
            "test:e2e:open": "cypress open"
        })
    
    # Create the package.json structure
    package_json = {
        "name": project_name,
        "version": "0.1.0",
        "private": True,
        "type": "module",
        "scripts": scripts,
        "dependencies": dependencies,
        "devDependencies": dev_dependencies
    }
    
    # Add browserslist configuration
    package_json["browserslist"] = [
        "> 1%",
        "last 2 versions",
        "not dead",
        "not ie 11"
    ]
    
    # Add engines configuration
    package_json["engines"] = {
        "node": ">=16.0.0",
        "npm": ">=8.0.0"
    }
    
    return package_json

def _create_vue_project_structure(project_path: Path, options: dict) -> None:
    """
    Create the directory structure for a Vue 3 project.
    
    Args:
        project_path: Base path for the project
        options: Project configuration options
    """
    # Create main directories
    src_dir = project_path / 'src'
    public_dir = project_path / 'public'
    tests_dir = project_path / 'tests'
    
    # Source subdirectories
    dirs = [
        src_dir,
        src_dir / 'assets',
        src_dir / 'components',
        src_dir / 'composables',
        src_dir / 'layouts',
        src_dir / 'router',
        src_dir / 'stores',
        src_dir / 'styles',
        src_dir / 'views',
        public_dir,
        tests_dir / 'unit',
        tests_dir / 'e2e'
    ]
    
    # Create all directories
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)
        
        # Add .gitkeep to empty directories
        if not any(directory.iterdir()):
            (directory / '.gitkeep').touch()
    
    # Create initial files
    (src_dir / 'main.ts').write_text('// Main application entry point\n')
    (src_dir / 'App.vue').write_text('<!-- Main App component -->\n')
    (src_dir / 'styles' / 'main.css').write_text('/* Main styles */\n')
    
    # Create a basic README if it doesn't exist
    readme_path = project_path / 'README.md'
    if not readme_path.exists():
        readme_path.write_text(f"# {project_path.name}\n\nVue 3 project created with Web Development MCP.\n")
    
    logger.info(f"Created Vue project structure at {project_path}")

def _create_vue_config_files(project_path: Path, options: dict) -> None:
    """
    Create configuration files for a Vue 3 project.
    
    Args:
        project_path: Base path for the project
        options: Project configuration options
    """
    # Vite config
    vite_config = '''import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [
    vue({
      script: {
        defineModel: true,
        propsDestructure: true
      }
    }),
    vueJsx(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 3000,
    open: true,
    host: true
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './tests/unit/setup.ts'
  }
})'''
    
    # TypeScript config
    ts_config = '''{
  "compilerOptions": {
    "target": "ESNext",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "moduleResolution": "Node",
    "strict": true,
    "jsx": "preserve",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "lib": ["ESNext", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "noEmit": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": [
    "src/**/*.ts",
    "src/**/*.d.ts",
    "src/**/*.tsx",
    "src/**/*.vue",
    "tests/**/*.ts",
    "tests/**/*.tsx"
  ],
  "references": [
    {
      "path": "./tsconfig.node.json"
    }
  ]
}'''
    
    # Node TypeScript config
    ts_config_node = '''{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}'''
    
    # ESLint config
    eslint_config = '''module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
    'vue/setup-compiler-macros': true
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier'
  ],
  parser: 'vue-eslint-parser',
  parserOptions: {
    ecmaVersion: 'latest',
    parser: '@typescript-eslint/parser',
    sourceType: 'module'
  },
  plugins: ['vue', '@typescript-eslint'],
  rules: {
    'vue/multi-word-component-names': 'off',
    'vue/component-tags-order': ['error', {
      'order': ['script', 'template', 'style']
    }],
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],
    'vue/attribute-hyphenation': ['error', 'always']
  },
  overrides: [
    {
      files: ['**/*.spec.ts', '**/*.test.ts'],
      env: {
        jest: true
      }
    }
  ]
}'''
    
    # Prettier config
    prettier_config = '''{
  "semi": false,
  "singleQuote": true,
  "printWidth": 100,
  "trailingComma": "es5",
  "tabWidth": 2,
  "useTabs": false,
  "endOfLine": "auto"
}'''
    
    # Jest config
    jest_config = '''export default {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  moduleFileExtensions: ['js', 'jsx', 'ts', 'tsx', 'json', 'vue'],
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest',
    '^.+\\.(js|jsx)$': 'babel-jest',
    '^.+\\.vue$': '@vue/vue3-jest'
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^\\.(css|less|scss|sass)$': 'identity-obj-proxy'
  },
  testMatch: ['**/tests/unit/**/*.spec.[jt]s?(x)'],
  testEnvironmentOptions: {
    customExportConditions: ['node', 'node-addons']
  },
  setupFilesAfterEnv: ['<rootDir>/tests/unit/setup.ts']
}'''
    
    # Write all config files
    config_files = [
        (project_path / 'vite.config.ts', vite_config),
        (project_path / 'tsconfig.json', ts_config),
        (project_path / 'tsconfig.node.json', ts_config_node),
        (project_path / '.eslintrc.js', eslint_config),
        (project_path / '.prettierrc', prettier_config),
        (project_path / 'jest.config.js', jest_config)
    ]
    
    for file_path, content in config_files:
        file_path.write_text(content, encoding='utf-8')
    
    logger.info("Created Vue configuration files")

def _create_vue_components(project_path: Path, options: dict) -> None:
    """
    Create initial Vue components and application files.
    
    Args:
        project_path: Base path for the project
        options: Project configuration options
    """
    src_dir = project_path / 'src'
    
    # Main App component
    app_vue = '''<template>
  <div id="app">
    <header>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/about">About</router-link>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  margin: 0 10px;
  text-decoration: none;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
'''
    
    # Main entry point
    main_ts = '''import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
'''
    
    # Router configuration
    router_index_ts = '''import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/AboutView.vue')
    }
  ]
})

export default router
'''
    
    # Pinia store example
    store_counter_ts = '''import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    name: 'Counter'
  }),
  getters: {
    doubleCount: (state) => state.count * 2
  },
  actions: {
    increment() {
      this.count++
    },
    reset() {
      this.count = 0
    }
  }
})
'''
    
    # Home view
    home_view = '''<template>
  <div class="home">
    <h1>Welcome to Your Vue.js + TypeScript App</h1>
    <p>This is a sample home page component.</p>
    
    <div class="counter">
      <h3>Counter Example</h3>
      <p>Count: {{ counter.count }}</p>
      <p>Double: {{ counter.doubleCount }}</p>
      <button @click="counter.increment">Increment</button>
      <button @click="counter.reset">Reset</button>
    </div>
    
    <div class="features">
      <h3>Features</h3>
      <ul>
        <li>Vue 3 Composition API</li>
        <li>TypeScript</li>
        <li>Vite</li>
        <li>Vue Router</li>
        <li>Pinia for state management</li>
        <li>ESLint + Prettier</li>
        <li>Jest for unit testing</li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useCounterStore } from '@/stores/counter'

const counter = useCounterStore()
</script>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.counter {
  margin: 20px 0;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
}

button {
  margin: 0 5px;
  padding: 5px 10px;
  cursor: pointer;
}

.features {
  margin-top: 30px;
  text-align: left;
}

.features ul {
  list-style-type: none;
  padding: 0;
}

.features li {
  padding: 5px 0;
  position: relative;
  padding-left: 25px;
}

.features li:before {
  content: '✓';
  color: #42b983;
  position: absolute;
  left: 0;
}
</style>
'''
    
    # About view
    about_view = '''<template>
  <div class="about">
    <h1>About This Project</h1>
    <p>
      This is a Vue 3 application generated with Web Development MCP.
    </p>
    <p>
      It includes modern tooling and best practices for Vue development.
    </p>
  </div>
</template>

<style scoped>
.about {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: left;
}

.about h1 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.about p {
  margin-bottom: 15px;
  line-height: 1.6;
}
</style>
'''
    
    # Main CSS
    main_css = '''/* Main CSS file */
:root {
  --primary-color: #42b983;
  --secondary-color: #2c3e50;
  --text-color: #2c3e50;
  --border-color: #eaeaea;
  --success-color: #4caf50;
  --warning-color: #ff9800;
  --danger-color: #f44336;
  --background-color: #ffffff;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-color);
  background-color: var(--background-color);
  line-height: 1.6;
}

a {
  color: var(--primary-color);
  text-decoration: none;
}

button, .btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s;
}

button:hover, .btn:hover {
  opacity: 0.9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.text-center {
  text-align: center;
}

.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }

.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }

.p-1 { padding: 0.5rem; }
.p-2 { padding: 1rem; }
.p-3 { padding: 1.5rem; }
.p-4 { padding: 2rem; }
'''
    
    # Test setup file
    test_setup_ts = '''// Jest setup file
import { config } from '@vue/test-utils'

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn()
  }))
})

// Global mocks can be added here
'''
    
    # Example test file
    example_test_ts = '''import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import HelloWorld from '@/components/HelloWorld.vue'

describe('HelloWorld', () => {
  it('renders properly', () => {
    const wrapper = mount(HelloWorld, {
      props: {
        msg: 'Hello Vue 3 + Vite'
      }
    })
    expect(wrapper.text()).toContain('Hello Vue 3 + Vite')
  })
})
'''
    
    # Create all component files
    component_files = [
        (src_dir / 'App.vue', app_vue),
        (src_dir / 'main.ts', main_ts),
        (src_dir / 'router' / 'index.ts', router_index_ts),
        (src_dir / 'stores' / 'counter.ts', store_counter_ts),
        (src_dir / 'views' / 'HomeView.vue', home_view),
        (src_dir / 'views' / 'AboutView.vue', about_view),
        (src_dir / 'styles' / 'main.css', main_css),
        (project_path / 'tests' / 'unit' / 'setup.ts', test_setup_ts),
        (project_path / 'tests' / 'unit' / 'example.spec.ts', example_test_ts)
    ]
    
    for file_path, content in component_files:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
    
    logger.info("Created Vue components and application files")
