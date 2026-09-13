#!/bin/zsh

# Double-click this file in Finder to open the SQL tutorial in your browser.
# Keep this Terminal window open while using live Supabase queries.

set -e

TUTORIAL_DIR="$(cd -- "$(dirname -- "$0")" && pwd -P)"
SERVER_SCRIPT="$TUTORIAL_DIR/sql_tutorial_server.py"
REQUIREMENTS_FILE="$TUTORIAL_DIR/requirements.txt"

cd "$TUTORIAL_DIR"

if [[ ! -f "$SERVER_SCRIPT" || ! -f "$REQUIREMENTS_FILE" ]]; then
  echo "This launcher must stay in the project folder."
  echo "sql_tutorial_server.py and requirements.txt were not found beside it."
  read "?Press Return to close."
  exit 1
fi

if [[ -x "$TUTORIAL_DIR/.venv/bin/python" ]]; then
  PYTHON_BIN="$TUTORIAL_DIR/.venv/bin/python"
elif [[ -x "$HOME/miniforge3/bin/python" ]]; then
  PYTHON_BIN="$HOME/miniforge3/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python)"
else
  echo "Python 3 was not found."
  echo "Install Python or Miniforge, then run this launcher again."
  read "?Press Return to close."
  exit 1
fi

if ! "$PYTHON_BIN" -c "import sqlalchemy, psycopg" 2>/dev/null; then
  echo "The required Python packages are missing."
  echo "Install the project packages first:"
  echo "  $PYTHON_BIN -m pip install -r \"$REQUIREMENTS_FILE\""
  read "?Press Return to close."
  exit 1
fi

"$PYTHON_BIN" "$SERVER_SCRIPT" &
SERVER_PID=$!

cleanup() {
  kill "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

sleep 1
open "http://127.0.0.1:8765"

echo "SQL Tutorial is open in your browser."
echo "Keep this window open while running live Supabase queries."
echo "Press Control+C here when you are finished."

wait "$SERVER_PID"
