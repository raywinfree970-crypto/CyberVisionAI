# Start the CyberVisionAI app from the repo root.
# Opens separate PowerShell windows for the Django server and Celery worker and opens the browser.

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
# Repo root is the parent of the scripts directory
$RepoRoot = Split-Path -Parent $ScriptDir
$VenvActivate = Join-Path $RepoRoot 'venv\Scripts\Activate.ps1'

if (-Not (Test-Path $VenvActivate)) {
    Write-Host "Virtualenv activate script not found at $VenvActivate" -ForegroundColor Yellow
    exit 1
}

# Start Django runserver in a new window
$runserverCmd = "& `'$VenvActivate`'; python `"$RepoRoot\manage.py`" runserver 0.0.0.0:8000"
Start-Process -FilePath powershell -ArgumentList "-NoExit","-Command", $runserverCmd

# Celery worker will be started after we confirm Redis is available. See below.

# If Redis is not running, try to start a temporary Redis container (requires Docker)
function Test-RedisPort {
    param($hostAddr = '127.0.0.1', $portNum = 6379)
    try {
        $sock = New-Object System.Net.Sockets.TcpClient
        $iar = $sock.BeginConnect($hostAddr, $portNum, $null, $null)
        $ok = $iar.AsyncWaitHandle.WaitOne(200)
        if ($ok) { $sock.EndConnect($iar); $sock.Close(); return $true }
        return $false
    } catch { return $false }
}

if (-not (Test-RedisPort)) {
    Write-Host "Redis not reachable on localhost:6379. Attempting to start via Docker (if available)..." -ForegroundColor Yellow
    if (Get-Command docker -ErrorAction SilentlyContinue) {
        try {
            # Check if container already exists
            $existing = docker ps -a --filter "name=cybervision_redis" --format "{{.Names}}" 2>$null
            if ($existing -notmatch 'cybervision_redis') {
                docker run --name cybervision_redis -p 6379:6379 -d redis:7 | Out-Null
                Start-Sleep -Seconds 2
                if (Test-RedisPort) {
                    Write-Host "Started Redis container 'cybervision_redis'." -ForegroundColor Green
                } else {
                    Write-Host "Failed to start Redis container or port still closed." -ForegroundColor Red
                }
            } else {
                # start existing container if it's stopped
                $stopped = docker ps -a --filter "name=cybervision_redis" --filter "status=exited" --format "{{.Names}}"
                if ($stopped) { docker start cybervision_redis | Out-Null; Start-Sleep -Seconds 2 }
                if (Test-RedisPort) { Write-Host "Started existing Redis container." -ForegroundColor Green }
            }
        } catch {
            Write-Host "Docker is installed but starting Redis failed: $_" -ForegroundColor Red
            Write-Host "If you don't have Docker, install Redis (WSL recommended) or run a Redis service locally." -ForegroundColor Yellow
        }
    } else {
        Write-Host "Docker not found. To run Celery you must install Redis or run Redis via WSL. See README Troubleshooting." -ForegroundColor Yellow
    }
}

# Start Celery worker only if Redis is available. If not, set eager task execution for dev so background tasks run synchronously.
if (Test-RedisPort) {
    Write-Host "Redis reachable, starting Celery worker..." -ForegroundColor Green
    $celeryCmd = "& `'$VenvActivate`'; python -m celery -A project worker --pool=solo -l info"
    Start-Process -FilePath powershell -ArgumentList "-NoExit","-Command", $celeryCmd
} else {
    Write-Host "Redis not found; running in development 'eager' task mode. Celery worker will not be started." -ForegroundColor Yellow
    # Set environment variable for Django/Celery synchronous task execution during development (best-effort)
    $env:CELERY_TASK_ALWAYS_EAGER = 'True'
    $env:CELERY_TASK_EAGER_PROPAGATES = 'True'
}

# Optionally start a Beat scheduler (commented out)
# $beatCmd = "& `'$VenvActivate`'; python -m celery -A project beat -l info"
# Start-Process -FilePath powershell -ArgumentList "-NoExit","-Command", $beatCmd

# Open default browser to the app
Start-Sleep -Seconds 2
Start-Process "http://localhost:8000/"

Write-Host "Started CyberVisionAI (Django + Celery). Check the opened windows for logs." -ForegroundColor Green
