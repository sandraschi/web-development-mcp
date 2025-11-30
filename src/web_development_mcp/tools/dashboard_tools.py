"""
Dashboard scaffolding tools for web-development-mcp.

Provides tools for creating modern admin dashboards with:
- Tailwind CSS setup
- shadcn/ui components
- Collapsible sidebar + topbar layout
- Theme toggle (dark/light)
- SOTA modals (help, logview)
- Card/list view switcher
- Popup chatbot with Ollama integration
"""

import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def setup_tailwind(
    project_path: str,
    with_forms: bool = True,
    with_typography: bool = True,
    with_container_queries: bool = False
) -> Dict[str, Any]:
    """Set up Tailwind CSS in an existing project.
    
    Args:
        project_path: Path to the project directory
        with_forms: Include @tailwindcss/forms plugin
        with_typography: Include @tailwindcss/typography plugin
        with_container_queries: Include @tailwindcss/container-queries plugin
        
    Returns:
        Dictionary with setup results
    """
    try:
        path = Path(project_path)
        
        # Install Tailwind and dependencies
        packages = ["tailwindcss", "postcss", "autoprefixer"]
        if with_forms:
            packages.append("@tailwindcss/forms")
        if with_typography:
            packages.append("@tailwindcss/typography")
        if with_container_queries:
            packages.append("@tailwindcss/container-queries")
        
        # Detect package manager
        if (path / "pnpm-lock.yaml").exists():
            cmd = ["pnpm", "add", "-D"] + packages
        elif (path / "yarn.lock").exists():
            cmd = ["yarn", "add", "-D"] + packages
        else:
            cmd = ["npm", "install", "-D"] + packages
        
        result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            return {"success": False, "error": result.stderr}
        
        # Create tailwind.config.js
        plugins = []
        if with_forms:
            plugins.append("require('@tailwindcss/forms')")
        if with_typography:
            plugins.append("require('@tailwindcss/typography')")
        if with_container_queries:
            plugins.append("require('@tailwindcss/container-queries')")
        
        tailwind_config = f"""/** @type {{import('tailwindcss').Config}} */
export default {{
  content: [
    "./index.html",
    "./src/**/*.{{js,ts,jsx,tsx,vue,svelte}}",
  ],
  darkMode: 'class',
  theme: {{
    extend: {{
      colors: {{
        sidebar: {{
          DEFAULT: 'hsl(var(--sidebar-background))',
          foreground: 'hsl(var(--sidebar-foreground))',
          primary: 'hsl(var(--sidebar-primary))',
          'primary-foreground': 'hsl(var(--sidebar-primary-foreground))',
          accent: 'hsl(var(--sidebar-accent))',
          'accent-foreground': 'hsl(var(--sidebar-accent-foreground))',
          border: 'hsl(var(--sidebar-border))',
          ring: 'hsl(var(--sidebar-ring))',
        }},
      }},
      keyframes: {{
        'slide-in-right': {{
          '0%': {{ transform: 'translateX(100%)' }},
          '100%': {{ transform: 'translateX(0)' }},
        }},
        'slide-out-right': {{
          '0%': {{ transform: 'translateX(0)' }},
          '100%': {{ transform: 'translateX(100%)' }},
        }},
        'fade-in': {{
          '0%': {{ opacity: '0' }},
          '100%': {{ opacity: '1' }},
        }},
      }},
      animation: {{
        'slide-in-right': 'slide-in-right 0.3s ease-out',
        'slide-out-right': 'slide-out-right 0.3s ease-in',
        'fade-in': 'fade-in 0.2s ease-out',
      }},
    }},
  }},
  plugins: [{', '.join(plugins)}],
}}
"""
        (path / "tailwind.config.js").write_text(tailwind_config)
        
        # Create postcss.config.js
        postcss_config = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
        (path / "postcss.config.js").write_text(postcss_config)
        
        # Create/update src/index.css with Tailwind directives
        css_path = path / "src" / "index.css"
        css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
    
    /* Sidebar */
    --sidebar-background: 0 0% 98%;
    --sidebar-foreground: 240 5.3% 26.1%;
    --sidebar-primary: 240 5.9% 10%;
    --sidebar-primary-foreground: 0 0% 98%;
    --sidebar-accent: 240 4.8% 95.9%;
    --sidebar-accent-foreground: 240 5.9% 10%;
    --sidebar-border: 220 13% 91%;
    --sidebar-ring: 217.2 91.2% 59.8%;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
    
    /* Sidebar dark */
    --sidebar-background: 240 5.9% 10%;
    --sidebar-foreground: 240 4.8% 95.9%;
    --sidebar-primary: 224.3 76.3% 48%;
    --sidebar-primary-foreground: 0 0% 100%;
    --sidebar-accent: 240 3.7% 15.9%;
    --sidebar-accent-foreground: 240 4.8% 95.9%;
    --sidebar-border: 240 3.7% 15.9%;
    --sidebar-ring: 217.2 91.2% 59.8%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
"""
        css_path.parent.mkdir(parents=True, exist_ok=True)
        css_path.write_text(css_content)
        
        return {
            "success": True,
            "project_path": str(project_path),
            "packages_installed": packages,
            "files_created": [
                "tailwind.config.js",
                "postcss.config.js", 
                "src/index.css"
            ],
            "plugins": {
                "forms": with_forms,
                "typography": with_typography,
                "container_queries": with_container_queries
            }
        }
        
    except Exception as e:
        logger.error(f"Error setting up Tailwind: {e}")
        return {"success": False, "error": str(e)}


def setup_shadcn(
    project_path: str,
    components: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Initialize shadcn/ui in a React/Next.js project.
    
    Args:
        project_path: Path to the project directory
        components: List of components to install (default: button, card, dialog, dropdown-menu)
        
    Returns:
        Dictionary with setup results
    """
    try:
        path = Path(project_path)
        
        if components is None:
            components = ["button", "card", "dialog", "dropdown-menu", "input", "label", "separator", "sheet", "tabs", "tooltip"]
        
        # Create components.json for shadcn
        components_json = {
            "$schema": "https://ui.shadcn.com/schema.json",
            "style": "default",
            "rsc": False,
            "tsx": True,
            "tailwind": {
                "config": "tailwind.config.js",
                "css": "src/index.css",
                "baseColor": "slate",
                "cssVariables": True,
                "prefix": ""
            },
            "aliases": {
                "components": "@/components",
                "utils": "@/lib/utils"
            }
        }
        
        (path / "components.json").write_text(json.dumps(components_json, indent=2))
        
        # Create lib/utils.ts
        utils_dir = path / "src" / "lib"
        utils_dir.mkdir(parents=True, exist_ok=True)
        
        utils_ts = '''import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
'''
        (utils_dir / "utils.ts").write_text(utils_ts)
        
        # Install clsx and tailwind-merge
        if (path / "pnpm-lock.yaml").exists():
            cmd = ["pnpm", "add", "clsx", "tailwind-merge", "class-variance-authority", "lucide-react"]
        elif (path / "yarn.lock").exists():
            cmd = ["yarn", "add", "clsx", "tailwind-merge", "class-variance-authority", "lucide-react"]
        else:
            cmd = ["npm", "install", "clsx", "tailwind-merge", "class-variance-authority", "lucide-react"]
        
        subprocess.run(cmd, cwd=project_path, capture_output=True, text=True, timeout=120)
        
        # Create components directory
        components_dir = path / "src" / "components" / "ui"
        components_dir.mkdir(parents=True, exist_ok=True)
        
        return {
            "success": True,
            "project_path": str(project_path),
            "files_created": [
                "components.json",
                "src/lib/utils.ts"
            ],
            "components_dir": str(components_dir),
            "next_steps": [
                "Run: npx shadcn@latest add " + " ".join(components),
                "Or manually add components from https://ui.shadcn.com/docs/components"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error setting up shadcn: {e}")
        return {"success": False, "error": str(e)}


def scaffold_dashboard(
    project_path: str,
    project_name: str = "dashboard",
    with_chatbot: bool = True,
    ollama_model: str = "llama3.2:3b"
) -> Dict[str, Any]:
    """Scaffold a complete admin dashboard with all features.
    
    Creates a modern dashboard with:
    - Collapsible sidebar navigation
    - Topbar with theme toggle and user menu
    - Help modal with keyboard shortcuts
    - Log viewer modal
    - Card/list view switcher
    - Popup chatbot with Ollama integration
    
    Args:
        project_path: Path to the project directory (must have React + Tailwind)
        project_name: Name for the dashboard
        with_chatbot: Include the Ollama chatbot component
        ollama_model: Default Ollama model for chatbot
        
    Returns:
        Dictionary with scaffold results
    """
    try:
        path = Path(project_path)
        templates_dir = Path(__file__).parent.parent / "templates" / "dashboard"
        
        # Create dashboard components directory
        dashboard_dir = path / "src" / "components" / "dashboard"
        dashboard_dir.mkdir(parents=True, exist_ok=True)
        
        # List of components to copy
        components = [
            "Sidebar.tsx",
            "Topbar.tsx",
            "HelpModal.tsx",
            "LogViewModal.tsx",
            "ViewSwitcher.tsx",
            "DashboardLayout.tsx",
        ]
        
        if with_chatbot:
            components.append("Chatbot.tsx")
        
        files_created = []
        
        for component in components:
            template_file = templates_dir / f"{component}.template"
            if template_file.exists():
                content = template_file.read_text(encoding='utf-8')
                
                # Replace placeholders if needed
                content = content.replace("llama3.2:3b", ollama_model)
                
                output_file = dashboard_dir / component
                output_file.write_text(content, encoding='utf-8')
                files_created.append(f"src/components/dashboard/{component}")
        
        # Create an index.ts for easy imports
        index_content = """// Dashboard components
export { Sidebar } from './Sidebar';
export { Topbar } from './Topbar';
export { HelpModal } from './HelpModal';
export { LogViewModal } from './LogViewModal';
export { ViewSwitcher, DataCard, DataListItem, DataView, type ViewMode } from './ViewSwitcher';
export { DashboardLayout } from './DashboardLayout';
"""
        if with_chatbot:
            index_content += "export { Chatbot } from './Chatbot';\n"
        
        (dashboard_dir / "index.ts").write_text(index_content)
        files_created.append("src/components/dashboard/index.ts")
        
        # Create example App.tsx
        app_example = f'''import {{ useState }} from 'react';
import {{ DashboardLayout }} from '@/components/dashboard';
import {{ ViewSwitcher, DataView, DataCard, DataListItem, type ViewMode }} from '@/components/dashboard';
import {{ Users, DollarSign, Activity, TrendingUp }} from 'lucide-react';

interface StatItem {{
  id: string;
  title: string;
  value: string;
  trend: {{ value: number; isPositive: boolean }};
  icon: React.ReactNode;
}}

function App() {{
  const [view, setView] = useState<ViewMode>('card');

  const stats: StatItem[] = [
    {{ id: '1', title: 'Total Users', value: '12,543', trend: {{ value: 12.5, isPositive: true }}, icon: <Users className="h-5 w-5" /> }},
    {{ id: '2', title: 'Revenue', value: '$45,231', trend: {{ value: 8.2, isPositive: true }}, icon: <DollarSign className="h-5 w-5" /> }},
    {{ id: '3', title: 'Active Sessions', value: '1,234', trend: {{ value: -3.1, isPositive: false }}, icon: <Activity className="h-5 w-5" /> }},
    {{ id: '4', title: 'Growth Rate', value: '23.5%', trend: {{ value: 4.3, isPositive: true }}, icon: <TrendingUp className="h-5 w-5" /> }},
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">{project_name}</h1>
            <p className="text-muted-foreground">Welcome back! Here's your overview.</p>
          </div>
          <ViewSwitcher view={{view}} onViewChange={{setView}} />
        </div>

        <DataView
          data={{stats}}
          view={{view}}
          cardGridCols={{4}}
          renderCard={{(item) => (
            <DataCard
              key={{item.id}}
              title={{item.title}}
              value={{item.value}}
              trend={{item.trend}}
              icon={{item.icon}}
            />
          )}}
          renderListItem={{(item) => (
            <DataListItem
              key={{item.id}}
              title={{item.title}}
              value={{item.value}}
              icon={{item.icon}}
              status={{{{ label: item.trend.isPositive ? 'Up' : 'Down', variant: item.trend.isPositive ? 'success' : 'error' }}}}
            />
          )}}
        />
      </div>
    </DashboardLayout>
  );
}}

export default App;
'''
        
        example_dir = path / "src" / "examples"
        example_dir.mkdir(parents=True, exist_ok=True)
        (example_dir / "DashboardApp.tsx").write_text(app_example)
        files_created.append("src/examples/DashboardApp.tsx")
        
        return {
            "success": True,
            "project_path": str(project_path),
            "project_name": project_name,
            "files_created": files_created,
            "features": {
                "sidebar": "Collapsible sidebar with navigation",
                "topbar": "Topbar with search, theme toggle, notifications, user menu",
                "help_modal": "Help center with keyboard shortcuts and documentation",
                "log_viewer": "Real-time log viewer with filtering and export",
                "view_switcher": "Card/list view toggle with DataCard and DataListItem",
                "chatbot": with_chatbot,
                "ollama_model": ollama_model if with_chatbot else None,
            },
            "keyboard_shortcuts": {
                "Cmd/Ctrl + B": "Toggle sidebar",
                "Cmd/Ctrl + /": "Open help",
                "Cmd/Ctrl + .": "Toggle theme",
                "Cmd/Ctrl + L": "Open logs",
                "Cmd/Ctrl + K": "Open search",
                "Cmd/Ctrl + J": "Open chatbot",
            },
            "next_steps": [
                "Install shadcn components: npx shadcn@latest add button card dialog dropdown-menu input label separator sheet tabs tooltip scroll-area select badge",
                "Copy src/examples/DashboardApp.tsx to src/App.tsx",
                "Start Ollama if using chatbot: ollama serve",
                "Run: npm run dev",
            ]
        }
        
    except Exception as e:
        logger.error(f"Error scaffolding dashboard: {e}")
        return {"success": False, "error": str(e)}


def register_tools(mcp):
    """Register dashboard tools with the MCP server."""
    mcp.tool()(setup_tailwind)
    mcp.tool()(setup_shadcn)
    mcp.tool()(scaffold_dashboard)
    
    logger.info("Dashboard tools registered successfully")

