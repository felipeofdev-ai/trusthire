#!/usr/bin/env python3
"""Generate a public benchmark summary from Locust CSV outputs."""

from __future__ import annotations

import csv
from pathlib import Path

RESULTS = Path("loadtest/results")
STATS_FILE = RESULTS / "trusthire_stats.csv"
OUT_FILE = Path("docs/BENCHMARK_PUBLIC.md")


def main() -> int:
    if not STATS_FILE.exists():
        OUT_FILE.write_text(
            "# Benchmark Público\n\n"
            "Nenhum resultado de benchmark encontrado ainda.\n\n"
            "Execute: `bash scripts/run_load_test.sh http://localhost:8000`\n"
        )
        return 0

    rows = list(csv.DictReader(STATS_FILE.open()))
    agg = next((r for r in rows if r.get("Name") == "Aggregated"), rows[-1])

    req_count = float(agg.get("Request Count") or 0)
    fail_count = float(agg.get("Failure Count") or 0)
    avg_ms = float(agg.get("Average Response Time") or 0)
    p95_ms = float(agg.get("95%") or 0)

    # Default run_load_test duration is 2m
    rpm = req_count / 2 if req_count else 0
    error_rate = (fail_count / req_count * 100) if req_count else 0

    OUT_FILE.write_text(
        "# Benchmark Público\n\n"
        "Resultados do último teste de carga executado via Locust.\n\n"
        f"- Sustained throughput: **{rpm:,.0f} req/min**\n"
        f"- Avg latency: **{avg_ms:.2f} ms**\n"
        f"- p95 latency: **{p95_ms:.2f} ms**\n"
        f"- Error rate: **{error_rate:.4f}%**\n"
        f"- Total requests: **{int(req_count):,}**\n"
        f"- Failures: **{int(fail_count):,}**\n"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
