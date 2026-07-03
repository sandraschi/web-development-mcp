!macro KillProcesses
  DetailPrint "Stopping processes..."
  ExecWait 'taskkill /F /IM "web-development-mcp-backend.exe" /T' $0
  ExecWait 'taskkill /F /IM "web-development-mcp-native.exe" /T' $0
  Sleep 2000
!macroend

!macro NSIS_HOOK_PREINSTALL
  !insertmacro KillProcesses
!macroend

!macro NSIS_HOOK_PREUNINSTALL
  !insertmacro KillProcesses
!macroend
