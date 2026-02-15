# Stripe Live Setup (TrustHire)

## Segurança primeiro
Se uma chave live foi exposta em chat/commit/log, **rotacione imediatamente** no Stripe Dashboard.

## 1) Configurar variáveis no Railway
- `STRIPE_SECRET_KEY`
- `STRIPE_PUBLISHABLE_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `STRIPE_SUCCESS_URL`
- `STRIPE_CANCEL_URL`
- `STRIPE_TRIAL_DAYS`

## 2) Criar produtos e preços via script
```bash
export STRIPE_SECRET_KEY=sk_live_...
bash scripts/stripe_setup_live.sh
```

O script retorna `STRIPE_PRICE_PRO_MONTHLY` e `STRIPE_PRICE_ENTERPRISE_MONTHLY`.

## 3) Configurar webhook no Stripe
URL recomendada:
- `https://SEU_BACKEND/api/webhooks/stripe`

Eventos obrigatórios:
- `checkout.session.completed`
- `invoice.payment_succeeded`
- `invoice.payment_failed`
- `customer.subscription.created`
- `customer.subscription.deleted`
- `payment_intent.succeeded`
- `payment_intent.payment_failed`

## 4) Validar endpoint
```bash
curl -X POST https://SEU_BACKEND/api/webhooks/stripe
```
Sem assinatura Stripe válida deve retornar `400` (ou `503` se Stripe não configurado).


## 5) Listener local (Stripe CLI)
```bash
bash scripts/stripe_webhook_local_test.sh http://localhost:8000
```

Em outro terminal, simule eventos:
```bash
stripe trigger checkout.session.completed
stripe trigger invoice.payment_succeeded
stripe trigger customer.subscription.deleted
```
