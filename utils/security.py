"""Security utilities and middleware."""

from __future__ import annotations

import html
import re
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Adds baseline HTTP security headers for browser clients."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        response.headers[
            "Content-Security-Policy"
        ] = "default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https:; script-src 'self' 'unsafe-inline' https:; connect-src 'self' https: http://localhost:8000 http://localhost:5173"
        return response


def sanitize_user_text(value: str) -> str:
    """Basic server-side sanitization for user-provided free text."""
    if not value:
        return value
    value = value.replace("\x00", "")
    value = re.sub(r"\s+", " ", value).strip()
    return html.escape(value)
