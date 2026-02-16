# 🛡️ TrustHire

> **Verify before you trust.**

AI-powered job offer verification system that detects scam indicators in recruitment messages.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Redis (optional, for caching)
- PostgreSQL (optional, for persistence)

### Installation

```bash
# Clone repository
git clone https://github.com/your-username/trusthire.git
cd trusthire

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Running

```bash
# Development mode
python main.py

# Or with uvicorn
uvicorn main:app --reload

# Production mode
ENV=prod uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

```bash
# Build and run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f app
```

## 📚 API Documentation

Once running, visit:
- Interactive API docs: http://localhost:8000/api/v1/docs
- Alternative docs: http://localhost:8000/api/v1/redoc

### Example API Call

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Urgent! Send $500 for job verification. Contact via Telegram.",
    "include_ai_analysis": true,
    "include_link_scan": true
  }'
```

## 🎯 Features

### Core Analysis
- ✅ Pattern-based scam detection
- ✅ AI-powered contextual analysis (Claude)
- ✅ Risk scoring (0-100)
- ✅ Confidence assessment
- ✅ Social engineering detection
- ✅ URL/link analysis
- ✅ Domain reputation checking

### Detection Categories
- 💰 Financial requests (payments, crypto)
- ⏰ Urgency pressure tactics
- 🔐 Sensitive data requests
- 🎁 Unrealistic promises
- 📱 Off-platform communication
- 🔗 Suspicious links
- 🎣 Phishing patterns
- 🧠 Social engineering

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────────────────┐
│   FastAPI Application   │
├─────────────────────────┤
│  ┌─────────────────┐   │
│  │ Pattern Engine  │   │
│  ├─────────────────┤   │
│  │ Risk Scoring    │   │
│  ├─────────────────┤   │
│  │ Link Analyzer   │   │
│  ├─────────────────┤   │
│  │ AI Layer        │   │
│  └─────────────────┘   │
└─────────────────────────┘
       │
┌──────▼──────┬────────────┐
│   Redis     │ PostgreSQL │
│   (Cache)   │   (Data)   │
└─────────────┴────────────┘
```


## 🚀 Deploy real (produção)

Para publicar a API de forma **real** no Railway com validação automática de healthcheck:

```bash
# Linux/macOS
npm i -g @railway/cli
export RAILWAY_TOKEN=seu_token
./scripts/deploy_real.sh
```

```powershell
# Windows (PowerShell)
npm i -g @railway/cli
$env:RAILWAY_TOKEN="seu_token"
.\scripts\deploy_real.ps1
```

Se o PowerShell bloquear execução de script local, rode antes:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

O script:
- valida pré-requisitos e estado limpo do Git;
- roda testes (`pytest -q`) antes da publicação;
- executa `railway up --ci`;
- detecta domínio público e valida `/health` até ficar online.

Se a detecção automática do domínio falhar, informe manualmente:

```bash
PUBLIC_API_URL=https://seu-app.up.railway.app ./scripts/deploy_real.sh
```

```powershell
.\scripts\deploy_real.ps1 -PublicApiUrl "https://seu-app.up.railway.app"
```

### Deploy direto pelo GitHub Actions

Você também pode publicar sem rodar nada localmente:

1. No GitHub do repositório, vá em **Settings → Secrets and variables → Actions** e crie:
   - `RAILWAY_TOKEN` (**obrigatório**)
   - `PUBLIC_API_URL` (recomendado, ex: `https://seu-app.up.railway.app`)
   - `RAILWAY_PROJECT_ID` (opcional)
   - `RAILWAY_ENVIRONMENT_ID` (opcional)
   - `RAILWAY_SERVICE_ID` (opcional)
2. Vá em **Actions → Deploy Railway → Run workflow**.
3. (Opcional) Preencha `public_api_url` no dispatch manual.
4. O workflow executa `./scripts/deploy_real.sh`, roda testes, faz deploy e valida `/health`.

Arquivo do workflow: `.github/workflows/deploy-railway.yml`.

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Specific test file
pytest tests/test_analyzer.py -v
```

## 📈 Configuration

Key environment variables:

- `ANTHROPIC_API_KEY` - Required for AI analysis
- `REDIS_URL` - Optional, for caching
- `DATABASE_URL` - Optional, for persistence
- `ENV` - Environment (dev/staging/prod)
- `LOG_LEVEL` - Logging level (INFO/DEBUG/WARNING)

See `.env.example` for all options.

## 🛠️ Development

### Project Structure

```
trusthire/
├── api/          # API routes and endpoints
├── core/         # Core analysis logic
├── engine/       # Detection engines
├── models/       # Pydantic models
├── services/     # External services
├── utils/        # Utilities
├── tests/        # Test suite
└── config.py     # Configuration
```

### Adding New Patterns

Edit `engine/pattern_engine.py`:

```python
PatternRule(
    pattern=re.compile(r"your-regex-here", re.I),
    category=SignalCategory.YOUR_CATEGORY,
    message="Description of what was detected",
    severity=Severity.HIGH,
    confidence=0.90,
)
```

## 📊 Monitoring

- Health check: `GET /health`
- Metrics: `GET /api/v1/stats`
- Structured JSON logging
- Sentry integration (optional)

## 🔒 Security

- Rate limiting per tier
- Input sanitization
- Secure headers
- CORS configuration
- API key authentication (enterprise)

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📧 Support

- Issues: [GitHub Issues](https://github.com/your-username/trusthire/issues)
- Discussions: [GitHub Discussions](https://github.com/your-username/trusthire/discussions)

---

**Built with ❤️ to protect job seekers from scams**


## ✅ Production Readiness Checklist

- Deploy público online: Railway (`render.yaml`/`railway.toml`) e health endpoint `/health`.
- Login real: JWT com refresh token e API keys.
- Banco real: suporte a PostgreSQL via `DATABASE_URL`.
- API documentada: Swagger em `/api/v1/docs`.
- Testes unitários: suíte `tests/` + CI em `.github/workflows/ci.yml`.
- Monitoramento e métricas: endpoint `/metrics` com uptime, latência média/p95, RPM e taxa de erro.
- Segurança básica: rate limiting, headers CSP/XSS, sanitização server-side e hash Argon2.

## Stripe (modo real)
1. No Dashboard Stripe, trocar para **Live mode**.
2. Configurar variáveis no Railway:
   - `STRIPE_SECRET_KEY`
   - `STRIPE_PUBLISHABLE_KEY`
   - `STRIPE_WEBHOOK_SECRET`
3. Criar produtos/preços live e preencher os `STRIPE_PRICE_*`.
4. Validar checkout no endpoint `/api/v1/billing`.

## Railway (produção)
1. Definir variáveis de ambiente de produção (`ENV=prod`, `SECRET_KEY`, `DATABASE_URL`, `REDIS_URL`).
2. Garantir `CORS_ORIGINS_STR` com domínio público do frontend.
3. Monitorar `/health` e `/metrics` no painel de observabilidade.


## 🚀 Deploy de Produção (script completo)

```bash
bash scripts/deploy_production.sh
```

Variáveis opcionais:
- `REGISTRY_URI` (ex: ECR/GHCR)
- `IMAGE_TAG` (default: `latest`)

## 📈 Monitoramento pronto + Dashboard pronto

```bash
docker compose -f docker-compose.monitoring.yml up -d
```

Acessos:
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001` (`admin/admin`)
- Loki: `http://localhost:3100`

Métricas Prometheus da API:
- `GET /metrics/prometheus`

## ⚡ Load test pronto

```bash
bash scripts/run_load_test.sh http://localhost:8000
```

Saída de benchmark:
- `loadtest/results/benchmark.md`
- CSVs do Locust em `loadtest/results/`


## 💳 Stripe Live (produção)

Guia operacional completo em `docs/STRIPE_LIVE_SETUP.md`.

Script para criação de produtos/preços live:
```bash
export STRIPE_SECRET_KEY=sk_live_...
bash scripts/stripe_setup_live.sh
```


Teste local do webhook com Stripe CLI:
```bash
bash scripts/stripe_webhook_local_test.sh http://localhost:8000
```


## 🌐 Provas Públicas de Senioridade

### Demo pública
- Live Demo: `https://app.trusthire.ai` (configure apontamento para seu deploy em produção)

### Screenshot do dashboard
- Suba a stack de monitoramento:
```bash
docker compose -f docker-compose.monitoring.yml up -d
```
- Acesse Grafana em `http://localhost:3001` e exporte screenshot do dashboard "TrustHire Production Overview".

### Benchmark publicado
```bash
bash scripts/run_load_test.sh http://localhost:8000
python scripts/generate_benchmark_summary.py
```
- Resultado público em: `docs/BENCHMARK_PUBLIC.md`

### Architecture diagram
- Arquitetura: `docs/ARCHITECTURE_DIAGRAM.md`
- Diagrama SVG: `docs/architecture.svg`

### Case study técnico
- Documento: `docs/CASE_STUDY_TECHNICAL.md`
