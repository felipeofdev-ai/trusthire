# Roadmap Completo — TrustHire Tier‑1 Fortune

## Objetivo
Transformar o TrustHire em SaaS sólido, auditável, escalável e atrativo para recrutamento técnico de alto nível, sem quebrar o template/UX atual.

## Fase 1 — Estabilidade e Segurança (1–2 semanas)
- [x] Headers de segurança (CSP, nosniff, frame deny, etc.)
- [x] Rate limiting base
- [x] Audit logs
- [x] Endpoint de health e métricas
- [ ] Rate limit distribuído com Redis (por IP + token)
- [ ] JWT rotation (access curto + refresh seguro)
- [ ] Device fingerprint + comportamento anômalo por sessão

### Critério de aceite
- 0 regressões funcionais
- ataque de burst 429 em <= 100 req/min por IP
- logs JSON em todos endpoints críticos

## Fase 2 — IA e Resiliência (1–2 semanas)
- [x] Router multi-provider (Claude/GPT/Codex)
- [x] ATS universal + export PDF
- [ ] Circuit breaker para provedores IA
- [ ] Retry exponencial com jitter
- [ ] Feature flags para rollout gradual por rota/provedor

### Critério de aceite
- fallback automático quando provider indisponível
- sem timeout cascata em picos

## Fase 3 — Observabilidade Corporativa (1 semana)
- [ ] OpenTelemetry tracing (HTTP + serviços)
- [ ] Prometheus metrics avançadas
- [ ] Dashboard Grafana (latência, erro, rpm, custo)
- [ ] Alertas (SLO de p95 e error rate)

### SLO inicial
- p95 < 250ms
- error_rate < 1%
- uptime > 99.9%

## Fase 4 — Infra Tier‑1 (2–4 semanas)
- [ ] Cloudflare (WAF + Bot + CDN)
- [ ] Front em Vercel
- [ ] API em App Runner/ECS
- [ ] PostgreSQL gerenciado (RDS/Supabase)
- [ ] Redis gerenciado (ElastiCache/Upstash)
- [ ] Object storage para anexos
- [ ] IaC com Terraform

## Fase 5 — Segurança Avançada e “AI Guardian” (1–2 semanas)
- [ ] Guardian Agent ativo (detecção de anomalia em logs)
- [ ] Auto-blocklist temporária por risco
- [ ] Regras de scraping e bot score
- [ ] Security playbooks (runbook de incidente)

## Fase 6 — Recrutamento e Visibilidade GitHub (contínuo)
- [ ] README técnico com benchmark real
- [ ] ADRs (decisões de arquitetura)
- [ ] Diagramas de fluxo (req, auth, IA, storage)
- [ ] GitHub Project board: Backlog/Building/Testing/Prod
- [ ] Topics do repositório: ai, fastapi, distributed-systems, security, observability
- [ ] Releases com changelog semântico

## Roadmap de execução recomendado (ordem)
1. Redis rate limit distribuído
2. Circuit breaker + retries IA
3. OpenTelemetry + Grafana
4. Cloudflare WAF/Bot + IaC
5. Guardian Agent com auto-ação controlada
6. Benchmarks públicos e portfolio polish
