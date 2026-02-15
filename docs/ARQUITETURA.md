# Arquitetura Técnica TrustHire

## Componentes
- **Frontend:** `index.html` (legado) + integração com `trusthire-frontend` (React/Vite/Next-ready).
- **Backend:** FastAPI com autenticação JWT, análise de risco e billing Stripe.
- **Dados:** PostgreSQL (relacional) + Redis (cache/rate limiting).
- **Observabilidade:** endpoint `/metrics`, logs JSON e healthcheck `/health`.

## Fluxo de requisição
1. Cliente envia mensagem para `POST /api/v1/analyze`.
2. Middleware aplica headers de segurança e coleta latência/erro.
3. Auth valida JWT/API key.
4. Analyzer roda engine de padrões + IA (quando habilitada).
5. Resultado retorna com score e recomendações.
6. Evento de auditoria é registrado (user_id, ação, timestamp, IP, device).

## Pipeline IA
- Entrada sanitizada no servidor.
- Pattern engine gera sinais determinísticos.
- Camada IA (Anthropic) complementa contexto (quando disponível).
- Risk scoring consolida score final (0-100).

## Segurança básica implementada
- JWT + API key.
- Hash de senha com Argon2 (compatível com bcrypt legado).
- Rate limit com `slowapi`.
- Headers CSP, XSS, clickjacking, nosniff.
- Sanitização server-side de inputs textuais.
- Audit logs.

## Infra recomendada
- Docker para build/deploy.
- Railway para runtime público.
- GitHub Actions para CI.
- Prometheus/Grafana para scraping de `/metrics`.


## Blueprint Tier-1 (sem alterar template visual)
- Edge/CDN/WAF: Cloudflare na frente do frontend (Vercel).
- API: FastAPI atrás de gateway + autoscaling container.
- Dados: PostgreSQL + Redis.
- Arquivos: object storage para documentos.
- Segurança: rate limit, headers hardened, validação server-side, audit logs.

## IA Multi-Provider
- `Claude`: análise de risco/scam.
- `GPT`: otimização e reasoning de currículo.
- `Codex`: tarefas técnicas de parsing/code-assist.
- Roteamento centralizado em `ai/router.py`.

## ATS Universal + PDF
- Endpoint: `POST /api/v1/resume/optimize`
- Providers suportados: Workday, Greenhouse, Lever, Taleo, iCIMS, SAP SuccessFactors, SmartRecruiters, BambooHR, Generic.
- Export: `output_format=pdf` retorna arquivo pronto para download.

## Portfólio (recrutamento)
- Públicos recomendados: `frontend/`, `README.md`, `docs/ARQUITETURA.md`, `backend/main.py`, `routes/`, `services/`.
- Privados: `.env`, chaves, `infra/terraform`, pesos/modelos sensíveis.
