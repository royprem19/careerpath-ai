@echo off
echo ===================================================
echo Starting CareerPath AI Backend Server (FastAPI)...
echo ===================================================
cd /d "%~dp0backend"
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py
) else (
    python main.py
)
pause
