#!/usr/bin/env bash
set -euo pipefail

# Real deployment script for Railway with post-deploy verification.
# Usage:
#   RAILWAY_TOKEN=xxx ./scripts/deploy_real.sh
# Optional vars:
#   HEALTHCHECK_TIMEOUT_SECONDS=240
#   HEALTHCHECK_INTERVAL_SECONDS=8
#   PUBLIC_API_URL=https://your-app.up.railway.app

HEALTHCHECK_TIMEOUT_SECONDS="${HEALTHCHECK_TIMEOUT_SECONDS:-240}"
HEALTHCHECK_INTERVAL_SECONDS="${HEALTHCHECK_INTERVAL_SECONDS:-8}"

step() { printf '\n==> %s\n' "$1"; }
fail() { printf '\n❌ %s\n' "$1"; exit 1; }

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Comando obrigatório não encontrado: $1"
}

step "Validando pré-requisitos"
require_cmd python
require_cmd pip
require_cmd curl
require_cmd git
require_cmd railway

if [[ -z "${RAILWAY_TOKEN:-}" ]]; then
  fail "Defina RAILWAY_TOKEN para deploy não-interativo."
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  fail "Há alterações não commitadas. Faça commit antes do deploy."
fi

step "Instalando dependências de runtime/teste"
pip install -r requirements.txt >/dev/null
pip install pytest >/dev/null

step "Executando testes"
pytest -q

step "Publicando nova versão no Railway"
railway up --ci

step "Detectando URL pública"
PUBLIC_API_URL="${PUBLIC_API_URL:-}"
if [[ -z "$PUBLIC_API_URL" ]]; then
  if railway domain >/tmp/trusthire_railway_domain.txt 2>/dev/null; then
    detected_domain="$(awk '/\.(railway|up\.railway)\.app/{print $NF; exit}' /tmp/trusthire_railway_domain.txt | tr -d '\r')"
    if [[ -n "$detected_domain" ]]; then
      if [[ "$detected_domain" =~ ^https?:// ]]; then
        PUBLIC_API_URL="$detected_domain"
      else
        PUBLIC_API_URL="https://${detected_domain}"
      fi
    fi
  fi
fi

if [[ -z "$PUBLIC_API_URL" ]]; then
  fail "Não foi possível detectar domínio automaticamente. Defina PUBLIC_API_URL e rode novamente."
fi

HEALTH_URL="${PUBLIC_API_URL%/}/health"
step "Aguardando healthcheck em ${HEALTH_URL}"

start_ts="$(date +%s)"
while true; do
  if curl -fsS "$HEALTH_URL" >/tmp/trusthire_health.json 2>/dev/null; then
    break
  fi

  now_ts="$(date +%s)"
  elapsed=$((now_ts - start_ts))
  if (( elapsed >= HEALTHCHECK_TIMEOUT_SECONDS )); then
    fail "Timeout no healthcheck (${HEALTHCHECK_TIMEOUT_SECONDS}s). Verifique logs: railway logs"
  fi
  sleep "$HEALTHCHECK_INTERVAL_SECONDS"
done

printf '\n✅ Deploy concluído com sucesso.\n'
printf 'URL: %s\n' "$PUBLIC_API_URL"
printf 'Health: %s\n\n' "$HEALTH_URL"
cat /tmp/trusthire_health.json
