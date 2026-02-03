@echo off
REM Quick start script for Windows

echo.
echo 🚀 Chemical Equipment Parameter Visualizer - Quick Start
echo =======================================================
echo.

REM Check Python
echo 📋 Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found
echo.

REM Check Node.js
echo 📋 Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js 16 or higher.
    pause
    exit /b 1
)
for /f "tokens=1" %%i in ('node --version') do set NODE_VERSION=%%i
echo ✓ Node.js %NODE_VERSION% found
echo.

REM Start backend
echo 🔨 Starting Backend...
cd backend
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
python manage.py migrate >nul 2>&1
echo ✓ Backend starting on port 8000...
start cmd /k python manage.py runserver
timeout /t 2 >nul

REM Start frontend
echo 🎨 Starting Frontend...
cd ..\frontend\web
call npm install -q >nul 2>&1
echo ✓ Frontend starting on port 3000...
start cmd /k npm run dev

echo.
echo ✅ Application Started!
echo 🌐 Frontend: http://localhost:3000
echo 📡 Backend API: http://localhost:8000/api
echo.
echo Close the terminal windows to stop the application
echo.
pause
