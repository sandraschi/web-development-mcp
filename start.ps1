Param([switch]$Headless)
# web-development-mcp Start - fleet standard launcher
# Backend: uvicorn web_sota\backend server:app (:10853) | Frontend: vite (:10852)

$RepoRoot = $PSScriptRoot
$BackendPort = 10853
$FrontendPort = 10852
$BackendDir = Join-Path $RepoRoot "web_sota\backend"
$WebRoot = Join-Path $RepoRoot "web_sota"

Write-Host "Starting web-development-mcp..." -ForegroundColor Cyan

function Clear-Port([int]$Port) {
    $owners = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($pid in $owners) {
        try { Stop-Process -Id $pid -Force -ErrorAction Stop; Write-Host "  cleared zombie PID $pid on :$Port" -ForegroundColor DarkYellow } catch {}
    }
}

Clear-Port $BackendPort
Clear-Port $FrontendPort

# --- Backend (hidden, with explicit WorkingDirectory) ---
$backendArgs = @("-NoProfile", "-Command", "uv run --project '$RepoRoot' uvicorn server:app --host 127.0.0.1 --port $BackendPort --app-dir '$BackendDir'")
$backend = Start-Process pwsh -ArgumentList $backendArgs -WorkingDirectory $BackendDir -WindowStyle Hidden -PassThru
Write-Host "  backend PID $($backend.Id) starting..." -ForegroundColor DarkGray

# --- Readiness: TCP poll (not a fixed sleep) ---
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    try {
        $client = New-Object Net.Sockets.TcpClient
        $iar = $client.BeginConnect("127.0.0.1", $BackendPort, $null, $null)
        if ($iar.AsyncWaitHandle.WaitOne(1000)) {
            $client.EndConnect($iar); $client.Close(); $ready = $true; break
        }
        $client.Close()
    } catch {}
    Start-Sleep -Seconds 2
}
if (-not $ready) { throw "Backend failed to bind 127.0.0.1:$BackendPort after 60s (PID $($backend.Id))" }
Write-Host "  backend ready on :$BackendPort" -ForegroundColor Green

# --- Frontend ---
if ($Headless) {
    Write-Host "  headless mode: frontend skipped" -ForegroundColor DarkGray
    return
}
Start-Process pwsh -ArgumentList @("-NoProfile", "-Command", "npm run dev") -WorkingDirectory $WebRoot
Start-Sleep -Seconds 3
Start-Process "http://localhost:$FrontendPort"
Write-Host "  frontend opening on :$FrontendPort" -ForegroundColor Green
