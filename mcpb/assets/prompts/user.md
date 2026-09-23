# web-development-mcp - user guide

This guide shows how to use the Web Development MCP server through its 22
tools, its chat proxy, and its dashboard. Every example names real tools
with real arguments. Anything not listed here does not exist: there is no
SvelteKit or Next.js scaffolder, no `configure_eslint`, no `install_deps`,
no `create_project`, and no `run_script`. When this guide says a value is
refused, it means the server returns `{success: false}` with a message you
can act on.

## 1. First run: providers, health, and orientation

Start with orientation, not scaffolding. Call `list_available_frameworks`
and read the `available` flags: React and Vue are scaffoldable, everything
else is described but unavailable. Then call `get_help` with no arguments to
see the five categories, and again with `category="scaffolding"` (or
`package`, `build`, `component`, `sampling`) for the real tool names in that
group. If you use the dashboard, confirm the backend dot is green and the
LLM indicator on the Chat page shows a detected provider. If it says no LLM,
install Ollama and pull any model, or start LM Studio, then reload: the
Chat page discovers providers live on mount. Without a provider, chat
answers 503 with setup instructions - that message is the onboarding check,
not an error to work around. Persist your provider and model choice on the
Settings page; the selection is revalidated against live discovery every
time the page loads, so stale choices never linger.

## 2. Starting a new project

Say you want a React marketing site. Call `create_react_app` with a valid
npm-style name and a target directory: `project_name="acme-site"`,
`target_directory="./projects"`. Leave options at their defaults unless you
have a reason: router and testing on, strict lint on, Prettier on, Husky
off. The tool creates the directory, `package.json`, the source tree, Vite
and TypeScript and Biome configs, and starter components, then returns the
feature list and the three next steps (`cd`, `npm install`, `npm run dev`).
If the directory already exists you get a refusal naming it - pick another
name or remove it yourself; the server never overwrites. Invalid names
(uppercase, spaces, underscores) are refused with the naming rule quoted.

For Vue the shape is identical: `create_vue_app` with the same two required
arguments, plus router, Pinia, and testing options. After either scaffold,
run `analyze_package_json` on the new directory to confirm the survey reads
back what you expect: framework detected, TypeScript present, testing
present. This two-call habit (create, then analyze) catches template drift
early and costs nothing.

If someone asks for SvelteKit, Next.js, or vanilla TypeScript, do not start
creating directories by hand to fake it. Return the refusal the server would
return: those frameworks are flagged unavailable, and the honest answer
names React and Vue as the working alternatives with an offer to proceed.

## 3. Taking over an existing project

Never change a project you have not surveyed. Call `detect_package_manager`
first: it reports every lockfile found and the primary manager by precedence
(bun beats pnpm beats yarn beats npm), plus whether `package.json` exists at
all. An empty directory yields `primary_manager: null` - that tells you to
scaffold instead of installing. Then call `analyze_package_json`: read the
dependency counts, the detected framework and build tool, the TypeScript and
testing flags, and the `issues`, `warnings`, and `potentially_vulnerable`
lists. Outdated React, a missing tsconfig beside an installed TypeScript,
absent testing libraries, and node-sass/request/bower all surface here with
exact messages. Fix what it flags before adding anything new: add the
missing tsconfig via `configure_typescript` rather than hand-writing one,
and treat a vulnerable package as a removal candidate via `remove_packages`
(confirming first, since removal is destructive).

## 4. Installing, updating, and removing packages

Install with `install_packages`, naming the project path, the package list,
and whether they are dev dependencies. Omit `package_manager` to use
detection; pass it explicitly only when the project genuinely uses two
managers (rare, and worth saying so). The tool returns the exact command it
ran and the outcome - quote both when reporting. For updates, prefer
`update_packages` with `check_only=True` first: it returns the outdated map
without touching anything, and that map is the basis for asking which
updates the user actually wants. Then update the named packages (or all)
with `check_only=False`. Removal via `remove_packages` edits `package.json`,
lockfiles, and installed code: always confirm, always name the packages,
and always report the command. Unsupported manager strings are refused with
the manager named - fix the string, do not retry blindly.

## 5. Configuring TypeScript, Vite, Biome, and tests

Configure in dependency order. `configure_typescript` first: strict on,
target `ES2020` unless the project needs otherwise, `include_react` true
for React projects (this switches JSX to `react-jsx` and extends the lib).
It writes `tsconfig.json` with bundler resolution, `@/*` path mapping,
sourcemaps, and the strict family including unused-locals and unused
parameters. Next `configure_vite` with the project's framework and its own
port - never copy a fleet port from another repo into a generated config;
if the user has no port preference, the template default stands, and you
say so. Then `configure_biome` for lint plus format in one file (this
replaces ESLint and Prettier - do not generate both systems for one
project), with strict rules on unless asked otherwise. Finally
`setup_testing_config` for Vitest with JSDOM globals and the Testing
Library setup file. Each tool returns the files it wrote: repeat the
filenames back so the user knows what changed. If a config file already
exists, these tools overwrite it - say that before running them on a
project the user cares about.

## 6. Generating components, hooks, and UI foundations

Generate components after configuration so aliases and JSX settings exist.
`generate_react_component` needs the project path and a PascalCase name;
pass `component_type="functional"` (the default), toggle styles and tests
explicitly rather than assuming, and supply `props_interface` as a
name-to-type map when the component takes props. The tool returns the
created files, the import statement, and a usage example - all three belong
in your reply. Non-PascalCase names are refused with the rule quoted; fix
the name, do not coerce it silently.

`generate_vue_component` is Composition API only: calling it with
`composition_api=False` returns an explicit refusal, and the correct
response is to proceed with the default, not to emulate the Options API by
hand. It writes the single-file component with typed props, emits, scoped
styles, and a test, plus the import and usage lines to quote back.

`generate_custom_hook` accepts exactly four hook types: `state`, `effect`,
`fetch`, and `storage`. Names must start with `use` followed by PascalCase
(`useUserData`, not `useuserdata`). Unknown types are refused by name -
relay the four valid values and ask which behavior the user wants instead
of guessing. The tool returns the file path, import, and a usage sketch.

For UI foundations, `setup_tailwind` installs the packages with the
detected manager and writes the Tailwind config, PostCSS config, and base
CSS, with optional forms, typography, and container-queries plugins named
individually. `setup_shadcn` writes `components.json` and the `cn` utility
and creates the UI directory, returning the exact `npx shadcn@latest add`
command for the follow-up. `scaffold_dashboard` copies the full kit -
sidebar, topbar, help and log modals, view switcher, layout, and optionally
the Ollama chatbot with the model you name - and returns the feature map,
the keyboard shortcuts, and the next steps including `ollama serve`. Run
foundations before components so styles and utilities exist when generated
code imports them.

## 7. Planning multi-step work

For anything spanning two or more tools, call `agentic_workflow_tool` with
the goal in plain language and present the returned plan before executing:
each step names a real tool, argument hints, and a reason. Then execute the
steps as individual tool calls in order. Scaffolding goals start with the
framework list and a create call. Package goals start with detection and
analysis before any install. Configuration goals run TypeScript, then Vite,
then Biome, then testing. Component goals generate first and wire styling
second. If the goal matches nothing, the planner falls back to help plus
the framework list - treat that as a signal to ask a clarifying question
rather than improvising. The plan mode never executes, so there is no risk
in planning first; the risk is in skipping the plan and running steps out
of order. Keep the safety guard on unless the user explicitly approves a
trusted batch, and announce every destructive step (removals, shutdown)
before running it.

## 8. Using chat well

Chat is a proxy, not a model: your message plus the composed system prompt
(skill content first, personality second) goes to the backend, which
forwards it to the detected local provider. Long answers stream token by
token through the NDJSON endpoint with automatic fallback to the
non-streaming call. If streaming stalls, the fallback still completes the
answer; if no provider runs at all, you get the 503 setup message. Choose
personalities deliberately: senior full-stack developer for complete
solutions with both sides of the stack, UI/UX designer for visual and
component architecture, summarizer for brief bullet answers, custom for
your own standing instructions. History persists locally with a 100-message
cap and exports to text; clearing wipes both the view and the stored copy.
Skill content refreshes from the server on page mount, so reinstalling or
editing `skills/*/SKILL.md` changes assistant behavior after a reload.

## 9. Dashboard pages and daily habits

Overview shows live uptime, event counts, and recent backend activity with
loading, error (with retry), and empty states - no sample data anywhere. Use
Tools Lab for guided tool runs, Projects for scaffolds, Component Factory
and Dependency Flow and Build Forge for their domains, Apps Hub for the
fleet registry, Logs for the ring buffer with filtering and export, Inbox
for the warnings-and-errors triage queue, Skills to read the exact
preprompts chat uses, Settings for providers and models, and Help for the
doc index and the full 22-tool table. A healthy daily loop is: Inbox first
(triage anything red), then the work, then Logs export if something needs a
report. The under-hero onboarding cue appears only when no local LLM is
detected and you have not marked yourself onboarded; it links to Settings
and to this guide's first section, and dismissing it persists locally.

## 10. Troubleshooting conversations

When a tool returns `{success: false}`, the `message` is the user-facing
truth: quote it, then act on it. Invalid names and existing directories
need new names, not retries. Missing `package.json` means you are in the
wrong directory or need to scaffold. Unsupported managers or hook types
need the valid value from the message, not another guess. Install and
update failures carry stderr - read it before retrying, and check network
and lockfile state first. Template render failures name the template and
the undefined variable: the usual cause is a hand-added `{{name}}` without
a matching context key (templates render under StrictUndefined) or a JSX
double-brace without `{% raw %}` protection. Chat 503s mean starting Ollama
or LM Studio, not prompt engineering. A red backend dot means checking the
process and the port (`Get-NetTCPConnection -LocalPort 10853`) before
touching any config. And when the goal itself is outside the catalogue -
SvelteKit scaffolds, ESLint generation, script running - say so plainly,
name the closest real capability, and offer it.

## 11. End-to-end scenario: SaaS landing page (React, from zero)

Goal: a marketing site with a pricing table, contact form, and tests.
First `list_available_frameworks` to confirm React is available, then
`create_react_app` with `project_name="acme-site"`, target `./projects`,
defaults on. Run `analyze_package_json` on the result to confirm React 18,
TypeScript, and Vitest read back. Then `generate_react_component` three
times: `PricingTable` with a props interface mapping plan names to feature
lists, `ContactForm` with fields for name, email, and message, and `Hero`
with headline props - styles and tests on for all three. If the design
calls for utility styling, `setup_tailwind` before generating so classes
resolve; for a component library look, `setup_shadcn` and use its next
steps to add button, card, and dialog. Finish with `npm install` and
`npm run dev` from the returned next steps, and verify the dev server port
matches the scaffolded `vite.config.ts` rather than any fleet port you
remember from elsewhere. Total: two survey calls, one scaffold, three
generations, one optional styling baseline - each confirmed before the
next begins.

## 12. End-to-end scenario: brownfield TypeScript migration (Vue)

Goal: bring an old Vue 2 JavaScript project to Vue 3 + strict TypeScript.
Do not scaffold - the directory exists and scaffolding refuses to
overwrite. Start with `detect_package_manager` (note npm versus yarn: the
commands differ downstream) and `analyze_package_json` (expect warnings
about outdated Vue, missing tsconfig, absent testing). Run
`update_packages` with `check_only=True` and read the outdated map before
touching versions. Then `configure_typescript` with strict on (no React
flag for Vue), `configure_vite` with framework vue and the project's
existing dev port, `configure_biome` with framework vue (exhaustive-deps
stays off), and `setup_testing_config` for Vitest. Migrate components one
at a time with `generate_vue_component` as the pattern reference for
Composition API shape, keeping the old files until each replacement
passes. Update in small batches with `update_packages` naming packages
explicitly, and remove dead dependencies with `remove_packages` only after
confirming each name. Quote every command the tools report so the migration
log is reproducible.

## 13. End-to-end scenario: internal ops dashboard with chatbot

Goal: an admin dashboard with log viewing and an Ollama-backed assistant.
Scaffold React first, then `scaffold_dashboard` with the project name and
`with_chatbot=True`, naming the Ollama model the team actually runs
(defaults to a small chat model; override with the `ollama_model`
argument). The tool returns the keyboard shortcuts - repeat them to the
user, since sidebar, help, logs, theme, search, and chatbot all have
chords. Follow the returned next steps exactly: add the listed shadcn
components, copy the example app over `src/App.tsx`, ensure `ollama serve`
runs, then `npm run dev`. Verify the chatbot answers through the backend
proxy (watch the Chat page's LLM indicator), and use the log viewer modal
in the scaffolded app for the same ring-buffer triage the server dashboard
shows under Inbox. If the model feels slow, that is an Ollama-side concern
(model size, GPU offload) - not something any server tool changes.

## 14. Package-manager specifics

npm: `install` / `install --save-dev`, `update` (optionally named),
`outdated --json` for checks, `uninstall` for removal. Yarn: `add` /
`add --dev`, `upgrade`, `outdated --json`, `remove`. Bun: `add` / `add -d`,
`update`, `outdated --json`, `remove`. pnpm: `add` / `add --save-dev`,
`update`, `outdated --json`, `remove`. The tools build these commands from
detection, so passing `package_manager` explicitly is only needed for
multi-manager oddities - and when you do, say why. Timeouts are five
minutes for installs and updates, two for Tailwind and shadcn setup; a
timeout surfaces as a failure with the partial output attached, and the
right response is retrying with a warmer cache or a smaller package set,
not repeating the identical call.

## 15. Generated config reference

The TypeScript config sets `target` (default ES2020), `module esnext` with
bundler resolution, `strict` plus unused-locals, unused-parameters,
implicit-returns, implicit-any, and the strict function/bind/apply family,
`jsx react-jsx` only with the React flag, path mapping `@/*` to `src/*`,
sourcemaps on, emit off, and `src/**/*` included with `node_modules`,
`dist`, and `build` excluded. The Biome config enables organize-imports,
recommended rules, useless-fragment errors, React exhaustive-deps as a
warning, non-null assertions off, console as warning, strict unused
variables under the strict flag, two-space formatting at width 100, and
single-quote semicolon JavaScript style. The Vite config wires the
framework plugin, the dev server (port, open, optional HTTPS, host), the
`@` alias, `dist` output with sourcemaps and vendor/router manual chunks,
CSS dev sourcemaps, and dependency optimization for the framework. The
Vitest config sets JSDOM, the setup file, globals, and the same alias.
When a project misbehaves, compare its files against this reference before
assuming a tool bug: most surprises are a flipped strict flag, a wrong
port, or a missing alias.

## 16. Component and hook recipes

A pricing table takes a props interface of plan names to string arrays and
renders one card per plan with the shared Button. A data-fetching hook
uses the `fetch` type with a URL option and loading/error state in the
template. A theme toggle uses the `storage` type so the choice persists.
A form field group uses the `state` type with value plus count metadata.
An analytics page view uses the `effect` type with the tracking call in
the effect body. In every case the tool returns the file path, the import
line, and a usage sketch: paste all three into your answer so the user can
wire the piece without asking a follow-up. Keep component names PascalCase
and hook names `use`-prefixed; the validators reject anything else with
the rule quoted, and renaming is always preferable to working around the
validator.

## 17. Glossary of tool messages

"2 of 5 frameworks scaffoldable" orients every greenfield discussion.
"Detected package manager: X" grounds every install. "No package.json in
..." means wrong directory or scaffold first. "Update check via X" versus
"Updated ... with X" distinguishes dry runs from mutations - never confuse
them in reports. "Installed ... with X" and "Removed ... with X" quote the
command alongside. "Wrote tsconfig.json/vite.config.ts/Biome/testing
config" names strictness, framework, and port as applicable. "Generated
React/Vue component/hook ..." names the files. "Planned N steps for: ..."
precedes execution, never replaces it. "Safety Guard enabled/disabled"
reflects real session state. "Shutting down in ..." precedes process exit.
"No local LLM detected ..." is a setup instruction, not a failure. "Only
the Composition API ..." and "Unsupported hook_type ..." name the valid
values. Treat each message as load-bearing text: quote, then act.

## 18. Providers, models, and discovery deep-dive

`GET /api/llm/discover` and `/api/llm/providers` return the same provider
array: Ollama and LM Studio with live `detected` booleans from sub-second
TCP probes, plus OpenAI and Anthropic with `configured` booleans derived
from server environment presence. The Settings page renders one card per
provider with a green detected/configured dot or a gray not-found dot, a
matching dropdown, and a model dropdown fed by `GET /api/llm/models`:
Ollama lists live from `/api/tags` when reachable, otherwise a flagged
curated fallback; LM Studio and cloud providers return flagged guidance
instead of invented lists. Selection persists under `llm_provider` and
`llm_model` and is revalidated on every page load, so a model removed from
Ollama falls back to the first available name rather than lingering.
`/api/llm/onboarding` packages the starter facts (what each local provider
is, where it listens, that cloud needs server-side keys) with the detected
list and the recommended first pick. When nothing is detected, the honest
UI states are "not found" cards, an empty model message pointing at
`docs/ONBOARDING.md`, and the dashboard's red onboarding cue - never a
pretend model name marked ready.

## 19. Dashboard page tour

Overview: live uptime, event totals, backend PID, and the five most recent
ring-buffer entries, with loading, error-with-retry, and empty states.
Projects, Components, Packages, Build: domain workspaces for scaffolds,
generation, dependencies, and pipelines. Chat: the proxy UI with streaming,
personalities, skill preprompting, history cap, export, and clear. Apps
Hub: the fleet registry view. Tools Lab (Control): guided dynamic tool
runs. Settings: infrastructure fields plus the full provider/model UI from
section 18. Logs: the ring buffer with level, kind, and text filters plus
JSON/CSV export and clearing. Inbox: warnings and errors only, newest
first, as the triage queue - start every session here. Skills: the exact
`SKILL.md` contents the chat preprompt is built from, one expandable card
per skill. Help: the five doc summaries with repo-relative paths and the
full 22-tool table mirroring `glama.json`. Every page handles the backend
being down with an explicit error card and retry, and every fetch honors
the same `VITE_API_TARGET` base.

## 20. Keyboard habits and power patterns

Prefer `just certify` (ruff, format check, pyright, pytest) before calling
any scaffold work done, and `just lint`/`just fix` for the webapp alongside
`tsc --noEmit`. Keep recipe bodies single-line with absolute paths, since
the runner spawns one process per line. Stage and commit in batches of at
most five files with honest conventional messages; keep `.env`, `*.bak`
variants, `reports/`, and database files out of every commit. Read the
fleet port registry before allocating anything, and never hardcode another
repo's port into generated configs. When the Inbox is red, triage before
building. When a tool message surprises you, re-read sections 10 and 17
before retrying. And when the goal outgrows the catalogue, say which tool
is missing rather than stretching one that exists: that feedback is how
the catalogue grows.

## 21. Migrating and upgrading existing projects

Switching package managers starts with detection, then a fresh install
under the new manager, then deleting the old lockfile by hand (no tool
deletes lockfiles for you - say so). Bumping React majors means updating
the package, re-running `configure_typescript` to keep JSX settings
aligned, and regenerating one component to confirm the template output
still compiles. Adopting Biome over an existing ESLint setup means running
`configure_biome`, deleting the old ESLint and Prettier configs yourself,
and running the formatter once across the project to normalize style in a
single reviewable commit. Ramping strictness (turning strict mode on in an
old codebase) surfaces unused locals, implicit anys, and missing return
paths as a wave: fix them file by file with the compiler output as the
checklist rather than loosening the config to silence it. Each migration
step ends with the test suite green before the next begins, and
`update_packages` with explicit package names beats blind full upgrades
when the changelog of any major dependency mentions breaking changes.
Treat lockfiles as reviewable artifacts in every migration: after any
install, update, or removal, the lockfile diff should show exactly the
packages you intended plus their transitive closure, and nothing else. A
lockfile that churns hundreds of lines for a one-package change signals a
manager mismatch (installing with npm in a yarn project, for example) -
stop, confirm detection output, and redo the operation under the right
manager rather than committing the churn. Commit the lockfile with the
code change it belongs to, so every install remains reproducible.

## 22. When scaffold output surprises you

Scaffolded projects currently ship without `biome.json` and `.gitignore`
because those upstream templates do not exist yet - run `configure_biome`
right after scaffolding and add your own ignore file rather than assuming
they were forgotten. With `router: false` you get components but no pages
directory, by design: the pages, Home, About, and Layout outputs are the
router's. The `prettier` and `husky` flags only affect the feature list and
follow-up steps, not the file tree. The `App.tsx` title renders your
project name through the template context; if it shows a placeholder
instead, the context injection regressed and the scaffold function needs
the `project_name` key restored. Vue output has no Pages concept beyond
views and stores - do not look for a React-shaped tree. And if generated
code references an alias or component that does not resolve, check that
configuration ran before generation: aliases come from the Vite and TS
configs, and generating first is the usual cause.

## 23. Asking for help effectively

Good requests name four things: the project path, the package manager in
use, the exact tool call (with arguments) that misbehaved, and the full
returned message. "Install failed in D:/shop (npm)" plus the pasted
`install_packages` result beats any paragraph of symptoms, because the
message already contains the command and the stderr. Include what you
already ran - detection output, analysis output, prior successful steps -
so redundant calls are skipped and the real divergence is visible. For
scaffolding surprises, add the options map you passed and the resulting
file tree (even abbreviated): router-off versus router-on explains most
missing-directory confusion, and the options map settles it instantly. For
chat problems, note the personality selected, whether the LLM indicator
showed detected, and whether streaming or fallback answered: those three
facts separate provider outages from proxy bugs from prompt issues. For
dashboard oddities, note the page, the backend status dot, and any Inbox
entries from the same minute - the ring buffer usually already recorded
the cause. And when requesting something the catalogue lacks, describe the
outcome you want rather than the tool you imagine: "a SvelteKit starter"
is actionable feedback about coverage, while "a tool that does X like
`install_deps` would" cites something that never existed and sends the
search down a false trail.
