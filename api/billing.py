"""TrustHire Billing API - Stripe checkout, portal and webhook."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from auth.auth_service import require_auth
from config import settings
from database.user_repository import UserRepository
from models.user_models import (
    CheckoutRequest,
    CheckoutResponse,
    PlanInfo,
    PortalRequest,
    PortalResponse,
    SubscriptionInfo,
    SubscriptionStatus,
    UserTier,
)
from utils.logger import get_logger

logger = get_logger("api.billing")
router = APIRouter(prefix="/billing", tags=["Billing"])
_processed_webhook_events: set[str] = set()

_stripe = None
if settings.STRIPE_SECRET_KEY:
    try:
        import stripe as _stripe_module

        _stripe_module.api_key = settings.STRIPE_SECRET_KEY
        _stripe = _stripe_module
        logger.info("Stripe initialized")
    except ImportError:
        logger.warning("stripe package not installed")
else:
    logger.warning("STRIPE_SECRET_KEY not set — billing endpoints disabled")


def _require_stripe() -> None:
    if not _stripe:
        raise HTTPException(status_code=503, detail="Billing not configured. Set STRIPE_SECRET_KEY.")


def _tier_from_plan(plan: str) -> UserTier:
    plan = (plan or "").lower()
    if "enterprise" in plan:
        return UserTier.ENTERPRISE
    if "pro" in plan or "premium" in plan:
        return UserTier.PRO
    return UserTier.FREE


PLANS: list[PlanInfo] = [
    PlanInfo(
        id="free",
        name="Free",
        tier=UserTier.FREE,
        price_monthly=0,
        price_yearly=0,
        daily_limit=10,
        features=["10 analyses/day", "Pattern detection", "Risk score", "API access"],
    ),
    PlanInfo(
        id="pro_monthly",
        name="Pro",
        tier=UserTier.PRO,
        price_monthly=19.90,
        price_yearly=14.90,
        daily_limit=100,
        stripe_price_id_monthly=settings.STRIPE_PRICE_PRO_MONTHLY,
        stripe_price_id_yearly=settings.STRIPE_PRICE_PRO_YEARLY,
        features=[
            "100 analyses/day",
            "AI analysis (Claude)",
            "Link scanning",
            "Social engineering detection",
            "Priority API",
            "CSV export",
            "Email support",
        ],
    ),
    PlanInfo(
        id="enterprise",
        name="Enterprise",
        tier=UserTier.ENTERPRISE,
        price_monthly=99.90,
        price_yearly=79.90,
        daily_limit=10000,
        stripe_price_id_monthly=settings.STRIPE_PRICE_ENTERPRISE_MONTHLY,
        stripe_price_id_yearly=settings.STRIPE_PRICE_ENTERPRISE_YEARLY,
        features=[
            "10,000 analyses/day",
            "All Pro features",
            "Bulk API",
            "Team management",
            "SLA 99.9%",
            "Dedicated support",
            "Custom integrations",
        ],
    ),
]


@router.get("/plans", response_model=list[PlanInfo])
async def get_plans():
    return PLANS


@router.get("/subscription", response_model=SubscriptionInfo)
async def get_subscription(user=Depends(require_auth)):
    db = UserRepository()
    user_db = await db.get_by_id(user.user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    current_period_end = None
    cancel_at_period_end = False

    if _stripe and user_db.stripe_subscription_id:
        try:
            sub = _stripe.Subscription.retrieve(user_db.stripe_subscription_id)
            current_period_end = datetime.fromtimestamp(sub["current_period_end"])
            cancel_at_period_end = sub.get("cancel_at_period_end", False)
        except Exception as e:
            logger.error(f"stripe_subscription_fetch_failed: {e}")

    return SubscriptionInfo(
        tier=user_db.tier,
        status=user_db.subscription_status,
        current_period_end=current_period_end,
        cancel_at_period_end=cancel_at_period_end,
        stripe_subscription_id=user_db.stripe_subscription_id,
    )


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(request: CheckoutRequest, user=Depends(require_auth)):
    _require_stripe()
    db = UserRepository()
    user_db = await db.get_by_id(user.user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    price_map = {
        "pro_monthly": settings.STRIPE_PRICE_PRO_MONTHLY,
        "pro_yearly": settings.STRIPE_PRICE_PRO_YEARLY,
        "enterprise_monthly": settings.STRIPE_PRICE_ENTERPRISE_MONTHLY,
        "enterprise_yearly": settings.STRIPE_PRICE_ENTERPRISE_YEARLY,
        "premium": settings.STRIPE_PRICE_PRO_MONTHLY,
    }
    price_id = price_map.get(request.plan)
    if not price_id:
        raise HTTPException(status_code=400, detail=f"Invalid plan. Options: {list(price_map.keys())}")

    success_url = request.success_url or settings.STRIPE_SUCCESS_URL
    cancel_url = request.cancel_url or settings.STRIPE_CANCEL_URL
    if not success_url or not cancel_url:
        raise HTTPException(status_code=400, detail="success_url and cancel_url are required")

    try:
        customer_id = user_db.stripe_customer_id
        if not customer_id:
            customer = _stripe.Customer.create(
                email=user_db.email,
                name=user_db.name,
                metadata={"trusthire_user_id": user_db.id},
            )
            customer_id = customer.id
            await db.update_stripe_customer(user_db.id, customer_id)

        session = _stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
            allow_promotion_codes=True,
            subscription_data={
                "metadata": {
                    "trusthire_user_id": user_db.id,
                    "plan": request.plan,
                },
                "trial_period_days": max(0, settings.STRIPE_TRIAL_DAYS),
            },
            metadata={"trusthire_user_id": user_db.id, "plan": request.plan},
        )

        return CheckoutResponse(checkout_url=session.url, session_id=session.id)
    except Exception as e:
        logger.error(f"stripe_checkout_failed: {e}")
        raise HTTPException(status_code=500, detail="Payment service error")


@router.post("/portal", response_model=PortalResponse)
async def create_portal(request: PortalRequest, user=Depends(require_auth)):
    _require_stripe()
    db = UserRepository()
    user_db = await db.get_by_id(user.user_id)
    if not user_db or not user_db.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No active subscription found")

    try:
        session = _stripe.billing_portal.Session.create(
            customer=user_db.stripe_customer_id,
            return_url=request.return_url,
        )
        return PortalResponse(portal_url=session.url)
    except Exception as e:
        logger.error(f"stripe_portal_failed: {e}")
        raise HTTPException(status_code=500, detail="Payment service error")


async def process_stripe_event(event: dict) -> bool:
    event_id = event.get("id")
    if event_id and event_id in _processed_webhook_events:
        logger.info("stripe_webhook_duplicate_ignored", extra={"event_id": event_id})
        return False

    if event_id:
        _processed_webhook_events.add(event_id)

    db = UserRepository()
    event_type = event.get("type", "")
    data = event.get("data", {}).get("object", {})

    logger.info("stripe_webhook_event", extra={"event_type": event_type})

    if event_type == "checkout.session.completed":
        user_id = data.get("metadata", {}).get("trusthire_user_id")
        subscription_id = data.get("subscription")
        plan = data.get("metadata", {}).get("plan", "")
        if user_id and subscription_id:
            await db.update_subscription(user_id, _tier_from_plan(plan), subscription_id, SubscriptionStatus.ACTIVE)

    elif event_type == "customer.subscription.created":
        metadata = data.get("metadata", {})
        user_id = metadata.get("trusthire_user_id")
        sub_id = data.get("id")
        if user_id and sub_id:
            await db.update_subscription(user_id, _tier_from_plan(metadata.get("plan", "pro")), sub_id, SubscriptionStatus.ACTIVE)

    elif event_type in ("customer.subscription.deleted", "customer.subscription.updated"):
        sub_id = data.get("id")
        status = data.get("status", "")
        customer = data.get("customer")
        user = await db.get_by_stripe_customer(customer) if customer else None
        if user:
            if status in ("canceled", "unpaid", "incomplete_expired"):
                await db.update_subscription(user.id, UserTier.FREE, None, SubscriptionStatus.CANCELED)
            elif status in ("active", "trialing", "past_due"):
                await db.update_subscription_status(user.id, SubscriptionStatus(status if status != "trialing" else "active"))

    elif event_type in ("invoice.payment_succeeded", "invoice.payment_failed"):
        customer = data.get("customer")
        user = await db.get_by_stripe_customer(customer) if customer else None
        if user:
            target = SubscriptionStatus.ACTIVE if event_type.endswith("succeeded") else SubscriptionStatus.PAST_DUE
            await db.update_subscription_status(user.id, target)

    return True


@router.post("/webhook", include_in_schema=False)
async def stripe_webhook(request: Request, stripe_signature: Optional[str] = Header(None, alias="stripe-signature")):
    _require_stripe()
    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    payload = await request.body()

    try:
        event = _stripe.Webhook.construct_event(payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET)
    except _stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")
    except Exception as e:
        logger.error(f"stripe_webhook_parse_failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")

    processed = await process_stripe_event(event)
    if not processed:
        return JSONResponse(content={"status": "duplicate"})

    return JSONResponse(content={"status": "success"})
