# Create a desktop shortcut to start_app.ps1
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$startScript = Join-Path $RepoRoot 'start_app.ps1'
if (-Not (Test-Path $startScript)) {
    Write-Host "start_app.ps1 not found at $startScript" -ForegroundColor Red
    exit 1
}

$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath('Desktop')
$ShortcutPath = Join-Path $Desktop 'CyberVisionAI.lnk'
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = 'powershell.exe'
$Shortcut.Arguments = "-NoExit -ExecutionPolicy Bypass -File `"$startScript`""
$Shortcut.WorkingDirectory = $RepoRoot
$Shortcut.WindowStyle = 1
$Shortcut.IconLocation = "$startScript,0"
$Shortcut.Save()
Write-Host "Shortcut created at $ShortcutPath" -ForegroundColor Green
