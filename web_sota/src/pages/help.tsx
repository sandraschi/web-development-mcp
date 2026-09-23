import { LifeBuoy } from "lucide-react";

const DOCS: { name: string; path: string; about: string }[] = [
  {
    name: "ONBOARDING",
    path: "docs/ONBOARDING.md",
    about:
      "Start here: LLM setup (Ollama/LM Studio/cloud keys), sanity checks, pitfalls.",
  },
  {
    name: "TOOLS",
    path: "docs/TOOLS.md",
    about: "All 22 MCP tools with arguments and effects.",
  },
  {
    name: "CONFIGURATION",
    path: "docs/CONFIGURATION.md",
    about: "Env vars, ports (10852/10853), transports, CORS rules.",
  },
  {
    name: "TROUBLESHOOTING",
    path: "docs/TROUBLESHOOTING.md",
    about: "Backend unreachable, 503 chat, template errors, push rejected.",
  },
  {
    name: "DEVELOPMENT",
    path: "docs/DEVELOPMENT.md",
    about: "Recipes, testing, docstring/return conventions, commit rules.",
  },
];

const TOOLS: { name: string; what: string }[] = [
  {
    name: "list_available_frameworks",
    what: "Framework catalogue (react/vue work)",
  },
  { name: "create_react_app", what: "Scaffold React+TS+Vite" },
  { name: "create_vue_app", what: "Scaffold Vue 3+TS+Vite" },
  { name: "detect_package_manager", what: "Lockfile detection" },
  { name: "install_packages", what: "Real install subprocess" },
  { name: "update_packages", what: "Update or check-only report" },
  { name: "remove_packages", what: "Uninstall (destructive)" },
  { name: "analyze_package_json", what: "Dep analysis + vuln flags" },
  { name: "configure_typescript", what: "Write tsconfig.json" },
  { name: "configure_biome", what: "Write biome.json" },
  { name: "configure_vite", what: "Write vite.config.ts" },
  { name: "setup_testing_config", what: "Vitest + Testing Library" },
  { name: "generate_react_component", what: "Component + styles + tests" },
  { name: "generate_vue_component", what: "Vue SFC (Composition API)" },
  { name: "generate_custom_hook", what: "React hook (4 types)" },
  { name: "setup_tailwind", what: "Tailwind baseline" },
  { name: "setup_shadcn", what: "shadcn/ui baseline" },
  { name: "scaffold_dashboard", what: "Full dashboard scaffold" },
  {
    name: "agentic_workflow_tool",
    what: "Deterministic plan (executes nothing)",
  },
  { name: "toggle_safety_guard", what: "Session guard state" },
  { name: "shutdown_server", what: "Graceful exit" },
  { name: "get_help", what: "Help by category" },
];

export function Help() {
  return (
    <div className="space-y-6" data-testid="help-page">
      <header>
        <h2 className="text-2xl font-bold tracking-tight text-white flex items-center gap-3">
          <LifeBuoy className="h-7 w-7 text-emerald-500" />
          Help
        </h2>
        <p className="mt-2 text-sm text-slate-300">
          Docs live in the repo (paths below are relative to the repo root).
          Tool list mirrors <code>glama.json</code> and{" "}
          <code>docs/TOOLS.md</code>.
        </p>
      </header>

      <section className="space-y-2">
        <h3 className="text-lg font-semibold text-slate-200">Documents</h3>
        {DOCS.map((d) => (
          <div
            key={d.path}
            className="rounded border border-slate-800 bg-slate-950/50 p-3"
          >
            <p className="text-sm font-medium text-slate-200">
              {d.name}{" "}
              <span className="font-mono text-slate-300">{d.path}</span>
            </p>
            <p className="text-sm text-slate-300">{d.about}</p>
          </div>
        ))}
      </section>

      <section className="space-y-2">
        <h3 className="text-lg font-semibold text-slate-200">MCP tools (22)</h3>
        <div className="overflow-x-auto rounded border border-slate-800">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-800 text-slate-300">
                <th className="px-3 py-2 font-medium">Tool</th>
                <th className="px-3 py-2 font-medium">What it does</th>
              </tr>
            </thead>
            <tbody>
              {TOOLS.map((t) => (
                <tr
                  key={t.name}
                  className="border-b border-slate-800 last:border-0"
                >
                  <td className="px-3 py-2 font-mono text-slate-200">
                    {t.name}
                  </td>
                  <td className="px-3 py-2 text-slate-300">{t.what}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
