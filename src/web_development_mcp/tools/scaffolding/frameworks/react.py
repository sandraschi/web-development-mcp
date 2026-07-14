"""
React project scaffolding implementation.

This module provides functionality to scaffold new React projects with TypeScript,
Vite, and other modern tooling.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ReactScaffolder:
    """Scaffolder implementation for React projects."""

    @staticmethod
    def create_project(project_name: str, project_path: Path, options: dict[str, Any]) -> dict[str, Any]:
        """Create a new React project.

        Args:
            project_name: Name of the project
            project_path: Path where the project should be created
            options: Project configuration options

        Returns:
            Dict containing project creation results
        """
        try:
            # Create project structure
            ReactScaffolder._create_project_structure(project_path, options)

            # Create package.json
            _package_json = ReactScaffolder._create_package_json(project_name, project_path, options)

            # Create config files
            ReactScaffolder._create_config_files(project_path, options)

            # Create initial components
            ReactScaffolder._create_components(project_path, options, project_name)

            return {
                "success": True,
                "project_name": project_name,
                "project_path": str(project_path),
                "framework": "react",
                "features_included": [
                    "TypeScript",
                    "Vite",
                    "ESLint" + (" (strict)" if options.get("eslint_strict", False) else ""),
                    "Prettier" if options.get("prettier", True) else None,
                    "React Router" if options.get("router", True) else None,
                    "Testing Library" if options.get("testing", True) else None,
                    "Husky git hooks" if options.get("husky", False) else None,
                ],
                "next_steps": [f"cd {project_path}", "npm install", "npm run dev"],
            }

        except Exception as e:
            logger.error(f"Error creating React app: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def validate_options(options: dict[str, Any]) -> list[str]:
        """Validate React project options.

        Args:
            options: Options to validate

        Returns:
            List of validation errors, empty if valid
        """
        errors = []

        # Add any React-specific validation here

        return errors

    @staticmethod
    def _create_project_structure(project_path: Path, options: dict[str, Any]) -> None:
        """Create the directory structure for a React project."""
        # Create main directories
        (project_path / "src").mkdir(parents=True, exist_ok=True)
        (project_path / "public").mkdir(exist_ok=True)
        (project_path / "src/components").mkdir(exist_ok=True)
        (project_path / "src/hooks").mkdir(exist_ok=True)
        (project_path / "src/utils").mkdir(exist_ok=True)
        (project_path / "src/assets").mkdir(exist_ok=True)

        if options.get("router", True):
            (project_path / "src/pages").mkdir(exist_ok=True)

        if options.get("testing", True):
            (project_path / "src/__tests__").mkdir(exist_ok=True)

    @staticmethod
    def _create_package_json(project_name: str, project_path: Path, options: dict[str, Any]) -> dict[str, Any]:
        """Create package.json for a React project."""
        package_json = {
            "name": project_name,
            "private": True,
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "tsc && vite build",
                "preview": "vite preview",
                "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
            },
            "dependencies": {"react": "^18.2.0", "react-dom": "^18.2.0"},
            "devDependencies": {
                "@types/react": "^18.2.55",
                "@types/react-dom": "^18.2.19",
                "@types/node": "^20.0.0",
                "@typescript-eslint/eslint-plugin": "^6.0.0",
                "@typescript-eslint/parser": "^6.0.0",
                "@vitejs/plugin-react": "^4.2.1",
                "autoprefixer": "^10.4.17",
                "eslint": "^8.0.0",
                "eslint-plugin-react-hooks": "^4.6.0",
                "eslint-plugin-react-refresh": "^0.4.5",
                "postcss": "^8.4.35",
                "tailwindcss": "^3.4.0",
                "typescript": "^5.3.0",
                "vite": "^5.0.0",
                "vite-tsconfig-paths": "^4.3.0",
            },
        }

        # Add React Router if enabled
        if options.get("router", True):
            package_json["dependencies"]["react-router-dom"] = "^6.22.0"

        # Add testing dependencies if enabled
        if options.get("testing", True):
            package_json["devDependencies"].update(
                {
                    "@testing-library/jest-dom": "^6.1.4",
                    "@testing-library/react": "^14.1.2",
                    "@testing-library/user-event": "^14.5.1",
                    "@types/jest": "^29.5.10",
                    "jest": "^29.7.0",
                    "jest-environment-jsdom": "^29.7.0",
                    "ts-jest": "^29.1.1",
                    "vitest": "^1.2.0",
                }
            )

            # Update scripts
            package_json["scripts"].update(
                {
                    "test": "vitest",
                    "test:watch": "vitest watch",
                    "test:coverage": "vitest run --coverage",
                    "typecheck": "tsc --noEmit",
                }
            )

        # Add Prettier if enabled
        if options.get("prettier", True):
            package_json["devDependencies"].update({"prettier": "^3.1.0", "eslint-config-prettier": "^9.0.0"})

            # Add Prettier config
            prettier_config = {
                "semi": True,
                "singleQuote": True,
                "printWidth": 100,
                "tabWidth": 2,
                "useTabs": False,
                "trailingComma": "es5",
                "bracketSpacing": True,
                "arrowParens": "always",
            }

            with open(project_path / ".prettierrc", "w") as f:
                json.dump(prettier_config, f, indent=2)

        # Add Husky if enabled
        if options.get("husky", False):
            package_json["devDependencies"].update({"husky": "^8.0.0", "lint-staged": "^15.0.0"})

            # Add Husky config
            husky_config = {"hooks": {"pre-commit": "lint-staged"}}

            # Add lint-staged config
            lint_staged_config = {"*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"]}

            with open(project_path / ".huskyrc.json", "w") as f:
                json.dump(husky_config, f, indent=2)

            with open(project_path / ".lintstagedrc.json", "w") as f:
                json.dump(lint_staged_config, f, indent=2)

        # Write package.json
        with open(project_path / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)

        return package_json

    @staticmethod
    def _create_config_files(project_path: Path, options: dict[str, Any]) -> None:
        """Create configuration files for a React project."""
        # Create tsconfig.json
        tsconfig = {
            "compilerOptions": {
                "target": "ES2020",
                "useDefineForClassFields": True,
                "lib": ["DOM", "DOM.Iterable", "ESNext"],
                "allowJs": False,
                "skipLibCheck": True,
                "esModuleInterop": True,
                "allowSyntheticDefaultImports": True,
                "strict": True,
                "forceConsistentCasingInFileNames": True,
                "module": "ESNext",
                "moduleResolution": "bundler",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx",
                "baseUrl": ".",
                "paths": {"@/*": ["./src/*"]},
            },
            "include": ["src"],
            "exclude": ["node_modules", "dist"],
        }

        with open(project_path / "tsconfig.json", "w") as f:
            json.dump(tsconfig, f, indent=2)

        # Create vite.config.ts
        vite_config = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  server: {
    port: 3000,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/__tests__/setup.ts',
  },
});
"""
        with open(project_path / "vite.config.ts", "w") as f:
            f.write(vite_config)

        # Create .eslintrc.json
        eslint_config = {
            "root": True,
            "env": {"browser": True, "es2021": True, "node": True, "jest": True},
            "extends": [
                "eslint:recommended",
                "plugin:react/recommended",
                "plugin:react-hooks/recommended",
                "plugin:@typescript-eslint/recommended",
                "plugin:import/errors",
                "plugin:import/warnings",
                "plugin:import/typescript",
                "plugin:jsx-a11y/recommended",
            ],
            "parser": "@typescript-eslint/parser",
            "parserOptions": {
                "ecmaFeatures": {"jsx": True},
                "ecmaVersion": "latest",
                "sourceType": "module",
            },
            "plugins": ["react", "react-hooks", "@typescript-eslint", "import", "jsx-a11y"],
            "rules": {
                "react/react-in-jsx-scope": "off",
                "react/prop-types": "off",
                "@typescript-eslint/explicit-module-boundary-types": "off",
            },
            "settings": {"react": {"version": "detect"}, "import/resolver": {"typescript": {}}},
        }

        if options.get("prettier", True):
            eslint_config["extends"].append("prettier")
            eslint_config["plugins"].append("prettier")
            eslint_config["rules"]["prettier/prettier"] = ["error"]

        if options.get("eslint_strict", False):
            eslint_config["rules"].update(
                {
                    "@typescript-eslint/no-explicit-any": "error",
                    "@typescript-eslint/no-non-null-assertion": "error",
                    "@typescript-eslint/no-unused-vars": ["error", {"argsIgnorePattern": "^_"}],
                    "react-hooks/exhaustive-deps": "warn",
                }
            )

        with open(project_path / ".eslintrc.json", "w") as f:
            json.dump(eslint_config, f, indent=2)

    @staticmethod
    def _create_components(project_path: Path, options: dict[str, Any], project_name: str = "React App") -> None:
        """Create initial React components."""
        # Create App.tsx
        app_tsx = """import { useState } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="text-3xl font-bold text-blue-600">
          Welcome to React + Vite
        </h1>
        <p className="mt-4">
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
        <div className="mt-6">
          <button
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            onClick={() => setCount((count) => count + 1)}
          >
            Count is: {count}
          </button>
        </div>
        <p className="mt-6">
          <a
            className="text-blue-400 hover:underline"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
          {' | '}
          <a
            className="text-blue-400 hover:underline"
            href="https://vitejs.dev/guide/features.html"
            target="_blank"
            rel="noopener noreferrer"
          >
            Vite Docs
          </a>
        </p>
      </header>
    </div>
  );
}

export default App;
"""
        with open(project_path / "src/App.tsx", "w") as f:
            f.write(app_tsx)

        # Create main.tsx
        main_tsx = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
"""
        with open(project_path / "src/main.tsx", "w") as f:
            f.write(main_tsx)

        # Create index.css
        index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;

  color-scheme: light dark;
  color: rgba(255, 255, 255, 0.87);
  background-color: #242424;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  margin: 0;
  display: flex;
  place-items: center;
  min-width: 320px;
  min-height: 100vh;
}

#root {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

@media (prefers-color-scheme: light) {
  :root {
    color: #213547;
    background-color: #ffffff;
  }
}
"""
        with open(project_path / "src/index.css", "w") as f:
            f.write(index_css)

        # Create index.html
        index_html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite + React + TypeScript</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""
        with open(project_path / "index.html", "w") as f:
            f.write(index_html)

        # Create test setup file if testing is enabled
        if options.get("testing", True):
            test_setup = """// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';
"""
            (project_path / "src/__tests__/setup.ts").parent.mkdir(parents=True, exist_ok=True)
            with open(project_path / "src/__tests__/setup.ts", "w") as f:
                f.write(test_setup)

            # Create a basic test
            app_test = """import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App', () => {
  it('renders welcome message', () => {
    render(<App />);
    expect(screen.getByText(/Welcome to React/)).toBeInTheDocument();
  });
});
"""
            with open(project_path / "src/__tests__/App.test.tsx", "w") as f:
                f.write(app_test)

        # Create a components/Button.tsx example
        button_tsx = """import { ButtonHTMLAttributes, FC } from 'react';

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
};

const Button: FC<ButtonProps> = ({
  children,
  className = '',
  variant = 'primary',
  size = 'md',
  ...props
}) => {
  const baseStyles = 'rounded font-medium focus:outline-none focus:ring-2 focus:ring-offset-2';

  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  };

  const sizes = {
    sm: 'px-2 py-1 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
"""
        with open(project_path / "src/components/Button.tsx", "w") as f:
            f.write(button_tsx)

        # Create a custom hook example
        use_counter_ts = """import { useState } from 'react';

type CounterOptions = {
  initialValue?: number;
  step?: number;
};

export function useCounter({ initialValue = 0, step = 1 }: CounterOptions = {}) {
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount((c) => c + step);
  const decrement = () => setCount((c) => c - step);
  const reset = () => setCount(initialValue);

  return {
    count,
    increment,
    decrement,
    reset,
  };
}
"""
        with open(project_path / "src/hooks/useCounter.ts", "w") as f:
            f.write(use_counter_ts)

        # Create a utility function example
        utils_ts = """/**
 * Formats a number as a currency string
 * @param amount - The amount to format
 * @param currency - The currency code (default: 'USD')
 * @returns Formatted currency string
 */
export function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}

/**
 * Truncates a string to a maximum length
 * @param str - The string to truncate
 * @param maxLength - Maximum length before truncation
 * @returns Truncated string with ellipsis if needed
 */
export function truncate(str: string, maxLength: number): string {
  if (str.length <= maxLength) return str;
  return `${str.substring(0, maxLength)}...`;
}
"""
        with open(project_path / "src/utils/string.ts", "w") as f:
            f.write(utils_ts)

        # Create a README.md
        readme_md = f"""# {project_name}

This project was bootstrapped with the Web Development MCP React template.

## Available Scripts

In the project directory, you can run:

### `npm start` or `npm run dev`

Runs the app in development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### `npm run build`

Builds the app for production to the `dist` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

### `npm test`

Launches the test runner in interactive watch mode.

### `npm run lint`

Runs ESLint on the project files.

## Learn More

You can learn more in the [React documentation](https://reactjs.org/).

To learn more about Vite, check out the [Vite documentation](https://vitejs.dev/).
"""
        with open(project_path / "README.md", "w") as f:
            f.write(readme_md)
