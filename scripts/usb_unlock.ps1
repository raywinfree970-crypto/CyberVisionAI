<#
PowerShell wrapper to interactively check a USB unlock key.

This prompts for a drive letter and a secure password, then calls the Python `check_usb.py` script.
If successful, it writes the token to `.cybervision_unlock_token` in the repo root (secure file) so other scripts can pick it up.
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot = Split-Path -Parent $ScriptDir

Write-Host "Enter drive letter (example: D) or full path to USB root:" -ForegroundColor Cyan
$drive = Read-Host
if ($drive -match '^[A-Za-z]$') { $drive = $drive + ':' }

Write-Host "Enter password for USB key:" -ForegroundColor Cyan
$secure = Read-Host -AsSecureString
$bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
$password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
[System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)

$py = Join-Path $RepoRoot 'venv\Scripts\python.exe'
if (-not (Test-Path $py)) { $py = 'python' }

try {
    $out = & $py "$RepoRoot\scripts\check_usb.py" --drive $drive --password $password 2>&1
    if ($LASTEXITCODE -ne 0) { Write-Host $out; exit 1 }
    # capture token line
    $tokenLine = $out | Select-String 'Token:' | ForEach-Object { $_.ToString().Split('Token:')[1].Trim() }
    if ($tokenLine) {
        $tokenFile = Join-Path $RepoRoot '.cybervision_unlock_token'
        $tokenLine | Out-File -FilePath $tokenFile -Encoding utf8
        Write-Host "Unlock token saved to: $tokenFile" -ForegroundColor Green
    } else {
        Write-Host $out
        Write-Host "No token captured." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error during unlock: $_" -ForegroundColor Red
}
