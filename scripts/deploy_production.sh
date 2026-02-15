#!/usr/bin/env bash
set -euo pipefail

APP_NAME="trusthire-api"
REGISTRY_URI="${REGISTRY_URI:-}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
PORT="${PORT:-8000}"

step(){ echo -e "\n==> $1"; }

step "Running tests before deploy"
pytest -q

step "Building Docker image"
docker build -t "${APP_NAME}:${IMAGE_TAG}" .

if [[ -n "$REGISTRY_URI" ]]; then
  step "Tagging and pushing image to registry"
  docker tag "${APP_NAME}:${IMAGE_TAG}" "${REGISTRY_URI}:${IMAGE_TAG}"
  docker push "${REGISTRY_URI}:${IMAGE_TAG}"
else
  echo "REGISTRY_URI not set, skipping push"
fi

if command -v railway >/dev/null 2>&1; then
  step "Deploying via Railway CLI"
  railway up --detach
else
  echo "Railway CLI not installed; deployment package is ready."
fi

cat <<TXT

Deploy completed (or package prepared).
Next checks:
- API health:   curl http://localhost:${PORT}/health
- API metrics:  curl http://localhost:${PORT}/metrics/prometheus
- Monitoring:   docker compose -f docker-compose.monitoring.yml up -d
- Dashboard:    http://localhost:3001 (admin/admin)
TXT
