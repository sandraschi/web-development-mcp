"""
SvelteKit project scaffolding utilities.

Provides functionality to create and configure new SvelteKit projects.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


def create_svelte_package_json(project_name: str, options: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create package.json for a SvelteKit project.

    Args:
        project_name: Name of the SvelteKit project
        options: Project configuration options

    Returns:
        Dict containing the package.json data
    """
    return {
        "name": project_name,
        "version": "0.0.1",
        "private": True,
        "type": "module",
        "scripts": {
            "dev": "vite dev",
            "build": "vite build",
            "preview": "vite preview",
            "check": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json",
            "check:watch": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json --watch",
            "test": "vitest",
            "test:watch": "vitest watch",
            "test:coverage": "vitest run --coverage",
            "format": "prettier --plugin-search-dir . --write . && eslint . --fix",
            "lint": "eslint .",
            "package": "svelte-kit sync && svelte-package",
            "prepare": "svelte-kit sync",
        },
        "devDependencies": {
            "@sveltejs/adapter-auto": "^3.0.0",
            "@sveltejs/kit": "^2.0.0",
            "@sveltejs/vite-plugin-svelte": "^3.0.0",
            "@testing-library/jest-dom": "^6.1.4",
            "@testing-library/svelte": "^4.0.0",
            "@testing-library/user-event": "^14.4.3",
            "@types/jest": "^29.5.0",
            "@types/node": "^20.0.0",
            "@typescript-eslint/eslint-plugin": "^6.0.0",
            "@typescript-eslint/parser": "^6.0.0",
            "eslint": "^8.0.0",
            "eslint-config-prettier": "^9.0.0",
            "eslint-plugin-svelte": "^2.0.0",
            "jsdom": "^22.0.0",
            "prettier": "^3.0.0",
            "prettier-plugin-svelte": "^3.0.0",
            "svelte": "^4.0.0",
            "svelte-check": "^3.0.0",
            "ts-jest": "^29.0.5",
            "typescript": "^5.0.0",
            "vite": "^5.0.0",
            "vitest": "^1.0.0",
        },
        "dependencies": {"@sveltejs/adapter-node": "^3.0.0"},
    }


def create_svelte_project_structure(project_path: Path, options: Dict[str, Any]) -> None:
    """
    Create the directory structure for a SvelteKit project.

    Args:
        project_path: Base path for the project
        options: Project configuration options
    """
    # Create main directories
    (project_path / "src").mkdir(parents=True, exist_ok=True)
    (project_path / "src/lib").mkdir(exist_ok=True)
    (project_path / "src/routes").mkdir(exist_ok=True)

    # Create app.html
    app_html = """<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8" />
		<link rel="icon" href="%sveltekit.assets%/favicon.png" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		%sveltekit.head%
	</head>
	<body data-sveltekit-preload-data="hover">
		<div style="display: contents">%sveltekit.body%</div>
	</body>
</html>"""
    (project_path / "src/app.html").write_text(app_html)


def create_svelte_config_files(project_path: Path, options: Dict[str, Any]) -> None:
    """
    Create configuration files for a SvelteKit project.

    Args:
        project_path: Base path for the project
        options: Project configuration options
    """
    # Create svelte.config.js
    svelte_config = """import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/kit/vite';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapter()
  },
  preprocess: vitePreprocess()
};

export default config;
"""
    (project_path / "svelte.config.js").write_text(svelte_config)

    # Create tsconfig.json
    tsconfig = {
        "extends": "./.svelte-kit/tsconfig.json",
        "compilerOptions": {
            "allowJs": True,
            "checkJs": True,
            "esModuleInterop": True,
            "forceConsistentCasingInFileNames": True,
            "resolveJsonModule": True,
            "skipLibCheck": True,
            "sourceMap": True,
            "strict": True,
        },
    }
    (project_path / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2))

    # Create .eslintrc.cjs
    eslint_config = """module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:svelte/recommended',
    'prettier'
  ],
  parserOptions: {
    sourceType: 'module',
    ecmaVersion: 2020,
    extraFileExtensions: ['.svelte']
  },
  env: {
    browser: true,
    es2017: true,
    node: true
  },
  plugins: ['@typescript-eslint'],
  overrides: [
    {
      files: ['*.svelte'],
      parser: 'svelte-eslint-parser',
      parserOptions: {
        parser: '@typescript-eslint/parser'
      }
    }
  ]
};
"""
    (project_path / ".eslintrc.cjs").write_text(eslint_config)

    # Create .prettierrc
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
    (project_path / ".prettierrc").write_text(json.dumps(prettier_config, indent=2))

    # Create .gitignore
    gitignore = """# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Directory for instrumented libs generated by jscoverage/JSCover
lib-cov

# Coverage directory used by tools like istanbul
coverage
*.lcov

# Dependency directories
node_modules/
.pnp
.pnp.js

# Environment variables
.env
.env.local
.env.*.local

# Build output
.svelte-kit
build
dist

# IDE
.vscode/
.idea/

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db"""
    (project_path / ".gitignore").write_text(gitignore)


def create_svelte_components(project_path: Path, options: Dict[str, Any]) -> None:
    """
    Create initial Svelte components and application files.

    Args:
        project_path: Base path for the project
        options: Project configuration options
    """
    # Create src/app.d.ts
    app_d_ts = """// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
  namespace App {
    // interface Error {}
    // interface Locals {}
    // interface PageData {}
    // interface Platform {}
  }
}

export {};
"""
    (project_path / "src/app.d.ts").write_text(app_d_ts)

    # Create src/routes/+layout.svelte
    layout_svelte = """<script lang="ts">
  import '../app.css';
</script>

<slot />
"""
    (project_path / "src/routes/+layout.svelte").write_text(layout_svelte)

    # Create src/routes/+page.svelte (homepage)
    page_svelte = """<script lang="ts">
  let count = 0;

  function increment() {
    count += 1;
  }
</script>

<main class="container">
  <h1>Welcome to SvelteKit</h1>
  <p>This is a new SvelteKit project.</p>

  <div class="card">
    <button on:click={increment}>
      Count: {count}
    </button>
  </div>

  <p>
    Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation
  </p>
</main>

<style>
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
    text-align: center;
  }

  h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }

  .card {
    padding: 2em;
    margin: 2em 0;
    border-radius: 8px;
    background: #f5f5f5;
    display: inline-block;
  }

  button {
    padding: 0.5em 1em;
    border: none;
    border-radius: 4px;
    background: #4CAF50;
    color: white;
    font-size: 1em;
    cursor: pointer;
  }

  button:hover {
    background: #45a049;
  }

  @media (prefers-color-scheme: dark) {
    :root {
      color: #f5f5f5;
      background: #1a1a1a;
    }

    a {
      color: #646cff;
    }

    button {
      background: #1a1a1a;
      border: 1px solid #646cff;
    }
  }
</style>
"""
    (project_path / "src/routes/+page.svelte").write_text(page_svelte)

    # Create src/app.css
    app_css = """/* Global styles */
:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;

  color-scheme: light dark;
  color: #213547;
  background-color: #ffffff;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

a {
  font-weight: 500;
  color: #646cff;
  text-decoration: inherit;
}

a:hover {
  color: #535bf2;
}

body {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
}

h1 {
  font-size: 3.2em;
  line-height: 1.1;
}

button {
  border-radius: 8px;
  border: 1px solid transparent;
  padding: 0.6em 1.2em;
  font-size: 1em;
  font-weight: 500;
  font-family: inherit;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: border-color 0.25s;
}

button:hover {
  border-color: #646cff;
}

button:focus,
button:focus-visible {
  outline: 4px auto -webkit-focus-ring-color;
}

@media (prefers-color-scheme: dark) {
  :root {
    color: rgba(255, 255, 255, 0.87);
    background-color: #242424;
  }

  a:hover {
    color: #747bff;
  }

  button {
    background-color: #1a1a1a;
  }
}
"""
    (project_path / "src/app.css").write_text(app_css)

    # Create vitest.config.ts
    vitest_config = """import { svelte } from "@sveltejs/vite-plugin-svelte";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [svelte({ hot: !process.env.VITEST })],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./vitest-setup.ts"],
  },
});
"""
    (project_path / "vitest.config.ts").write_text(vitest_config)

    # Create vitest-setup.ts
    vitest_setup = """import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/svelte';
import matchers from '@testing-library/jest-dom/matchers';

// Extend Vitest's expect method with methods from react-testing-library
expect.extend(matchers);

// Run cleanup after each test case (e.g., clearing jsdom)
afterEach(() => {
  cleanup();
});
"""
    (project_path / "vitest-setup.ts").write_text(vitest_setup)

    logger.info("Created SvelteKit components and application files")
