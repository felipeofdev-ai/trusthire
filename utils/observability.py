"""Observability primitives for TrustHire."""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass
from threading import Lock
from typing import Deque, Dict


@dataclass
class RequestSnapshot:
    total_requests: int
    total_errors: int
    uptime_seconds: float
    avg_latency_ms: float
    p95_latency_ms: float
    requests_per_minute: float
    error_rate: float
    estimated_cost_per_request_usd: float


class RequestMetrics:
    """In-memory metrics aggregator for API requests."""

    def __init__(self, estimated_cost_per_request_usd: float = 0.002) -> None:
        self.started_at = time.time()
        self.total_requests = 0
        self.total_errors = 0
        self.latencies_ms: Deque[float] = deque(maxlen=5000)
        self.request_timestamps: Deque[float] = deque(maxlen=10000)
        self.estimated_cost_per_request_usd = estimated_cost_per_request_usd
        self._lock = Lock()

    def record(self, latency_ms: float, is_error: bool) -> None:
        now = time.time()
        with self._lock:
            self.total_requests += 1
            if is_error:
                self.total_errors += 1
            self.latencies_ms.append(latency_ms)
            self.request_timestamps.append(now)
            self._trim_old(now)

    def _trim_old(self, now: float) -> None:
        one_minute_ago = now - 60
        while self.request_timestamps and self.request_timestamps[0] < one_minute_ago:
            self.request_timestamps.popleft()

    def snapshot(self) -> RequestSnapshot:
        with self._lock:
            now = time.time()
            self._trim_old(now)
            uptime = max(0.001, now - self.started_at)
            latencies = sorted(self.latencies_ms)

            avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
            p95_idx = int((len(latencies) - 1) * 0.95) if latencies else 0
            p95 = latencies[p95_idx] if latencies else 0.0
            rpm = float(len(self.request_timestamps))
            error_rate = (self.total_errors / self.total_requests) if self.total_requests else 0.0

            return RequestSnapshot(
                total_requests=self.total_requests,
                total_errors=self.total_errors,
                uptime_seconds=uptime,
                avg_latency_ms=round(avg_latency, 2),
                p95_latency_ms=round(p95, 2),
                requests_per_minute=round(rpm, 2),
                error_rate=round(error_rate, 4),
                estimated_cost_per_request_usd=self.estimated_cost_per_request_usd,
            )


def metrics_to_dict(snapshot: RequestSnapshot) -> Dict[str, float]:
    uptime_pct = 100.0 - (snapshot.error_rate * 100.0)
    return {
        "uptime_percent": round(max(0.0, uptime_pct), 3),
        "uptime_seconds": round(snapshot.uptime_seconds, 2),
        "latency_avg_ms": snapshot.avg_latency_ms,
        "latency_p95_ms": snapshot.p95_latency_ms,
        "requests_per_minute": snapshot.requests_per_minute,
        "error_rate": snapshot.error_rate,
        "cost_per_request_usd": snapshot.estimated_cost_per_request_usd,
        "total_requests": snapshot.total_requests,
        "total_errors": snapshot.total_errors,
    }
