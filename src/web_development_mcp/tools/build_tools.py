"""
Build configuration and development tools.

Handles Vite, TypeScript, ESLint, and other build tool configurations.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def register_tools(mcp):
    """Register build tools with the MCP server."""

    @mcp.tool()
    def configure_typescript(
        project_path: str,
        strict_mode: bool = True,
        target: str = "ES2020",
        include_react: bool = False,
    ) -> dict[str, Any]:
        """Create or update TypeScript configuration.

        Args:
            project_path: Path to the project directory
            strict_mode: Enable strict TypeScript checking
            target: TypeScript compilation target
            include_react: Include React-specific TypeScript settings
        """
        try:
            path = Path(project_path)
            tsconfig_path = path / "tsconfig.json"

            # Base TypeScript configuration
            tsconfig = {
                "compilerOptions": {
                    "target": target,
                    "lib": ["DOM", "DOM.Iterable", "ES6"],
                    "allowJs": True,
                    "skipLibCheck": True,
                    "esModuleInterop": True,
                    "allowSyntheticDefaultImports": True,
                    "strict": strict_mode,
                    "forceConsistentCasingInFileNames": True,
                    "noFallthroughCasesInSwitch": True,
                    "module": "esnext",
                    "moduleResolution": "bundler",
                    "resolveJsonModule": True,
                    "isolatedModules": True,
                    "noEmit": True,
                    "declaration": False,
                    "declarationMap": False,
                    "sourceMap": True,
                    "outDir": "./dist",
                    "baseUrl": ".",
                    "paths": {"@/*": ["src/*"]},
                },
                "include": ["src/**/*", "src/**/*.tsx", "src/**/*.ts"],
                "exclude": ["node_modules", "dist", "build"],
            }

            # React-specific settings
            if include_react:
                tsconfig["compilerOptions"]["jsx"] = "react-jsx"
                tsconfig["compilerOptions"]["lib"].append("ES2015")

            # Additional strict settings
            if strict_mode:
                tsconfig["compilerOptions"].update(
                    {
                        "noUnusedLocals": True,
                        "noUnusedParameters": True,
                        "noImplicitReturns": True,
                        "noImplicitAny": True,
                        "strictNullChecks": True,
                        "strictFunctionTypes": True,
                        "strictBindCallApply": True,
                    }
                )

            # Write configuration
            with open(tsconfig_path, "w", encoding="utf-8") as f:
                json.dump(tsconfig, f, indent=2)

            return {
                "success": True,
                "project_path": project_path,
                "config_file": "tsconfig.json",
                "strict_mode": strict_mode,
                "target": target,
                "react_support": include_react,
                "features": [
                    "Path mapping (@/* -> src/*)",
                    "Source maps",
                    "ES modules",
                    "Strict checking" if strict_mode else "Lenient checking",
                    "React JSX" if include_react else "No JSX",
                ],
            }

        except Exception as e:
            logger.error(f"Error configuring TypeScript: {e}")
            return {"success": False, "error": str(e)}

    @mcp.tool()
    def configure_biome(
        project_path: str,
        framework: str = "react",
        typescript: bool = True,
        strict_rules: bool = True,
    ) -> dict[str, Any]:
        """Create Biome configuration (replaces ESLint + Prettier).

        Args:
            project_path: Path to the project directory
            framework: Frontend framework (react, vue, svelte)
            typescript: Include TypeScript strict rules
            strict_rules: Use strict rule set
        """
        try:
            path = Path(project_path)
            biome_config = {
                "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
                "organizeImports": {"enabled": True},
                "linter": {
                    "enabled": True,
                    "rules": {
                        "recommended": True,
                        "complexity": {"noUselessFragments": "error"},
                        "correctness": {"useExhaustiveDependencies": "warn" if framework == "react" else "off"},
                        "style": {"noNonNullAssertion": "off"},
                        "suspicious": {"noConsole": "warn"},
                    },
                },
                "formatter": {"enabled": True, "indentStyle": "space", "indentWidth": 2, "lineWidth": 100},
                "javascript": {
                    "formatter": {"quoteStyle": "single", "trailingCommas": "all", "semicolons": "always"}
                },
            }
            if strict_rules:
                biome_config["linter"]["rules"]["correctness"]["noUnusedVariables"] = "error"
            biome_path = path / "biome.json"
            with open(biome_path, "w", encoding="utf-8") as f:
                json.dump(biome_config, f, indent=2)
            return {"success": True, "config_files": ["biome.json"], "message": "Biome configured (replaces ESLint + Prettier)"}
        except Exception as e:
            return {"success": False, "error": str(e)}
                        "no-debugger": "error",
                        "no-unused-vars": "error",
                        "no-undef": "error",
                        "prefer-const": "error",
                        "no-var": "error",
                        "eqeqeq": "error",
                        "curly": "error",
                        "semi": ["error", "always"],
                        "quotes": ["error", "single"],
                        "indent": ["error", 2],
                        "comma-dangle": ["error", "never"],
                        "object-curly-spacing": ["error", "always"],
                        "array-bracket-spacing": ["error", "never"],
                        "space-before-blocks": "error",
                        "keyword-spacing": "error",
                    }
                )

                if typescript:
                    eslint_config["rules"].update(
                        {
                            "@typescript-eslint/no-unused-vars": "error",
                            "@typescript-eslint/explicit-function-return-type": "warn",
                            "@typescript-eslint/no-explicit-any": "warn",
                            "@typescript-eslint/prefer-nullish-coalescing": "error",
                            "@typescript-eslint/prefer-optional-chain": "error",
                        }
                    )

            # Write configuration
            with open(eslint_path, "w", encoding="utf-8") as f:
                json.dump(eslint_config, f, indent=2)

            # Create .eslintignore
            eslintignore_content = """dist/
build/
node_modules/
*.min.js
coverage/
.env
.env.local
.env.production
"""

            with open(path / ".eslintignore", "w", encoding="utf-8") as f:
                f.write(eslintignore_content)

            return {
                "success": True,
                "project_path": project_path,
                "framework": framework,
                "typescript": typescript,
                "strict_rules": strict_rules,
                "config_files": [".eslintrc.json", ".eslintignore"],
                "features": [
                    f"{framework.title()} support",
                    "TypeScript integration" if typescript else "JavaScript only",
                    "Austrian dev standards" if strict_rules else "Standard rules",
                    "Import/export validation",
                    "Code style enforcement",
                ],
            }

        except Exception as e:
            logger.error(f"Error configuring ESLint: {e}")
            return {"success": False, "error": str(e)}

    @mcp.tool()
    def configure_vite(
        project_path: str, framework: str = "react", port: int = 10700, enable_https: bool = False
    ) -> dict[str, Any]:
        """Create Vite configuration optimized for development.

        Args:
            project_path: Path to the project directory
            framework: Frontend framework (react, vue, svelte)
            port: Development server port
            enable_https: Enable HTTPS for development server
        """
        try:
            path = Path(project_path)
            vite_config_path = path / "vite.config.ts"

            # Framework-specific plugin imports
            plugin_imports = {
                "react": "import react from '@vitejs/plugin-react';",
                "vue": "import vue from '@vitejs/plugin-vue';",
                "svelte": "import { svelte } from '@sveltejs/vite-plugin-svelte';",
            }

            plugin_usage = {"react": "react()", "vue": "vue()", "svelte": "svelte()"}

            # Create Vite configuration
            vite_config = f"""import {{ defineConfig }} from 'vite';
{plugin_imports.get(framework, "")}
import {{ resolve }} from 'path';

export default defineConfig({{
  plugins: [{plugin_usage.get(framework, "")}],

  server: {{
    port: {port},
    open: true,
    https: {str(enable_https).lower()},
    host: true
  }},

  resolve: {{
    alias: {{
      '@': resolve(__dirname, 'src')
    }}
  }},

  build: {{
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {{
      output: {{
        manualChunks: {{
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom']
        }}
      }}
    }}
  }},

  css: {{
    devSourcemap: true
  }},

  optimizeDeps: {{
    include: ['{framework}']
  }}
}});
"""

            # Write configuration
            with open(vite_config_path, "w", encoding="utf-8") as f:
                f.write(vite_config)

            return {
                "success": True,
                "project_path": project_path,
                "framework": framework,
                "config_file": "vite.config.ts",
                "server_config": {"port": port, "https": enable_https, "host": True, "open": True},
                "features": [
                    f"{framework.title()} plugin",
                    "Path aliases (@/ -> src/)",
                    "Source maps",
                    "Bundle splitting",
                    "CSS source maps",
                    "Dependency optimization",
                ],
            }

        except Exception as e:
            logger.error(f"Error configuring Vite: {e}")
            return {"success": False, "error": str(e)}

    @mcp.tool()
    def setup_testing_config(
        project_path: str, framework: str = "react", test_runner: str = "vitest"
    ) -> dict[str, Any]:
        """Setup testing configuration with Vitest and Testing Library.

        Args:
            project_path: Path to the project directory
            framework: Frontend framework (react, vue, svelte)
            test_runner: Testing framework (vitest, jest)
        """
        try:
            path = Path(project_path)

            if test_runner == "vitest":
                # Create vitest.config.ts
                vitest_config = """import { defineConfig } from 'vitest/config';
import { resolve } from 'path';

export default defineConfig({
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    globals: true
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  }
});
"""

                with open(path / "vitest.config.ts", "w", encoding="utf-8") as f:
                    f.write(vitest_config)

                # Create test setup file
                test_dir = path / "src" / "test"
                test_dir.mkdir(parents=True, exist_ok=True)

                setup_content = """import '@testing-library/jest-dom';
"""

                with open(test_dir / "setup.ts", "w", encoding="utf-8") as f:
                    f.write(setup_content)

            return {
                "success": True,
                "project_path": project_path,
                "framework": framework,
                "test_runner": test_runner,
                "config_files": ["vitest.config.ts", "src/test/setup.ts"],
                "features": [
                    "JSDOM environment",
                    "Testing Library integration",
                    "Global test utilities",
                    "Path aliases support",
                ],
            }

        except Exception as e:
            logger.error(f"Error setting up testing: {e}")
            return {"success": False, "error": str(e)}
