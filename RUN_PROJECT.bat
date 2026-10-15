@echo off
setlocal
cd /d "%~dp0"
echo ===============================================
echo   SENTINEL - SMS and URL Threat Analyzer
echo ===============================================
where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher "py" was not found. Install Python 3 and enable Add Python to PATH.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  py -m venv .venv
  if errorlevel 1 goto failed
)
echo Installing or checking dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed
echo.
echo Starting the server in a separate window...
start "Sentinel Flask Server" cmd /k "cd /d "%~dp0" ^&^& .venv\Scripts\python.exe app.py"
timeout /t 3 /nobreak >nul
start "" http://127.0.0.1:5000
exit /b 0
:failed
echo.
echo Setup failed. Read the error above, then check Python and internet access.
pause
exit /b 1
