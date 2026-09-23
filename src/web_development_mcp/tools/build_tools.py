"""
Build configuration and development tools.

Handles Vite, TypeScript, Biome, and other build tool configurations.
"""

import json
import logging
from pathlib import Path
from typing import Annotated, Any

from pydantic import Field

logger = logging.getLogger(__name__)

_MUTATING = {}


def register_tools(mcp):
    """Register build tools with the MCP server."""

    @mcp.tool(annotations=_MUTATING)
    def configure_typescript(
        project_path: Annotated[str, Field(description="Path to the project directory")],
        strict_mode: Annotated[bool, Field(description="Enable strict TypeScript checking")] = True,
        target: Annotated[str, Field(description="TypeScript compilation target")] = "ES2020",
        include_react: Annotated[bool, Field(description="Include React-specific settings (jsx react-jsx)")] = False,
    ) -> dict[str, Any]:
        """Create or update tsconfig.json with strict, modern defaults.

        Writes tsconfig.json (path mapping @/*, sourcemaps, ESM bundler
        resolution) plus React JSX and noUnusedLocals/Parameters when asked.

        ## Return Format

        `{success, message, project_path, config_file, strict_mode, target,
        react_support, features}`.

        ## Examples

        - configure_typescript(project_path="D:/proj", strict_mode=True,
          include_react=True) -> writes tsconfig.json with jsx react-jsx.
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
                "message": f"Wrote tsconfig.json (strict={strict_mode}, react={include_react})",
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
            logger.exception(f"Error configuring TypeScript: {e}")
            return {"success": False, "error": str(e), "message": f"TypeScript config failed: {e}"}

    @mcp.tool(annotations=_MUTATING)
    def configure_biome(
        project_path: Annotated[str, Field(description="Path to the project directory")],
        framework: Annotated[str, Field(description="Frontend framework (react, vue, svelte)")] = "react",
        typescript: Annotated[bool, Field(description="Include TypeScript strict rules")] = True,
        strict_rules: Annotated[bool, Field(description="Use strict rule set")] = True,
    ) -> dict[str, Any]:
        """Create biome.json (replaces ESLint + Prettier).

        Writes formatter + linter config with organize-imports on.

        ## Return Format

        `{success, message, config_files}`.

        ## Examples

        - configure_biome(project_path="D:/proj") -> writes biome.json.
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
                "javascript": {"formatter": {"quoteStyle": "single", "trailingCommas": "all", "semicolons": "always"}},
            }
            if strict_rules:
                biome_config["linter"]["rules"]["correctness"]["noUnusedVariables"] = "error"
            biome_path = path / "biome.json"
            with open(biome_path, "w", encoding="utf-8") as f:
                json.dump(biome_config, f, indent=2)
            return {
                "success": True,
                "config_files": ["biome.json"],
                "message": "Biome configured (replaces ESLint + Prettier)",
            }
        except Exception as e:
            logger.exception(f"Error configuring Biome: {e}")
            return {"success": False, "error": str(e), "message": f"Biome config failed: {e}"}

    @mcp.tool(annotations=_MUTATING)
    def configure_vite(
        project_path: Annotated[str, Field(description="Path to the project directory")],
        framework: Annotated[str, Field(description="Frontend framework (react, vue, svelte)")] = "react",
        port: Annotated[int, Field(description="Development server port")] = 11099,
        enable_https: Annotated[bool, Field(description="Enable HTTPS for development server")] = False,
    ) -> dict[str, Any]:
        """Create vite.config.ts optimized for development.

        Writes path aliases, sourcemaps, bundle splitting, and the dev
        server port. Never hardcode another repo's fleet port here — pass
        the project's own port.

        ## Return Format

        `{success, message, project_path, framework, config_file,
        server_config, features}`.

        ## Examples

        - configure_vite(project_path="D:/proj", framework="react", port=11099) ->
          writes vite.config.ts serving on 11099.
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
                "message": f"Wrote vite.config.ts for {framework} on port {port}",
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
            logger.exception(f"Error configuring Vite: {e}")
            return {"success": False, "error": str(e), "message": f"Vite config failed: {e}"}

    @mcp.tool(annotations=_MUTATING)
    def setup_testing_config(
        project_path: Annotated[str, Field(description="Path to the project directory")],
        framework: Annotated[str, Field(description="Frontend framework (react, vue, svelte)")] = "react",
        test_runner: Annotated[str, Field(description="Testing framework (vitest, jest)")] = "vitest",
    ) -> dict[str, Any]:
        """Write Vitest + Testing Library config (vitest.config.ts, src/test/setup.ts).

        ## Return Format

        `{success, message, project_path, framework, test_runner,
        config_files, features}`.

        ## Examples

        - setup_testing_config(project_path="D:/proj") ->
          writes vitest.config.ts + src/test/setup.ts (JSDOM).
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
                "message": f"Wrote {test_runner} testing config for {framework}",
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
            logger.exception(f"Error setting up testing: {e}")
            return {"success": False, "error": str(e), "message": f"Testing setup failed: {e}"}
