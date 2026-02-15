#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"
USERS="${USERS:-100}"
SPAWN_RATE="${SPAWN_RATE:-20}"
DURATION="${DURATION:-2m}"
OUT_DIR="loadtest/results"
mkdir -p "$OUT_DIR"

if ! command -v locust >/dev/null 2>&1; then
  echo "Installing locust..."
  pip install locust >/dev/null
fi

echo "Running load test against $BASE_URL"
locust -f loadtest/locustfile.py \
  --host "$BASE_URL" \
  --users "$USERS" \
  --spawn-rate "$SPAWN_RATE" \
  --run-time "$DURATION" \
  --headless \
  --csv "$OUT_DIR/trusthire" \
  --only-summary

python - <<'PY'
import csv
from pathlib import Path

stats = Path('loadtest/results/trusthire_stats.csv')
if not stats.exists():
    raise SystemExit('stats file not generated')

rows = list(csv.DictReader(stats.open()))
agg = next((r for r in rows if r.get('Name') == 'Aggregated'), rows[-1])
req = float(agg.get('Request Count') or 0)
fail = float(agg.get('Failure Count') or 0)
avg = float(agg.get('Average Response Time') or 0)
p95 = float(agg.get('95%') or 0)
if req <= 0:
    rpm = 0
else:
    rpm = req / 2  # rough estimate for 2m default

md = Path('loadtest/results/benchmark.md')
md.write_text(
    "# TrustHire Load Test Report\n\n"
    f"- Total requests: {int(req)}\n"
    f"- Failures: {int(fail)}\n"
    f"- Avg latency: {avg:.2f} ms\n"
    f"- P95 latency: {p95:.2f} ms\n"
    f"- Approx req/min: {rpm:.2f}\n"
)
print(md.read_text())
PY
