# Biome pre-commit gate: runs `biome ci` on the COMMITTED files that live
# under a web root (args come from pre-commit's pass_filenames). Scoped to
# changed files so pre-existing dirt elsewhere never blocks a commit.
$repoRoot = Split-Path -Parent $PSScriptRoot
$webRoots = @("web_sota", "webapp", "webapp/frontend", "web") | Where-Object {
    Test-Path (Join-Path $repoRoot $_)
}
if ($webRoots.Count -eq 0) { exit 0 }

$byRoot = @{}
foreach ($f in $args) {
    $full = $f
    if (-not [System.IO.Path]::IsPathRooted($full)) { $full = Join-Path (Get-Location).Path $full }
    if ($full -notmatch "\.(ts|tsx|js|jsx|json)$") { continue }
    foreach ($root in $webRoots) {
        $dir = Join-Path $repoRoot $root
        if ($full.StartsWith($dir, [StringComparison]::OrdinalIgnoreCase)) {
            if (-not $byRoot.ContainsKey($dir)) { $byRoot[$dir] = @() }
            $byRoot[$dir] += $full
            break
        }
    }
}
if ($byRoot.Count -eq 0) { exit 0 }

$failed = $false
foreach ($dir in $byRoot.Keys) {
    Push-Location $dir
    try {
        npx @biomejs/biome ci $byRoot[$dir]
        if ($LASTEXITCODE -ne 0) { $failed = $true }
    } finally { Pop-Location }
}
if ($failed) { Write-Error "pre-commit-biome: violations - run 'just fix'."; exit 1 }
exit 0
