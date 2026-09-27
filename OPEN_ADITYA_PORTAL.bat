@echo off
title Aditya University Portal - Always On Launcher
cd /d "%~dp0"

echo ======================================================================
echo  ADITYA UNIVERSITY - STUDENT PERFORMANCE ANALYTICS & ERP
echo  Ensuring 24/7 Always-On Service is Running...
echo ======================================================================

:: Check if live_service is running
tasklist /FI "IMAGENAME eq cloudflared.exe" 2>NUL | find /I /N "cloudflared.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [+] 24/7 Live Service is ALREADY RUNNING!
) else (
    echo [*] Starting 24/7 Background Service...
    start "" wscript.exe "%~dp0run_live_service_silent.vbs"
    timeout /t 5 /nobreak >nul
)

:: Read public link if available
set PUBLIC_LINK=http://localhost:5000
if exist "%~dp0ACTIVE_PUBLIC_LINK.txt" (
    set /p PUBLIC_LINK=<"%~dp0ACTIVE_PUBLIC_LINK.txt"
)

echo.
echo ======================================================================
echo  PORTAL LINKS:
echo  1. Public Worldwide Link: %PUBLIC_LINK%
echo  2. Localhost Link:        http://localhost:5000
echo ======================================================================
echo.
echo Opening portal in your web browser now...
start "" "%PUBLIC_LINK%"
start "" http://localhost:5000

echo Done! You may close this window.
timeout /t 4 >nul
exit
