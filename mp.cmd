@echo off
setlocal EnableExtensions
REM ============================================================
REM  mp.cmd  -  one entry point for Windows (PowerShell or cmd)
REM  Usage:  .\mp check | setkey | odds | daily | fixture | grade | close | publish | preview | setup
REM ============================================================
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "VPY=%~dp0.venv\Scripts\python.exe"
if not exist "%VPY%" call :makevenv
if not exist "%VPY%" exit /b 1
set "CMD=%~1"
if "%CMD%"=="" set "CMD=help"
if /I "%CMD%"=="check"   goto check
if /I "%CMD%"=="setkey"  goto setkey
if /I "%CMD%"=="odds"    goto odds
if /I "%CMD%"=="daily"   goto daily
if /I "%CMD%"=="fixture" goto fixture
if /I "%CMD%"=="grade"   goto grade
if /I "%CMD%"=="close"   goto close
if /I "%CMD%"=="publish" goto publish
if /I "%CMD%"=="preview" goto preview
if /I "%CMD%"=="setup"   goto setup
if /I "%CMD%"=="gitsetup" goto gitsetup
if /I "%CMD%"=="push"    goto push
echo Commands: check, setkey, odds, daily, fixture, grade, close, publish, preview, setup, gitsetup, push
exit /b 0

:check
"%VPY%" -m pip install -r requirements.txt --quiet --disable-pip-version-check
"%VPY%" run_check.py
exit /b %ERRORLEVEL%
:setkey
"%VPY%" run_setup.py
exit /b %ERRORLEVEL%
:odds
"%VPY%" run_probe.py
exit /b %ERRORLEVEL%
:daily
"%VPY%" run_daily.py %2 %3
exit /b %ERRORLEVEL%
:fixture
"%VPY%" run_daily.py --fixture %2
exit /b %ERRORLEVEL%
:grade
"%VPY%" run_grade.py
exit /b %ERRORLEVEL%
:close
"%VPY%" run_close.py
exit /b %ERRORLEVEL%
:publish
"%VPY%" run_publish.py %2 %3
exit /b %ERRORLEVEL%
:preview
echo Opening http://localhost:8000  (press Ctrl+C here to stop the preview)
start "" http://localhost:8000
"%VPY%" -m http.server 8000 --directory site\public
exit /b 0
:push
"%VPY%" run_push.py
exit /b %ERRORLEVEL%
:gitsetup
"%VPY%" run_gitsetup.py %2 %3
exit /b %ERRORLEVEL%
:setup
"%VPY%" -m pip install -r requirements.txt
exit /b %ERRORLEVEL%

:makevenv
echo [setup] Creating a private Python environment in .venv (one time, 2-5 minutes)...
where py >nul 2>nul
if not errorlevel 1 (
  py -3.13 -m venv .venv >nul 2>nul
  if not exist "%VPY%" py -3.12 -m venv .venv >nul 2>nul
  if not exist "%VPY%" py -3 -m venv .venv
) else (
  python -m venv .venv
)
if not exist "%VPY%" (
  echo [setup] ERROR: Python was not found. Install Python 3.13 from python.org, tick "Add python.exe to PATH", reopen PowerShell, try again.
  exit /b 1
)
"%VPY%" -m pip install --upgrade pip --quiet --disable-pip-version-check
"%VPY%" -m pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
  echo [setup] ERROR: package installation failed. Copy the text above and send it to Claude.
  exit /b 1
)
echo [setup] Environment ready.
exit /b 0
