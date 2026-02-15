#!/usr/bin/env bash
set -euo pipefail

BACKEND_URL="${1:-http://localhost:8000}"

if ! command -v stripe >/dev/null 2>&1; then
  echo "Stripe CLI not found. Install: https://docs.stripe.com/stripe-cli"
  exit 1
fi

echo "Forwarding Stripe events to ${BACKEND_URL}/api/webhooks/stripe"
stripe listen --forward-to "${BACKEND_URL}/api/webhooks/stripe"
