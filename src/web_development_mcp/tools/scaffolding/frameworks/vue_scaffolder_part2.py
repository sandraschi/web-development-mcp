"""
Vue 3 project scaffolding implementation - Part 2.

This module contains configuration file creation for Vue 3 projects.
"""

import json
from pathlib import Path
from typing import Any


class VueScaffolderConfigs:
    """Handles creation of configuration files for Vue 3 projects."""

    @staticmethod
    def create_config_files(project_path: Path, options: dict[str, Any]) -> None:
        """Create all configuration files for a Vue project."""
        VueScaffolderConfigs._create_tsconfig(project_path, options)
        VueScaffolderConfigs._create_vite_config(project_path, options)
        VueScaffolderConfigs._create_eslint_config(project_path, options)
        VueScaffolderConfigs._create_tailwind_config(project_path, options)
        VueScaffolderConfigs._create_postcss_config(project_path, options)

    @staticmethod
    def _create_tsconfig(project_path: Path, options: dict[str, Any]) -> None:
        """Create tsconfig.json for TypeScript configuration."""
        tsconfig = {
            "compilerOptions": {
                "target": "ES2020",
                "useDefineForClassFields": True,
                "module": "ESNext",
                "lib": ["ES2020", "DOM", "DOM.Iterable"],
                "skipLibCheck": True,
                "moduleResolution": "bundler",
                "allowImportingTsExtensions": True,
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "strict": True,
                "noUnusedLocals": True,
                "noUnusedParameters": True,
                "noFallthroughCasesInSwitch": True,
                "baseUrl": ".",
                "paths": {"@/*": ["./src/*"]},
                "types": ["vite/client", "@vitejs/plugin-vue", "@vitejs/plugin-vue-jsx"],
            },
            "include": [
                "src/**/*.ts",
                "src/**/*.d.ts",
                "src/**/*.tsx",
                "src/**/*.vue",
                "tests/**/*.ts",
                "tests/**/*.tsx",
            ],
            "exclude": ["node_modules"],
        }

        with open(project_path / "tsconfig.json", "w") as f:
            json.dump(tsconfig, f, indent=2)

    @staticmethod
    def _create_vite_config(project_path: Path, options: dict[str, Any]) -> None:
        """Create vite.config.ts for Vite configuration."""
        vite_config = """import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';
import { fileURLToPath, URL } from 'node:url';
import VueDevTools from 'vite-plugin-vue-devtools';

export default defineConfig({
  plugins: [
    vue({
      script: {
        defineModel: true,
        propsDestructure: true
      }
    }),
    vueJsx(),
    VueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
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
    setupFiles: './tests/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
});
"""
        with open(project_path / "vite.config.ts", "w") as f:
            f.write(vite_config)

    @staticmethod
    def _create_eslint_config(project_path: Path, options: dict[str, Any]) -> None:
        """Create .eslintrc.js for ESLint configuration."""
        eslint_config = """module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
    'vue/setup-compiler-macros': true,
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
    'plugin:@typescript-eslint/recommended',
    '@vue/eslint-config-typescript',
    '@vue/eslint-config-prettier',
  ],
  parser: 'vue-eslint-parser',
  parserOptions: {
    ecmaVersion: 'latest',
    parser: '@typescript-eslint/parser',
    sourceType: 'module',
  },
  plugins: ['vue', '@typescript-eslint'],
  rules: {
    'vue/multi-word-component-names': 'off',
    'vue/no-multiple-template-root': 'off',
    'vue/component-tags-order': ['error', {
      'order': ['script', 'template', 'style']
    }],
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],
    'vue/attributes-order': ['error', {
      'order': [
        'DEFINITION',
        'LIST_RENDERING',
        'CONDITIONALS',
        'RENDER_MODIFIERS',
        'GLOBAL',
        'UNIQUE',
        'TWO_WAY_BINDING',
        'OTHER_DIRECTIVES',
        'OTHER_ATTR',
        'EVENTS',
        'CONTENT'
      ]
    }]
  },
  overrides: [
    {
      files: ['**/__tests__/*.{j,t}s?(x)', '**/tests/unit/**/*.spec.{j,t}s?(x)'],
      env: {
        jest: true,
      },
    },
  ],
};
"""
        with open(project_path / ".eslintrc.js", "w") as f:
            f.write(eslint_config)

    @staticmethod
    def _create_tailwind_config(project_path: Path, options: dict[str, Any]) -> None:
        """Create tailwind.config.js for Tailwind CSS configuration."""
        tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#3b82f6',
          light: '#60a5fa',
          dark: '#2563eb',
        },
      },
    },
  },
  plugins: [],
}
"""
        with open(project_path / "tailwind.config.js", "w") as f:
            f.write(tailwind_config)

    @staticmethod
    def _create_postcss_config(project_path: Path, options: dict[str, Any]) -> None:
        """Create postcss.config.js for PostCSS configuration."""
        postcss_config = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
        with open(project_path / "postcss.config.js", "w") as f:
            f.write(postcss_config)
