# TrustHire

Job offer and recruitment message analyzer that detects scam indicators using pattern matching and AI.

---

## What it does

Analyzes text from job offers or recruiter messages and returns a risk score (0–100) with detailed breakdown of detected signals:

- Financial requests (payments, crypto, wire transfers)
- Urgency and pressure tactics
- Requests for sensitive personal data
- Unrealistic salary or benefit promises
- Off-platform communication redirects (Telegram, WhatsApp)
- Suspicious URLs and domain reputation
- Phishing and social engineering patterns

---

## Stack

Python · FastAPI · Anthropic Claude API · PostgreSQL · Redis · JWT auth · Docker · Railway

---

## Quickstart

```bash
git clone https://github.com/felipeofdev-ai/trusthire.git
cd trusthire
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# add your ANTHROPIC_API_KEY to .env
uvicorn main:app --reload
```

**Analyze a message:**
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Urgent! Send $500 for job verification. Contact via Telegram.",
    "include_ai_analysis": true,
    "include_link_scan": true
  }'
```

**API docs:** `http://localhost:8000/api/v1/docs`

---

## Docker

```bash
docker-compose up -d
docker-compose logs -f app
```

---

## Testing

```bash
pytest
pytest --cov=. --cov-report=html
```

---

## Configuration

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Claude API key for AI analysis |
| `DATABASE_URL` | No | PostgreSQL connection string |
| `REDIS_URL` | No | Redis for caching |
| `ENV` | No | `dev` / `staging` / `prod` |

See `.env.example` for all options.

---

## Deploy

Configured for Railway deployment:

```bash
npm i -g @railway/cli
export RAILWAY_TOKEN=your_token
./scripts/deploy_real.sh
```

Or trigger via GitHub Actions: `Actions → Deploy Railway → Run workflow`

---

## Monitoring

```bash
docker compose -f docker-compose.monitoring.yml up -d
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3001 (admin/admin)
GET /metrics/prometheus
```

---

## Project structure

```
api/          # FastAPI routes
engine/       # Pattern detection engine
core/         # Configuration, logging
services/     # External services (Anthropic, URL scanning)
models/       # Pydantic models
auth/         # JWT + API key authentication
tests/        # Test suite
```

---

MIT License · [@felipeofdev-ai](https://github.com/felipeofdev-ai)
