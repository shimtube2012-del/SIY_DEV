#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "==================================================="
echo "  Banking Accounting RAG - Start"
echo "==================================================="
echo

# 1. Check Python
echo "[1/5] Checking Python..."
if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "[ERROR] Python is not installed."
    echo "        https://www.python.org/downloads/"
    exit 1
fi
PYTHON=$(command -v python3 || command -v python)
$PYTHON --version
echo "       OK"
echo

# 2. Check Ollama
echo "[2/5] Checking Ollama..."
if ! command -v ollama &>/dev/null; then
    echo "[ERROR] Ollama is not installed."
    echo "        https://ollama.com"
    exit 1
fi
ollama --version
echo "       OK"
echo

# 3. Install Python packages
echo "[3/5] Installing Python packages..."
$PYTHON -m pip install -r requirements.txt -q
echo "       OK"
echo

# 4. Start Ollama server
echo "[4/5] Starting Ollama server..."
if pgrep -x ollama >/dev/null 2>&1; then
    echo "       Ollama server already running"
else
    ollama serve >/dev/null 2>&1 &
    sleep 3
    echo "       Ollama server started"
fi
echo

# 5. Check Vector DB
echo "[5/5] Checking Vector DB..."
if [ -f chroma_db/chroma.sqlite3 ]; then
    echo "       Vector DB found. OK"
else
    echo "       Building Vector DB... (about 50 min, first time only)"
    $PYTHON src/build_vectordb.py
    echo "       OK"
fi
echo

# 6. Start Flask server + open browser
echo "==================================================="
echo "  Starting service..."
echo "  Open http://localhost:5000 in your browser."
echo "  Press Ctrl+C to stop."
echo "==================================================="
echo

# Open browser (platform-dependent)
open_browser() {
    sleep 3
    if command -v xdg-open &>/dev/null; then
        xdg-open http://localhost:5000
    elif command -v open &>/dev/null; then
        open http://localhost:5000
    fi
}
open_browser &

# Cleanup on exit
cleanup() {
    kill %1 2>/dev/null  # kill open_browser if still waiting
    echo
    echo "  Server stopped."
}
trap cleanup EXIT INT TERM

$PYTHON src/app.py
