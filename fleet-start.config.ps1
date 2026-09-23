# Per-repo fleet start config for web-development-mcp
# Edit ports/backend target here - start.ps1 is fleet-standard.
@{
    Name         = 'web-development-mcp'
    BackendPort  = 10853
    FrontendPort = 10852
    HealthPath   = '/health'
    WebRoot      = 'web_sota'
    Backend = @{
        Kind          = 'uvicorn-web-app'
        UvicornTarget = 'server:app'
        WorkDir       = 'web_sota\backend'
        SyncExtras    = @('dev')
        Env           = @{ WEB_PORT = '10853' }
    }
    Frontend = @{
        Kind           = 'vite-npm'
        PackageManager = 'npm'
        PortEnvVar     = 'VITE_PORT'
        ApiTargetEnv   = 'VITE_API_TARGET'
    }
}
