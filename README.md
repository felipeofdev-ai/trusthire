> **Live demo:** https://felipeofdev-ai.github.io/labs/trusthire/

<div align="center">

# ðŸ›¡ï¸ TrustHire

### AI that protects professionals before they apply

[![Live](https://img.shields.io/badge/demo-analyze_API-4DE8C2?style=for-the-badge)](https://github.com/felipeofdev-ai/trusthire)
[![Stack](https://img.shields.io/badge/Python-FastAPI-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/felipeofdev-ai/trusthire)
[![AI](https://img.shields.io/badge/Claude-Anthropic-D66BFF?style=for-the-badge)](https://www.anthropic.com)
[![Stars](https://img.shields.io/github/stars/felipeofdev-ai/trusthire?style=for-the-badge)](https://github.com/felipeofdev-ai/trusthire/stargazers)

**Paste a job offer or recruiter DM â†’ get a risk score (0â€“100) with explainable signals.**  
Built so people donâ€™t lose money or data to hiring scams.

[Portfolio RPG](https://felipeofdev-ai.github.io/) Â· [Backend](https://github.com/felipeofdev-ai/trusthire-backend) Â· [Frontend](https://github.com/felipeofdev-ai/trusthire-frontend) Â· [Author](https://github.com/felipeofdev-ai)

</div>

---

## Why this quest exists

Recruitment fraud is a real boss fight: fake offers, â€œpay for onboardingâ€, crypto fees, Telegram redirects.  
TrustHire is a **production-shaped** analyzer â€” heuristics + optional Claude â€” that returns **citations you can trust**, not vibes.

## What it detects

| Signal class | Examples |
|---|---|
| Financial pressure | wire, crypto, â€œverification feeâ€ |
| Urgency tactics | â€œhire today or lose the roleâ€ |
| PII harvesting | SSN, bank login, passport dumps |
| Unrealistic bait | inflated salary / benefits |
| Off-platform redirect | Telegram / WhatsApp-only hiring |
| Link / domain risk | phishing patterns, shady hosts |

## Stack

`Python` Â· `FastAPI` Â· `Anthropic Claude` Â· `PostgreSQL` Â· `Redis` Â· `JWT` Â· `Docker` Â· `Stripe` (SaaS path)

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
  <b>If this helped you or your team â€” â­ the repo.</b><br/>
  Stars help recruiters and candidates find tools that put <i>trust before apply</i>.
</p>

<p align="center">
  Made by <a href="https://github.com/felipeofdev-ai">Felipe Fernandes</a> Â· Systems & Agentic AI Engineer
</p>

---

## Live demo

**Try it in the browser (no clone):** see badge / homepage above, or the [Labs hub](https://felipeofdev-ai.github.io/labs/).

## Constellation

| Project | Demo |
|---------|------|
| [CardOpsAI](https://github.com/felipeofdev-ai/CardOpsAI) | [lab](https://felipeofdev-ai.github.io/labs/cardopsai/) |
| [BridgeTrace-AI](https://github.com/felipeofdev-ai/BridgeTrace-AI) | [lab](https://felipeofdev-ai.github.io/labs/bridgetrace/) |
| [Meridian](https://github.com/felipeofdev-ai/Meridian) | [lab](https://felipeofdev-ai.github.io/labs/meridian/) |
| [TrustHire](https://github.com/felipeofdev-ai/trusthire) | [lab](https://felipeofdev-ai.github.io/labs/trusthire/) |
| [secure-ship-kit](https://github.com/felipeofdev-ai/secure-ship-kit) | [lab](https://felipeofdev-ai.github.io/labs/secure-ship-kit/) |
| [agentic-rag-cite](https://github.com/felipeofdev-ai/agentic-rag-cite) | [lab](https://felipeofdev-ai.github.io/labs/agentic-rag-cite/) |
| [hitl-langgraph-kit](https://github.com/felipeofdev-ai/hitl-langgraph-kit) | [lab](https://felipeofdev-ai.github.io/labs/hitl-langgraph-kit/) |
| [forge-mcp-server](https://github.com/felipeofdev-ai/forge-mcp-server) | [lab](https://felipeofdev-ai.github.io/labs/forge-mcp-server/) |
| [agent-eval-harness](https://github.com/felipeofdev-ai/agent-eval-harness) | [lab](https://felipeofdev-ai.github.io/labs/agent-eval-harness/) |
| [lgpd-checklist-agent](https://github.com/felipeofdev-ai/lgpd-checklist-agent) | [lab](https://felipeofdev-ai.github.io/labs/lgpd-checklist-agent/) |
| [hiring-packet](https://github.com/felipeofdev-ai/hiring-packet) | [lab](https://felipeofdev-ai.github.io/labs/hiring-packet/) |
| [philo-ai-os](https://github.com/felipeofdev-ai/philo-ai-os) | [lab](https://felipeofdev-ai.github.io/labs/philo-ai-os/) |
| [balcaoia-local](https://github.com/felipeofdev-ai/balcaoia-local) | [studio](https://balcaoia-studio.vercel.app) |

Portfolio: [felipeofdev-ai.github.io](https://felipeofdev-ai.github.io/) · Author: Felipe Fernandes · `felipe.of.dev@gmail.com`

> If this helped you, **star this repo** — organic only. No bots, no paid stars.