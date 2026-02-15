#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${STRIPE_SECRET_KEY:-}" ]]; then
  echo "Set STRIPE_SECRET_KEY in environment (live key)"
  exit 1
fi

auth=(-u "${STRIPE_SECRET_KEY}:")

echo "Creating Stripe products/prices in live mode..."

premium_product=$(curl -s https://api.stripe.com/v1/products "${auth[@]}" \
  -d name="TrustHire Premium" \
  -d description="Unlimited + AI Match + Support")
premium_prod_id=$(echo "$premium_product" | python -c "import sys,json;print(json.load(sys.stdin)['id'])")

premium_price=$(curl -s https://api.stripe.com/v1/prices "${auth[@]}" \
  -d unit_amount=999 \
  -d currency=usd \
  -d "recurring[interval]=month" \
  -d product="$premium_prod_id")
premium_price_id=$(echo "$premium_price" | python -c "import sys,json;print(json.load(sys.stdin)['id'])")

enterprise_product=$(curl -s https://api.stripe.com/v1/products "${auth[@]}" \
  -d name="TrustHire Enterprise" \
  -d description="All Premium + API + Blockchain")
enterprise_prod_id=$(echo "$enterprise_product" | python -c "import sys,json;print(json.load(sys.stdin)['id'])")

enterprise_price=$(curl -s https://api.stripe.com/v1/prices "${auth[@]}" \
  -d unit_amount=4999 \
  -d currency=usd \
  -d "recurring[interval]=month" \
  -d product="$enterprise_prod_id")
enterprise_price_id=$(echo "$enterprise_price" | python -c "import sys,json;print(json.load(sys.stdin)['id'])")

cat <<TXT
Done.

Save these env vars in Railway:
STRIPE_PRICE_PRO_MONTHLY=${premium_price_id}
STRIPE_PRICE_ENTERPRISE_MONTHLY=${enterprise_price_id}

Also keep product IDs for audit:
PREMIUM_PRODUCT_ID=${premium_prod_id}
ENTERPRISE_PRODUCT_ID=${enterprise_prod_id}
TXT
