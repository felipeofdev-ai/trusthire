"""
TrustHire Configuration — SaaS Edition
Centralized, Railway-ready configuration
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    # ==================== APPLICATION ====================
    APP_NAME: str = "TrustHire"
    APP_VERSION: str = "2.0.0"
    ENV: str = "dev"            # dev | staging | prod
    DEBUG: bool = False

    # ==================== API ====================
    API_V1_PREFIX: str = "/api/v1"
    API_TITLE: str = "TrustHire API"
    API_DESCRIPTION: str = "AI-powered job offer verification and scam detection"

    # ==================== SECURITY ====================
    # Generate: openssl rand -hex 32
    SECRET_KEY: str = "dev-secret-key-change-in-production-please"
    API_KEY_HEADER: str = "X-API-Key"
    ALLOWED_HOSTS: str = "*"
    # CORS_ORIGINS as a plain string — split on comma at runtime
    # In Railway set as: https://felipeofdev-ai.github.io,https://trusthire.dev
    CORS_ORIGINS_STR: str = "http://localhost:3000,http://localhost:8000,https://felipeofdev-ai.github.io,https://trusthire.dev"

    @property
    def CORS_ORIGINS(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS_STR.split(",") if o.strip()]

    # ==================== RATE LIMITING ====================
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_FREE: str = "10/minute"
    RATE_LIMIT_PRO: str = "100/minute"
    RATE_LIMIT_ENTERPRISE: str = "1000/minute"

    # ==================== AI ====================
    ANTHROPIC_API_KEY: Optional[str] = None
    AI_MODEL: str = "claude-sonnet-4-20250514"
    AI_MAX_TOKENS: int = 500
    AI_TIMEOUT: int = 15
    AI_TEMPERATURE: float = 0.3

    # ==================== ANALYSIS ENGINE ====================
    ENGINE_VERSION: str = "2.0.0"
    RULESET_VERSION: str = "2026.02"
    MAX_TEXT_LENGTH: int = 10000
    MIN_CONFIDENCE_THRESHOLD: float = 0.75
    ENABLE_PATTERN_ENGINE: bool = True
    ENABLE_AI_LAYER: bool = True
    ENABLE_ML_DETECTOR: bool = False
    FAIL_OPEN: bool = True

    # ==================== DATABASE ====================
    # Optional — app runs without DB (in-memory mode)
    DATABASE_URL: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # ==================== CACHE ====================
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600
    CACHE_PREFIX: str = "trusthire:"

    # ==================== MONITORING ====================
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    METRICS_ENABLED: bool = True

    # ==================== STRIPE ====================
    # Optional — billing disabled if empty
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_PRO_MONTHLY: str = ""
    STRIPE_PRICE_PRO_YEARLY: str = ""
    STRIPE_PRICE_ENTERPRISE_MONTHLY: str = ""
    STRIPE_PRICE_ENTERPRISE_YEARLY: str = ""

    # ==================== FEATURES ====================
    FEATURE_PDF_REPORTS: bool = True
    FEATURE_DOMAIN_REPUTATION: bool = True
    FEATURE_LINK_ANALYSIS: bool = True
    FEATURE_SOCIAL_ENGINEERING: bool = True
    FEATURE_COMMUNITY_REPORTS: bool = False
    FEATURE_RECRUITER_PROFILES: bool = False

    # ==================== TIERS ====================
    FREE_TIER_DAILY_LIMIT: int = 10
    PRO_TIER_DAILY_LIMIT: int = 100
    ENTERPRISE_TIER_DAILY_LIMIT: int = 10000

    # ==================== EXTERNAL ====================
    VIRUSTOTAL_API_KEY: Optional[str] = None
    URLSCAN_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


def validate_production_config():
    """
    Warn about missing optional config — but NEVER crash the app.
    The app can start without Stripe/DB and gracefully degrade.
    """
    warnings = []

    if not settings.ANTHROPIC_API_KEY:
        warnings.append("ANTHROPIC_API_KEY not set — AI analysis disabled")

    if not settings.DATABASE_URL:
        warnings.append("DATABASE_URL not set — using in-memory store")

    if not settings.STRIPE_SECRET_KEY:
        warnings.append("STRIPE_SECRET_KEY not set — billing disabled")

    if "dev-secret-key" in settings.SECRET_KEY:
        warnings.append("SECRET_KEY is default — change for production!")

    for w in warnings:
        import logging
        logging.getLogger("config").warning(w)

    return True
