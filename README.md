<div align="center">

# 🛡️ TrustHire

### AI that protects professionals before they apply

[![Live](https://img.shields.io/badge/demo-analyze_API-4DE8C2?style=for-the-badge)](https://github.com/felipeofdev-ai/trusthire)
[![Stack](https://img.shields.io/badge/Python-FastAPI-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/felipeofdev-ai/trusthire)
[![AI](https://img.shields.io/badge/Claude-Anthropic-D66BFF?style=for-the-badge)](https://www.anthropic.com)
[![Stars](https://img.shields.io/github/stars/felipeofdev-ai/trusthire?style=for-the-badge)](https://github.com/felipeofdev-ai/trusthire/stargazers)

**Paste a job offer or recruiter DM → get a risk score (0–100) with explainable signals.**  
Built so people don’t lose money or data to hiring scams.

[Portfolio RPG](https://felipeofdev-ai.github.io/) · [Backend](https://github.com/felipeofdev-ai/trusthire-backend) · [Frontend](https://github.com/felipeofdev-ai/trusthire-frontend) · [Author](https://github.com/felipeofdev-ai)

</div>

---

## Why this quest exists

Recruitment fraud is a real boss fight: fake offers, “pay for onboarding”, crypto fees, Telegram redirects.  
TrustHire is a **production-shaped** analyzer — heuristics + optional Claude — that returns **citations you can trust**, not vibes.

## What it detects

| Signal class | Examples |
|---|---|
| Financial pressure | wire, crypto, “verification fee” |
| Urgency tactics | “hire today or lose the role” |
| PII harvesting | SSN, bank login, passport dumps |
| Unrealistic bait | inflated salary / benefits |
| Off-platform redirect | Telegram / WhatsApp-only hiring |
| Link / domain risk | phishing patterns, shady hosts |

## Stack

`Python` · `FastAPI` · `Anthropic Claude` · `PostgreSQL` · `Redis` · `JWT` · `Docker` · `Stripe` (SaaS path)

## Quickstart

```bash
git clone https://github.com/felipeofdev-ai/trusthire.git
cd trusthire
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # set ANTHROPIC_API_KEY
uvicorn main:app --reload
```

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Urgent! Send $500 for job verification. Contact via Telegram.",
    "include_ai_analysis": true,
    "include_link_scan": true
  }'
```

API docs: `http://localhost:8000/api/v1/docs`

## Docker

```bash
docker-compose up -d
docker-compose logs -f app
```

## Tests

```bash
pytest
pytest --cov=. --cov-report=html
```

## Config

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Claude for AI analysis |
| `DATABASE_URL` | No | PostgreSQL |
| `REDIS_URL` | No | Cache |
| `ENV` | No | `dev` / `staging` / `prod` |

## Ecosystem

| Repo | Role |
|---|---|
| [trusthire](https://github.com/felipeofdev-ai/trusthire) | Core analyzer (this repo) |
| [trusthire-backend](https://github.com/felipeofdev-ai/trusthire-backend) | SaaS API + Stripe |
| [trusthire-frontend](https://github.com/felipeofdev-ai/trusthire-frontend) | Product UI |

---

<p align="center">
  <b>If this helped you or your team — ⭐ the repo.</b><br/>
  Stars help recruiters and candidates find tools that put <i>trust before apply</i>.
</p>

<p align="center">
  Made by <a href="https://github.com/felipeofdev-ai">Felipe Fernandes</a> · Systems & Agentic AI Engineer
</p>
