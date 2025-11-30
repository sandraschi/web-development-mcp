"""
Vue 3 project scaffolding implementation - Part 3.

This module contains component creation for Vue 3 projects.
"""

from pathlib import Path
from typing import Dict, Any

class VueScaffolderComponents:
    """Handles creation of Vue components and project files."""
    
    @staticmethod
    def create_components(project_path: Path, options: Dict[str, Any]) -> None:
        """Create all initial components and project files."""
        src_dir = project_path / 'src'
        
        # Create main application files
        VueScaffolderComponents._create_main_ts(src_dir, options)
        VueScaffolderComponents._create_app_vue(src_dir, options)
        VueScaffolderComponents._create_navbar(src_dir, options)
        
        # Create router if enabled
        if options.get("router", True):
            VueScaffolderComponents._create_router(src_dir, options)
            VueScaffolderComponents._create_views(src_dir, options)
        
        # Create Pinia store if enabled
        if options.get("pinia", True):
            VueScaffolderComponents._create_stores(src_dir, options)
        
        # Create styles
        VueScaffolderComponents._create_styles(src_dir, options)
        
        # Create index.html
        VueScaffolderComponents._create_index_html(project_path, options)
        
        # Create test files if testing is enabled
        if options.get("testing", True):
            VueScaffolderComponents._create_test_files(project_path, options)
        
        # Create README.md
        VueScaffolderComponents._create_readme(project_path, options)
    
    @staticmethod
    def _create_main_ts(src_dir: Path, options: Dict[str, Any]) -> None:
        """Create main.ts entry point."""
        main_ts = """import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
"""
        with open(src_dir / "main.ts", "w") as f:
            f.write(main_ts)
    
    @staticmethod
    def _create_app_vue(src_dir: Path, options: Dict[str, Any]) -> None:
        """Create App.vue root component."""
        app_vue = """<script setup lang="ts">
import { RouterView } from 'vue-router'
import TheNavbar from './components/TheNavbar.vue'
</script>

<template>
  <TheNavbar />
  <main class="container mx-auto px-4 py-8">
    <RouterView />
  </main>
</template>

<style scoped>
/* Add your styles here */
</style>
"""
        with open(src_dir / "App.vue", "w") as f:
            f.write(app_vue)
    
    @staticmethod
    def _create_navbar(src_dir: Path, options: Dict[str, Any]) -> None:
        """Create TheNavbar.vue component."""
        navbar_vue = """<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}
</script>

<template>
  <nav class="bg-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <RouterLink to="/" class="text-xl font-bold text-gray-900">
              Vue App
            </RouterLink>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <RouterLink 
              to="/" 
              class="border-indigo-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              active-class="border-indigo-500"
              exact-active-class="border-indigo-500"
            >
              Home
            </RouterLink>
            <RouterLink 
              to="/about" 
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              active-class="border-indigo-500 text-gray-900"
            >
              About
            </RouterLink>
          </div>
        </div>
        <div class="-mr-2 flex items-center sm:hidden">
          <button
            @click="toggleMenu"
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
            aria-expanded="false"
          >
            <span class="sr-only">Open main menu</span>
            <svg
              class="block h-6 w-6"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu, show/hide based on menu state. -->
    <div v-show="isMenuOpen" class="sm:hidden">
      <div class="pt-2 pb-3 space-y-1">
        <RouterLink
          to="/"
          class="bg-indigo-50 border-indigo-500 text-indigo-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
          active-class="bg-indigo-50 border-indigo-500 text-indigo-700"
          exact-active-class="bg-indigo-50 border-indigo-500 text-indigo-700"
          @click="isMenuOpen = false"
        >
          Home
        </RouterLink>
        <RouterLink
          to="/about"
          class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
          active-class="bg-indigo-50 border-indigo-500 text-indigo-700"
          @click="isMenuOpen = false"
        >
          About
        </RouterLink>
      </div>
    </div>
  </nav>
</template>
"""
        with open(src_dir / "components" / "TheNavbar.vue", "w") as f:
            f.write(navbar_vue)
    
    @staticmethod
    def _create_router(src_dir: Path, options: Dict[str, Any]) -> None:
        """Create router configuration."""
        (src_dir / "router").mkdir(exist_ok=True)
        
        router_ts = """import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

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
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
"""
        with open(src_dir / "router" / "index.ts", "w") as f:
            f.write(router_ts)
    
    @staticmethod
    def _create_views(src_dir: Path, options: Dict[str, Any]) -> None:
        """Create view components."""
        views_dir = src_dir / "views"
        views_dir.mkdir(exist_ok=True)
        
        # HomeView.vue
        home_view = """<template>
  <div class="home">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Welcome to Your Vue.js App</h1>
    <p class="text-lg text-gray-700 mb-6">
      For a guide and recipes on how to configure / customize this project,<br>
      check out the 
      <a 
        href="https://v3.vuejs.org/guide/" 
        target="_blank" 
        rel="noopener"
        class="text-indigo-600 hover:text-indigo-800 underline"
      >
        Vue 3 documentation
      </a>.
    </p>
    <div class="space-y-4">
      <h2 class="text-xl font-semibold text-gray-800">Installed CLI Plugins</h2>
      <ul class="list-disc pl-5 space-y-2">
        <li><a href="https://vitejs.dev/" target="_blank" rel="noopener" class="text-indigo-600 hover:underline">Vite</a></li>
        <li><a href="https://v3.vuejs.org/" target="_blank" rel="noopener" class="text-indigo-600 hover:underline">Vue 3</a></li>
        <li><a href="https://www.typescriptlang.org/" target="_blank" rel="noopener" class="text-indigo-600 hover:underline">TypeScript</a></li>
        <li><a href="https://tailwindcss.com/" target="_blank" rel="noopener" class="text-indigo-600 hover:underline">Tailwind CSS</a></li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomeView',
  components: {}
});
</script>
"""
        with open(views_dir / "HomeView.vue", "w") as f:
            f.write(home_view)
        
        # AboutView.vue
        about_view = """<template>
  <div class="about">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">About This Project</h1>
    <div class="prose max-w-none">
      <p class="text-lg text-gray-700 mb-4">
        This is a Vue 3 application generated with the Web Development MCP.
      </p>
      <p class="text-gray-700 mb-4">
        It includes modern tooling like Vite, TypeScript, Vue Router, Pinia, and Tailwind CSS.
      </p>
      <h2 class="text-xl font-semibold text-gray-800 mt-8 mb-4">Project Structure</h2>
      <div class="bg-gray-50 p-4 rounded-md mb-6">
        <pre class="text-sm text-gray-800">
src/
├── assets/          # Static assets
├── components/      # Reusable components
├── composables/     # Composable functions
├── router/          # Vue Router configuration
├── stores/          # Pinia stores
├── styles/          # Global styles
├── views/           # Route components
├── App.vue          # Root component
└── main.ts          # Application entry point</pre>
      </div>
      <h2 class="text-xl font-semibold text-gray-800 mt-8 mb-4">Available Scripts</h2>
      <ul class="list-disc pl-5 space-y-2">
        <li><code class="bg-gray-100 px-1.5 py-0.5 rounded">npm run dev</code> - Start development server</li>
        <li><code class="bg-gray-100 px-1.5 py-0.5 rounded">npm run build</code> - Build for production</li>
        <li><code class="bg-gray-100 px-1.5 py-0.5 rounded">npm run preview</code> - Preview production build</li>
        <li><code class="bg-gray-100 px-1.5 py-0.5 rounded">npm run test:unit</code> - Run unit tests</li>
        <li><code class="bg-gray-100 px-1.5 py-0.5 rounded">npm run lint</code> - Lint and fix files</li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'AboutView',
  components: {}
});
</script>
"""
        with open(views_dir / "AboutView.vue", "w") as f:
            f.write(about_view)
    
    @staticmethod
    def _create_stores(src_dir: Path, options: Dict[str, Any]) -> None:
        """Create Pinia store."""
        stores_dir = src_dir / "stores"
        stores_dir.mkdir(exist_ok=True)
        
        stores_index = """import { defineStore } from 'pinia'

export const useMainStore = defineStore('main', {
  state: () => ({
    counter: 0,
  }),
  getters: {
    doubleCount: (state) => state.counter * 2,
  },
  actions: {
    increment() {
      this.counter++
    },
  },
})
"""
        with open(stores_dir / "index.ts", "w") as f:
            f.write(stores_index)
    
    @staticmethod
    def _create_styles(src_dir: Path, options: Dict[str, Any]) -> None:
        """Create global styles."""
        assets_dir = src_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        
        main_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

/* Custom styles */
.container {
  @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8;
}
"""
        with open(assets_dir / "main.css", "w") as f:
            f.write(main_css)
    
    @staticmethod
    def _create_index_html(project_path: Path, options: Dict[str, Any]) -> None:
        """Create index.html."""
        index_html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vue 3 App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
"""
        with open(project_path / "index.html", "w") as f:
            f.write(index_html)
    
    @staticmethod
    def _create_test_files(project_path: Path, options: Dict[str, Any]) -> None:
        """Create test setup and example test files."""
        tests_dir = project_path / "tests"
        tests_dir.mkdir(exist_ok=True)
        
        # Create tests/setup.ts
        test_setup = """import { config } from '@vue/test-utils'
import { createI18n } from 'vue-i18n'
import { createTestingPinia } from '@pinia/testing'

// Mock global components
const components = ['RouterLink', 'RouterView']

components.forEach(component => {
  config.global.components[component] = component
  config.global.components[component] = component
})

// Mock i18n
config.global.plugins = [
  createI18n({
    legacy: false,
    locale: 'en',
    messages: {
      en: {}
    }
  }),
  createTestingPinia()
]
"""
        with open(tests_dir / "setup.ts", "w") as f:
            f.write(test_setup)
        
        # Create tests/unit/example.spec.ts
        unit_tests_dir = tests_dir / "unit"
        unit_tests_dir.mkdir(exist_ok=True)
        
        example_test = """import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import { useMainStore } from '../../src/stores'
import HomeView from '../../src/views/HomeView.vue'

describe('HomeView', () => {
  it('renders properly', () => {
    const wrapper = mount(HomeView)
    expect(wrapper.text()).toContain('Welcome to Your Vue.js App')
  })
})
"""
        with open(unit_tests_dir / "example.spec.ts", "w") as f:
            f.write(example_test)
    
    @staticmethod
    def _create_readme(project_path: Path, options: Dict[str, Any]) -> None:
        """Create README.md."""
        project_name = project_path.name
        
        readme = f"""# {project_name}

This project was bootstrapped with the Web Development MCP Vue template.

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## Recommended IDE Setup

- [VS Code](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin) to make the TypeScript language service aware of `.vue` types.

If the standalone TypeScript plugin doesn't feel fast enough to you, Volar has also implemented a [Take Over Mode](https://github.com/johnsoncodehk/volar/discussions/471#discussioncomment-1361669) that is more performant. You can enable it by the following steps:

1. Disable the built-in TypeScript Extension
    1. Run `Extensions: Show Built-in Extensions` from VSCode's command palette
    2. Find `TypeScript and JavaScript Language Features`, right click and select `Disable (Workspace)`
2. Reload the VSCode window by running `Developer: Reload Window` from the command palette.

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Structure

```
src/
├── assets/          # Static assets (images, fonts, etc.)
├── components/      # Reusable Vue components
├── composables/     # Composable functions (Vue 3 Composition API)
├── router/          # Vue Router configuration
├── stores/          # Pinia stores for state management
├── styles/          # Global styles and Tailwind configuration
├── views/           # Page components
├── App.vue          # Root component
└── main.ts          # Application entry point
```

## Learn More

- [Vue 3 Documentation](https://v3.vuejs.org/)
- [Vue Router Documentation](https://router.vuejs.org/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Vite Documentation](https://vitejs.dev/guide/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
"""
        with open(project_path / "README.md", "w") as f:
            f.write(readme)
