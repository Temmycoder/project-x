@echo off
REM X-Share Setup Script for Windows

echo.
echo ╔════════════════════════════════════╗
echo ║       X-Share Setup Wizard          ║
echo ║   Professional Screen Sharing       ║
echo ╚════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check Node
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Python and Node.js found
echo.

REM Setup Backend
echo 📦 Installing Python dependencies...
cd backend
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Python setup failed
    pause
    exit /b 1
)
cd ..

REM Setup Frontend
echo 📦 Installing Node dependencies...
cd electron-app
call npm install
if %errorlevel% neq 0 (
    echo ❌ Node setup failed
    pause
    exit /b 1
)
cd ..

echo.
echo ✅ Setup Complete!
echo.
echo Next steps:
echo.
echo 1. Start Python Server (Terminal 1):
echo    cd backend
echo    python server.py
echo.
echo 2. Start Electron App (Terminal 2):
echo    cd electron-app
echo    npm run dev
echo.
echo Happy streaming! 🚀
echo.
pause
