@echo off
cd /d "%~dp0"

echo ===================================================
echo   Banking Accounting RAG - Start
echo ===================================================
echo.

REM 1. Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed.
    echo         https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo        OK
echo.

REM 2. Check Ollama
echo [2/5] Checking Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Ollama is not installed.
    echo         https://ollama.com
    pause
    exit /b 1
)
ollama --version
echo        OK
echo.

REM 3. Install Python packages
echo [3/5] Installing Python packages...
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo [ERROR] Package install failed.
    pause
    exit /b 1
)
echo        OK
echo.

REM 4. Start Ollama server
echo [4/5] Starting Ollama server...
tasklist /FI "IMAGENAME eq ollama.exe" 2>nul | find /I "ollama.exe" >nul
if %errorlevel% neq 0 (
    start /B ollama serve >nul 2>&1
    timeout /t 3 /nobreak >nul
    echo        Ollama server started
) else (
    echo        Ollama server already running
)
echo.

REM 5. Check Vector DB
echo [5/5] Checking Vector DB...
if exist chroma_db\chroma.sqlite3 goto :db_ready
echo        Building Vector DB... (about 50 min, first time only)
cd src
python build_vectordb.py
if %errorlevel% neq 0 (
    echo [ERROR] Vector DB build failed.
    pause
    exit /b 1
)
cd /d "%~dp0"
echo        OK
goto :db_done
:db_ready
echo        Vector DB found. OK
:db_done
echo.

REM 6. Start Flask server + open browser
echo ===================================================
echo   Starting service...
echo   Open http://localhost:5000 in your browser.
echo   Close this window or press Ctrl+C to stop.
echo ===================================================
echo.

cd src
start /B python app.py
timeout /t 3 /nobreak >nul
start http://localhost:5000
echo   Server is running. Press any key to stop.
pause >nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app.py*" >nul 2>&1
