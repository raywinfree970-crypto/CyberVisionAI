<#
Run a quick smoke test: apply migrations and call the voice AI endpoint with a sample prompt.
This script assumes the virtualenv in the repo root is activated or will activate it for you.

Usage (from project root):
  .\scripts\smoke_test.ps1
#>

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
# repo root is parent of scripts dir
$RepoRoot = Split-Path -Parent $ScriptDir
$VenvActivate = Join-Path $RepoRoot 'venv\Scripts\Activate.ps1'

if (Test-Path $VenvActivate) {
    Write-Host "Activating virtualenv..." -ForegroundColor Cyan
    & powershell -NoProfile -ExecutionPolicy Bypass -Command "& '$VenvActivate'"
} else {
    Write-Host "Virtualenv activate script not found at $VenvActivate. Make sure venv is created and activated." -ForegroundColor Yellow
}

Write-Host "Applying migrations..." -ForegroundColor Cyan
python "$RepoRoot\manage.py" migrate --noinput

Write-Host "Waiting a moment for services to stabilize..." -ForegroundColor Cyan
Start-Sleep -Seconds 1

Write-Host "Running in-process Django smoke test (uses Django test client; no server needed)..." -ForegroundColor Cyan
python "$RepoRoot\scripts\smoke_test.py"

Write-Host "Smoke test finished." -ForegroundColor Green
