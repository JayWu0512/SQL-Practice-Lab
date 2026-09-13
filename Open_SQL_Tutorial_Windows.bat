@echo off
setlocal

REM Double-click this file in Windows File Explorer to open the SQL tutorial.
REM Keep the "SQL Tutorial Server" window open while using live Supabase queries.

set "TUTORIAL_DIR=%~dp0"
set "SERVER_SCRIPT=%TUTORIAL_DIR%sql_tutorial_server.py"
set "REQUIREMENTS_FILE=%TUTORIAL_DIR%requirements.txt"

if not exist "%SERVER_SCRIPT%" (
    echo This launcher must stay in the project folder.
    echo sql_tutorial_server.py was not found beside it.
    pause
    exit /b 1
)

if not exist "%REQUIREMENTS_FILE%" (
    echo This launcher must stay in the project folder.
    echo requirements.txt was not found beside it.
    pause
    exit /b 1
)

set "PYTHON_EXE=%TUTORIAL_DIR%.venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=%USERPROFILE%\miniforge3\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"

"%PYTHON_EXE%" -c "import sqlalchemy, psycopg" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Required Python packages are missing.
    echo Install the project packages in this Python environment with:
    echo   "%PYTHON_EXE%" -m pip install -r "%REQUIREMENTS_FILE%"
    echo.
    pause
    exit /b 1
)

start "SQL Tutorial Server" cmd /k ""%PYTHON_EXE%" "%SERVER_SCRIPT%""
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:8765"

echo.
echo SQL Tutorial opened in your default browser.
echo Keep the separate "SQL Tutorial Server" window open while using live queries.
echo Close that server window when you are finished.
timeout /t 3 /nobreak >nul
