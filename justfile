set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]
import 'scripts/just/fleet.just'

REPO := justfile_directory()

# --- Dashboard ---

# Open the interactive recipe dashboard in the browser
default:
    @just --list

# --- Serve ---

# Launch the full stack (uvicorn backend :10853 + vite frontend :10852)
serve:
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "{{REPO}}\start.ps1"

# --- Quality ---

# Execute Ruff lint + format check + Biome CI (single-line bodies: just runs
# each recipe LINE as its own process, so all paths are absolute — no
# Set-Location, no cwd assumptions)
lint:
    uv run ruff check "{{REPO}}"; uv run ruff format --check "{{REPO}}"; npx @biomejs/biome ci "{{REPO}}\web_sota"

# Execute Ruff fix + formatting + Biome write
fix:
    uv run ruff check "{{REPO}}" --fix --unsafe-fixes; uv run ruff format "{{REPO}}"; npx @biomejs/biome check --write "{{REPO}}\web_sota"

# Format only (ruff + biome)
fmt:
    uv run ruff format "{{REPO}}"; npx @biomejs/biome check --write "{{REPO}}\web_sota"

# Run the Python test suite
test:
    uv run pytest "{{REPO}}\tests" -q

# Full local gate: lint + types + tests (mirrors CI)
certify:
    uv run ruff check "{{REPO}}"; uv run ruff format --check "{{REPO}}"; uv run pyright "{{REPO}}\src"; uv run pytest "{{REPO}}\tests" -q

# Browser walk of the running webapp (needs `just serve` first)
e2e:
    powershell.exe -NoProfile -File "{{REPO}}\scripts\just\cua-webapp-test.ps1"

# --- Hardening ---

# Execute Bandit security audit
check-sec:
    uv run bandit -r "{{REPO}}\src"

# Execute safety audit of dependencies
audit-deps:
    uv run safety check

# --- Tauri NSIS ---

# Build the PyInstaller backend .exe and copy to Tauri resources
build-sidecar:
    powershell.exe -NoProfile -File native\build-sidecar.ps1

# Build the Tauri NSIS desktop installer (full pipeline: frontend -> sidecar -> Rust -> NSIS)
build-native: build-sidecar
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"; $vcvars = "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"; $envOutput = cmd /c "`"$vcvars`" > nul & set" | Where-Object { $_ -match '^(INCLUDE|LIB|LIBPATH|VCToolsVersion|WindowsSdkDir|UniversalCRTSdkDir|UCRTVersion)=' }; foreach ($line in $envOutput) { $parts = $line.Split('=', 2); Set-Item -Path "env:$($parts[0])" -Value $parts[1] -ErrorAction SilentlyContinue }; Set-Location '{{justfile_directory()}}\native'; npx @tauri-apps/cli build --bundles nsis


# Bootstrap: install dev deps + pre-commit hook
bootstrap:
    uv sync --group dev; uv run pre-commit install; Write-Host "Pre-commit hooks installed." -ForegroundColor Green
