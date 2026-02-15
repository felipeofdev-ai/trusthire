# Case Study Técnico — TrustHire

## Problema
Fraudes em recrutamento crescem em canais fora das plataformas oficiais. O objetivo foi construir uma API SaaS para análise de risco com foco em segurança, rastreabilidade e operação real.

## Decisões de arquitetura
1. **FastAPI + camadas**
   - Separação em `api/`, `services/`, `engine/`, `utils/`.
2. **Segurança primeiro**
   - Headers hardening, sanitização server-side, autenticação JWT/API key, webhook Stripe assinado.
3. **Observabilidade nativa**
   - Endpoints `/metrics`, `/metrics/prometheus`, `/system/health`.
4. **Billing de produção**
   - Checkout/Portal Stripe + webhook com idempotência para evitar eventos duplicados.
5. **Evolução orientada a provas públicas**
   - Stack de monitoring (Prometheus/Grafana/Loki), load testing com Locust e benchmark publicado.

## Trade-offs
- **Idempotência de webhook** foi implementada in-memory para ambiente simples; para alta escala, migrar para Redis/PostgreSQL.
- **PDF fallback local** no frontend garante continuidade de UX, mas o caminho principal é backend para consistência e auditoria.

## Resultados técnicos esperados
- Menor risco de inconsistência em billing por duplicidade de eventos Stripe.
- Aumento de confiabilidade operacional com monitoramento e métricas padronizadas.
- Melhor sinal técnico para recrutadores por documentação e benchmark reproduzível.

## Próximos passos de elite
- OpenTelemetry tracing distribuído.
- Circuit breaker para provedores de IA.
- Cache distribuído e fila assíncrona para tarefas pesadas.
- Publicação contínua de benchmark em domínio público.
