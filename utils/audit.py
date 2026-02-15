"""Audit logging helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from fastapi import Request
from utils.logger import get_logger

logger = get_logger("audit")


def log_audit_event(
    action: str,
    user_id: str,
    request: Optional[Request] = None,
    status: str = "success",
    device: str = "unknown",
) -> None:
    ip = request.client.host if request and request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown") if request else "unknown"
    logger.info(
        "audit_event",
        extra={
            "extra": {
                "action": action,
                "user_id": user_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ip": ip,
                "device": device,
                "user_agent": ua,
                "status": status,
            }
        },
    )
