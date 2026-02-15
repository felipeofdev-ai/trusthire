#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PARENT_DIR="$(dirname "$ROOT_DIR")"
BACKEND_DIR="${PARENT_DIR}/trusthire-backend"
FRONTEND_DIR="${PARENT_DIR}/trusthire-frontend"

echo "🔗 Integrando ecossistema TrustHire"
echo "- Projeto base:      ${ROOT_DIR}"
echo "- trusthire-backend: ${BACKEND_DIR}"
echo "- trusthire-frontend:${FRONTEND_DIR}"

clone_or_pull() {
  local repo_url="$1"
  local target_dir="$2"

  if [[ -d "$target_dir/.git" ]]; then
    echo "📥 Atualizando $(basename "$target_dir")..."
    git -C "$target_dir" pull --ff-only
  else
    echo "📦 Clonando $(basename "$target_dir")..."
    git clone "$repo_url" "$target_dir"
  fi
}

clone_or_pull "https://github.com/felipeofdev-ai/trusthire-backend.git" "$BACKEND_DIR"
clone_or_pull "https://github.com/felipeofdev-ai/trusthire-frontend.git" "$FRONTEND_DIR"

if [[ -f "$BACKEND_DIR/.env.example" && ! -f "$BACKEND_DIR/.env" ]]; then
  cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
fi

if [[ -f "$BACKEND_DIR/.env" ]]; then
  python - "$BACKEND_DIR/.env" <<'PY'
from pathlib import Path
import re

path = Path(__import__('sys').argv[1])
content = path.read_text()
origins = "http://localhost:3000,http://localhost:5173,http://localhost:4173,http://localhost:8080,http://127.0.0.1:3000,http://127.0.0.1:5173,http://127.0.0.1:4173,http://127.0.0.1:8080"

if re.search(r'^ALLOWED_ORIGINS=', content, flags=re.MULTILINE):
    content = re.sub(r'^ALLOWED_ORIGINS=.*$', f'ALLOWED_ORIGINS={origins}', content, flags=re.MULTILINE)
else:
    content += f'\nALLOWED_ORIGINS={origins}\n'

path.write_text(content)
print(f"✅ Backend .env atualizado: {path}")
PY
else
  echo "⚠️  Não foi possível criar/editar ${BACKEND_DIR}/.env"
fi

cat > "$FRONTEND_DIR/.env.local" <<EOF2
VITE_API_URL=http://localhost:8000/api/v1
VITE_TRUSTHIRE_WEB_URL=http://localhost:8080
EOF2

echo "✅ Frontend .env.local atualizado: ${FRONTEND_DIR}/.env.local"

cat <<'TXT'

🚀 Próximos passos:
1) Backend
   cd ../trusthire-backend
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python main.py

2) Frontend React
   cd ../trusthire-frontend
   npm install
   npm run dev

3) Projeto trusthire (este repositório)
   cd ../trusthire
   python -m http.server 8080

Acesse:
- Backend API:     http://localhost:8000/api/v1/docs
- Frontend React:  http://localhost:5173 (ou porta informada pelo Vite)
- Frontend HTML:   http://localhost:8080?api=http://localhost:8000/api/v1
TXT
