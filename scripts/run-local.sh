#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER="$ROOT/server"
PY="$SERVER/.venv/bin/python"

if [ ! -x "$PY" ]; then
  echo "Virtual environment is missing."
  echo "Run first:"
  echo "  bash scripts/bootstrap-local.sh"
  exit 2
fi

cd "$SERVER"
exec "$PY" -m uvicorn app.main:app --host 127.0.0.1 --port 9000
