@echo off
echo ========================================================
echo Starting AI Agent PoC: Multi-Agent System
echo ========================================================

echo [1/2] Starting FastAPI Backend on http://localhost:8000 ...
start "Backend - FastAPI AI Agent Orchestrator" cmd /k "cd /d %~dp0 && python -m uvicorn backend.main:app --reload --port 8000"

echo [2/2] Starting Frontend Cockpit Dashboard on http://localhost:3000 ...
start "Frontend - Vite React Cockpit" cmd /k "cd /d %~dp0frontend\dashboard && npm run dev"

echo.
echo Both servers have been launched in separate windows!
echo - API Swagger Docs: http://localhost:8000/docs
echo - React Dashboard:  http://localhost:3000
echo ========================================================
