Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Starting AI Agent PoC: Multi-Agent System" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan

$projectRoot = $PSScriptRoot
if (-not $projectRoot) { $projectRoot = Get-Location }

Write-Host "[1/2] Launching FastAPI Backend (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$projectRoot'; python -m uvicorn backend.main:app --reload --port 8000"

Write-Host "[2/2] Launching React Dashboard (Port 3000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$projectRoot\frontend\dashboard'; npm run dev"

Write-Host "Opening dashboard in browser..." -ForegroundColor Cyan
Start-Sleep -Seconds 3
Start-Process "http://localhost:3000"

Write-Host "`nReady! Backend running on :8000, Dashboard on :3000." -ForegroundColor Green
