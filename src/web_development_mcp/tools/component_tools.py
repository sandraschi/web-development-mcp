"""
Component generation and code template tools.

Handles smart component creation with best practices and Austrian dev standards.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def register_tools(mcp):
    """Register component generation tools with the MCP server."""

    @mcp.tool()
    def generate_react_component(
        project_path: str,
        component_name: str,
        component_type: str = "functional",
        include_styles: bool = True,
        include_tests: bool = True,
        props_interface: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Generate a React component with TypeScript and best practices.

        Args:
            project_path: Path to the project directory
            component_name: Name of the component (PascalCase)
            component_type: Type of component (functional, class)
            include_styles: Create accompanying CSS module file
            include_tests: Create test file
            props_interface: Optional props interface definition {"propName": "propType"}
        """
        try:
            path = Path(project_path)

            # Validate component name
            if not _is_valid_component_name(component_name):
                return {
                    "success": False,
                    "error": "Component name must be PascalCase (e.g., MyComponent)",
                }

            # Create component directory
            component_dir = path / "src" / "components" / component_name
            component_dir.mkdir(parents=True, exist_ok=True)

            # Generate props interface
            props_code = ""
            if props_interface:
                props_code = f"interface {component_name}Props {{\n"
                for prop_name, prop_type in props_interface.items():
                    props_code += f"  {prop_name}: {prop_type};\n"
                props_code += "}\n\n"

            # Generate functional component
            component_code = f"""import React from 'react';
{f"import styles from './{component_name}.module.css';" if include_styles else ""}

{props_code}export const {component_name}: React.FC{f"<{component_name}Props>" if props_interface else ""} = ({{{", ".join(props_interface.keys()) if props_interface else ""}}}) => {{
  return (
    <div className={{{f"styles.{component_name.lower()}" if include_styles else f'"{component_name.lower()}"'}}}>
      <h2>{component_name} Component</h2>
      {f"<p>Welcome to the {component_name} component!</p>" if not props_interface else ""}
    </div>
  );
}};

export default {component_name};
"""

            # Write component file
            component_file = component_dir / f"{component_name}.tsx"
            with open(component_file, "w", encoding="utf-8") as f:
                f.write(component_code)

            files_created = [f"src/components/{component_name}/{component_name}.tsx"]

            # Generate styles
            if include_styles:
                styles_content = f""".{component_name.lower()} {{
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #ffffff;
}}

.{component_name.lower()} h2 {{
  margin-top: 0;
  color: #333;
  font-size: 1.5rem;
}}

.{component_name.lower()} p {{
  color: #666;
  line-height: 1.6;
}}
"""

                styles_file = component_dir / f"{component_name}.module.css"
                with open(styles_file, "w", encoding="utf-8") as f:
                    f.write(styles_content)

                files_created.append(f"src/components/{component_name}/{component_name}.module.css")

            # Generate tests
            if include_tests:
                test_content = f"""import {{ render, screen }} from '@testing-library/react';
import {{ {component_name} }} from '../{component_name}';

describe('{component_name}', () => {{
  it('renders without crashing', () => {{
    render(<{component_name} />);
    expect(screen.getByText('{component_name} Component')).toBeInTheDocument();
  }});
}});
"""

                test_dir = component_dir / "__tests__"
                test_dir.mkdir(exist_ok=True)
                test_file = test_dir / f"{component_name}.test.tsx"

                with open(test_file, "w", encoding="utf-8") as f:
                    f.write(test_content)

                files_created.append(
                    f"src/components/{component_name}/__tests__/{component_name}.test.tsx"
                )

            # Create index file for easier imports
            index_content = f"export {{ default, {component_name} }} from './{component_name}';\n"

            index_file = component_dir / "index.ts"
            with open(index_file, "w", encoding="utf-8") as f:
                f.write(index_content)

            files_created.append(f"src/components/{component_name}/index.ts")

            return {
                "success": True,
                "component_name": component_name,
                "component_type": component_type,
                "files_created": files_created,
                "features": [
                    "TypeScript interface" if props_interface else "No props",
                    "CSS modules" if include_styles else "No styles",
                    "Test file" if include_tests else "No tests",
                    "Index file for clean imports",
                    "Austrian dev standards",
                ],
                "import_statement": f"import {{ {component_name} }} from '@/components/{component_name}';",
                "usage_example": f"<{component_name} />",
            }

        except Exception as e:
            logger.error(f"Error generating React component: {e}")
            return {"success": False, "error": str(e)}

    @mcp.tool()
    def generate_vue_component(
        project_path: str,
        component_name: str,
        composition_api: bool = True,
        include_styles: bool = True,
        include_tests: bool = True,
    ) -> Dict[str, Any]:
        """Generate a Vue 3 component with TypeScript and Composition API.

        Args:
            project_path: Path to the project directory
            component_name: Name of the component (PascalCase)
            composition_api: Use Composition API (recommended for Vue 3)
            include_styles: Include scoped styles
            include_tests: Create test file
        """
        try:
            path = Path(project_path)

            if not _is_valid_component_name(component_name):
                return {"success": False, "error": "Component name must be PascalCase"}

            component_dir = path / "src" / "components"
            component_dir.mkdir(parents=True, exist_ok=True)

            # Generate Vue component with Composition API
            if composition_api:
                component_code = f"""<template>
  <div class="{component_name.lower()}">
    <h2>{{ title }}</h2>
    <p>Welcome to the {component_name} component!</p>
  </div>
</template>

<script setup lang="ts">
import {{ ref }} from 'vue';

interface Props {{
  title?: string;
}}

const props = withDefaults(defineProps<Props>(), {{
  title: '{component_name} Component'
}});

const emit = defineEmits<{{
  click: [value: string];
}}>();

// Component logic here
const handleClick = () => {{
  emit('click', 'Component clicked!');
}};
</script>

{
                    f'''<style scoped>
.{component_name.lower()} {{
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #ffffff;
}}

.{component_name.lower()} h2 {{
  margin-top: 0;
  color: #333;
  font-size: 1.5rem;
}}

.{component_name.lower()} p {{
  color: #666;
  line-height: 1.6;
}}
</style>'''
                    if include_styles
                    else ""
                }
"""

            # Write component file
            component_file = component_dir / f"{component_name}.vue"
            with open(component_file, "w", encoding="utf-8") as f:
                f.write(component_code)

            files_created = [f"src/components/{component_name}.vue"]

            # Generate test file
            if include_tests:
                test_content = f"""import {{ mount }} from '@vue/test-utils';
import {component_name} from '../{component_name}.vue';

describe('{component_name}', () => {{
  it('renders properly', () => {{
    const wrapper = mount({component_name});
    expect(wrapper.text()).toContain('{component_name} Component');
  }});

  it('accepts title prop', () => {{
    const title = 'Custom Title';
    const wrapper = mount({component_name}, {{
      props: {{ title }}
    }});
    expect(wrapper.text()).toContain(title);
  }});
}});
"""

                test_file = component_dir / f"{component_name}.test.ts"
                with open(test_file, "w", encoding="utf-8") as f:
                    f.write(test_content)

                files_created.append(f"src/components/{component_name}.test.ts")

            return {
                "success": True,
                "component_name": component_name,
                "api_style": "Composition API" if composition_api else "Options API",
                "files_created": files_created,
                "features": [
                    "TypeScript support",
                    "Composition API",
                    "Props interface",
                    "Event emitters",
                    "Scoped styles" if include_styles else "No styles",
                    "Test file" if include_tests else "No tests",
                ],
                "import_statement": f"import {component_name} from '@/components/{component_name}.vue';",
                "usage_example": f'<{component_name} title="My Title" @click="handleClick" />',
            }

        except Exception as e:
            logger.error(f"Error generating Vue component: {e}")
            return {"success": False, "error": str(e)}

    @mcp.tool()
    def generate_custom_hook(
        project_path: str, hook_name: str, hook_type: str = "state"
    ) -> Dict[str, Any]:
        """Generate a custom React hook with TypeScript.

        Args:
            project_path: Path to the project directory
            hook_name: Name of the hook (should start with 'use')
            hook_type: Type of hook (state, effect, fetch, storage)
        """
        try:
            path = Path(project_path)

            # Validate hook name
            if not hook_name.startswith("use") or not hook_name[3:4].isupper():
                return {
                    "success": False,
                    "error": "Hook name must start with 'use' followed by PascalCase (e.g., useMyHook)",
                }

            hooks_dir = path / "src" / "hooks"
            hooks_dir.mkdir(parents=True, exist_ok=True)

            # Generate hook based on type
            if hook_type == "state":
                hook_code = f"""import {{ useState, useCallback }} from 'react';

interface {hook_name.capitalize()}State {{
  value: string;
  count: number;
}}

export const {hook_name} = (initialValue: string = '') => {{
  const [state, setState] = useState<{hook_name.capitalize()}State>({{
    value: initialValue,
    count: 0
  }});

  const updateValue = useCallback((newValue: string) => {{
    setState(prev => ({{
      value: newValue,
      count: prev.count + 1
    }}));
  }}, []);

  const reset = useCallback(() => {{
    setState({{
      value: initialValue,
      count: 0
    }});
  }}, [initialValue]);

  return {{
    ...state,
    updateValue,
    reset
  }};
}};
"""

            elif hook_type == "fetch":
                hook_code = f"""import {{ useState, useEffect, useCallback }} from 'react';

interface {hook_name.capitalize()}Options {{
  url: string;
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  headers?: Record<string, string>;
}}

interface {hook_name.capitalize()}State<T> {{
  data: T | null;
  loading: boolean;
  error: string | null;
}}

export const {hook_name} = <T = any>(options: {hook_name.capitalize()}Options) => {{
  const [state, setState] = useState<{hook_name.capitalize()}State<T>>({{
    data: null,
    loading: false,
    error: null
  }});

  const fetchData = useCallback(async () => {{
    setState(prev => ({{ ...prev, loading: true, error: null }}));

    try {{
      const response = await fetch(options.url, {{
        method: options.method || 'GET',
        headers: options.headers
      }});

      if (!response.ok) {{
        throw new Error(`HTTP error! status: ${{response.status}}`);
      }}

      const data = await response.json();
      setState({{ data, loading: false, error: null }});
    }} catch (error) {{
      setState(prev => ({{
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'An error occurred'
      }}));
    }}
  }}, [options.url, options.method, options.headers]);

  useEffect(() => {{
    fetchData();
  }}, [fetchData]);

  return {{
    ...state,
    refetch: fetchData
  }};
}};
"""

            # Write hook file
            hook_file = hooks_dir / f"{hook_name}.ts"
            with open(hook_file, "w", encoding="utf-8") as f:
                f.write(hook_code)

            return {
                "success": True,
                "hook_name": hook_name,
                "hook_type": hook_type,
                "file_created": f"src/hooks/{hook_name}.ts",
                "import_statement": f"import {{ {hook_name} }} from '@/hooks/{hook_name}';",
                "usage_example": f"const {{ /* destructure return values */ }} = {hook_name}(/* parameters */);",
            }

        except Exception as e:
            logger.error(f"Error generating custom hook: {e}")
            return {"success": False, "error": str(e)}


def _is_valid_component_name(name: str) -> bool:
    """Validate component name follows PascalCase convention."""
    import re

    return bool(re.match(r"^[A-Z][a-zA-Z0-9]*$", name))
