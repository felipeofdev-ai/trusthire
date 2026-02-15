"""AI Guardian agent for defensive log scanning (safe passive mode by default)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class GuardianAlert:
    ip: str
    reason: str
    score: float


class GuardianAgent:
    """
    Passive-first anomaly scanner.
    In active mode, integrate with firewall/blocklist service.
    """

    def __init__(self, block_threshold: float = 0.85) -> None:
        self.block_threshold = block_threshold

    def score_event(self, event: dict) -> float:
        score = 0.0
        status = int(event.get("status_code", 200))
        ua = str(event.get("user_agent", "")).lower()
        path = str(event.get("path", ""))

        if status >= 500:
            score += 0.25
        if "sqlmap" in ua or "curl" in ua:
            score += 0.25
        if "../" in path or "wp-admin" in path or ".env" in path:
            score += 0.45
        if event.get("requests_per_minute", 0) > 120:
            score += 0.35

        return min(score, 1.0)

    def scan(self, events: Iterable[dict]) -> list[GuardianAlert]:
        alerts: list[GuardianAlert] = []
        for e in events:
            score = self.score_event(e)
            if score >= self.block_threshold:
                alerts.append(
                    GuardianAlert(
                        ip=str(e.get("ip", "unknown")),
                        reason="anomaly_score_exceeded",
                        score=score,
                    )
                )
        return alerts
