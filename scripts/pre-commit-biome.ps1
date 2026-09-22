# Biome pre-commit gate: runs `biome ci` on every web root that exists.
# Called by .pre-commit-config.yaml (local hook, system language).
$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$roots = @("web_sota", "webapp", "webapp/frontend", "web") |
    Where-Object { Test-Path (Join-Path $repoRoot $_) }
if ($roots.Count -eq 0) { Write-Output "pre-commit-biome: no web root found, skipping."; exit 0 }
$failed = $false
foreach ($root in $roots) {
    $dir = Join-Path $repoRoot $root
    Write-Output "pre-commit-biome: biome ci $dir"
    Push-Location $dir
    try { npx @biomejs/biome ci . } catch { $failed = $true } finally { Pop-Location }
}
if ($failed) { Write-Error "pre-commit-biome: violations found — run 'just fix'."; exit 1 }
