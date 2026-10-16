#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER="$ROOT/server"
VENV="$SERVER/.venv"

echo "[1/4] Checking Python..."
python3 --version

echo "[2/4] Creating isolated virtual environment..."
if ! python3 -m venv "$VENV"; then
  echo
  echo "ERROR: Python venv support is missing."
  echo "On Ubuntu install it once with:"
  echo "  sudo apt install python3-venv"
  echo
  echo "Then run this script again."
  exit 2
fi

echo "[3/4] Installing project dependencies inside .venv..."
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install -e "$SERVER[dev]"

echo "[4/4] Running tests..."
cd "$SERVER"
"$VENV/bin/python" -m pytest -q

echo
echo "Bootstrap complete."
echo "Run API with:"
echo "  bash scripts/run-local.sh"
