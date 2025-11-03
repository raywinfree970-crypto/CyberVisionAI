# Build an executable of the desktop launcher using PyInstaller

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $RepoRoot

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Cyan
    pip install pyinstaller
}

Write-Host "Creating build directory..." -ForegroundColor Cyan

# Build with one-folder to avoid missing template/static files. The produced folder will contain the exe and supporting files.
pyinstaller --noconfirm --onedir --name CyberVisionAI_Desktop desktop_app.py

Write-Host "Build complete. See the 'dist\\CyberVisionAI_Desktop' folder. Copy the entire folder to distribute (templates/static/media should remain alongside the exe)." -ForegroundColor Green
