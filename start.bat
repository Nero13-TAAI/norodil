@echo off
REM Quick start script for Windows
REM This starts both the webhook server and background monitor

echo ================================================
echo  WhatsApp AI Automation System
echo  NÖRODİL Dil ve Konusma Merkezi
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then: venv\Scripts\activate
    echo Then: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if .env exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and fill in your credentials
    pause
    exit /b 1
)

echo Starting system...
echo.

REM Start webhook server in new window
start "WhatsApp Webhook Server" cmd /k "venv\Scripts\activate && cd execution && python whatsapp_webhook_server.py"

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start background monitor in new window
start "Background Monitor" cmd /k "venv\Scripts\activate && cd execution && python background_monitor.py"

echo.
echo ================================================
echo  System started!
echo  - Webhook Server: http://localhost:5000
echo  - Background Monitor: Running
echo ================================================
echo.
echo Press any key to stop all services...
pause >nul

REM Kill the processes
taskkill /FI "WindowTitle eq WhatsApp Webhook Server*" /F
taskkill /FI "WindowTitle eq Background Monitor*" /F

echo.
echo System stopped.
pause
