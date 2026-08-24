@echo off
title Starting AgriRakshak Platform Services...
echo ========================================================
echo   AgriRakshak — Automatic Platform Launcher
echo ========================================================

echo [1/3] Starting Keras AI Model Server on Port 8000...
start "AgriRakshak Model Server (8000)" cmd /k "cd /d C:\Users\prans\OneDrive\Desktop\agrirakshak-api && C:\Users\prans\OneDrive\Desktop\agrirakshak-api\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/3] Starting FastAPI Supabase Backend on Port 8001...
start "AgriRakshak FastAPI Backend (8001)" cmd /k "cd /d C:\Users\prans\OneDrive\Desktop\agrirakshak-api\agrirakshak\backend && C:\Users\prans\OneDrive\Desktop\agrirakshak-api\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001"

timeout /t 3 /nobreak >nul

echo [3/3] Starting Next.js Frontend Portal on Port 3000...
start "AgriRakshak Next.js Frontend (3000)" cmd /k "cd /d C:\Users\prans\OneDrive\Desktop\agrirakshak-api\agrirakshak\frontend && npm run dev"

echo ========================================================
echo All 3 AgriRakshak services launched!
echo Frontend: http://localhost:3000
echo Backend Docs: http://localhost:8001/docs
echo Model Server: http://localhost:8000
echo ========================================================
pause
