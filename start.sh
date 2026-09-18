#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND="$ROOT/backend"
FRONTEND="$ROOT/frontend"
VENV="$BACKEND/.venv"

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "ERREUR: Python 3 est requis."
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "ERREUR: Node.js/npm est requis."
  exit 1
fi

if [[ ! -x "$VENV/bin/python" ]]; then
  echo "[1/5] Creation de l'environnement Python..."
  "$PYTHON" -m venv "$VENV"
else
  echo "[1/5] Environnement Python deja present."
fi

PYTHON_EXE="$VENV/bin/python"
echo "[2/5] Installation/mise a jour des dependances backend..."
"$PYTHON_EXE" -m pip install --disable-pip-version-check -q -r "$BACKEND/requirements.txt"

[[ -f "$BACKEND/.env" ]] || cp "$BACKEND/.env.example" "$BACKEND/.env"
[[ -f "$FRONTEND/.env" ]] || cp "$FRONTEND/.env.example" "$FRONTEND/.env"

if [[ ! -d "$FRONTEND/node_modules" ]]; then
  echo "[3/5] Installation des dependances frontend..."
  (cd "$FRONTEND" && npm install)
else
  echo "[3/5] Dependances frontend deja presentes."
fi

echo "[4/5] Lancement FastAPI : http://localhost:8000"
(cd "$BACKEND" && "$PYTHON_EXE" -m uvicorn app.main:app --reload --port 8000) &
BACK_PID=$!

echo "[5/5] Lancement Vite : http://localhost:5173"
(cd "$FRONTEND" && npm run dev) &
FRONT_PID=$!

cleanup() {
  echo "Arret de StudySprint..."
  kill "$BACK_PID" "$FRONT_PID" 2>/dev/null || true
}
trap cleanup INT TERM EXIT

printf '\nApplication : http://localhost:5173\nAPI         : http://localhost:8000\nSwagger     : http://localhost:8000/docs\n'
wait
