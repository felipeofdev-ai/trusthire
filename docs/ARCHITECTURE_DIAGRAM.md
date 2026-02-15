# Architecture Diagram (TrustHire)

![TrustHire architecture](./architecture.svg)

## Fluxo resumido
1. Usuário acessa frontend (Vercel/Edge).
2. Requisição vai para API (FastAPI) com autenticação.
3. Camada de análise + billing + observabilidade.
4. Dados operacionais em PostgreSQL + Redis.
5. Logs/métricas para Prometheus/Grafana/Loki.
