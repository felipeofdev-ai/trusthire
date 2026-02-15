# 🚀 TrustHire - Guia Rápido de Integração


## ✅ Integração automática (recomendado)

No repositório `trusthire`, execute:

```bash
bash scripts/link_trusthire_ecossistema.sh
```

Esse script:
- clona/atualiza `trusthire-backend` e `trusthire-frontend` como diretórios irmãos;
- ajusta `ALLOWED_ORIGINS` no backend para aceitar frontend React e `index.html`;
- cria `trusthire-frontend/.env.local` apontando para `http://localhost:8000/api/v1`.

Depois, suba os 3 serviços conforme instruções exibidas pelo script.

---

## ⚡ Setup em 5 Minutos

### 1️⃣ Clone os 3 Repositórios

```bash
cd ~/projects

# Repositório 1: Projeto original
git clone https://github.com/felipeofdev-ai/trusthire.git

# Repositório 2: Backend separado
git clone https://github.com/felipeofdev-ai/trusthire-backend.git

# Repositório 3: Frontend React separado
git clone https://github.com/felipeofdev-ai/trusthire-frontend.git
```

---

### 2️⃣ Configure o Backend

```bash
cd trusthire-backend

# 1. Copie os arquivos do projeto premium
# (use os arquivos de trusthire-ultimate-complete/backend/)

# 2. Crie o arquivo .env
cp .env.example .env
# Edite o .env e adicione suas chaves da Anthropic e Stripe

# 3. Instale as dependências
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt

# 4. Inicie o backend
python main.py
```

✅ Backend rodando em: http://localhost:8000

---

### 3️⃣ Configure o Frontend React

```bash
cd trusthire-frontend

# 1. Copie os arquivos do projeto premium
# (use os arquivos de trusthire-ultimate-complete/frontend/)

# 2. Crie o arquivo .env
echo "VITE_API_URL=http://localhost:8000" > .env

# 3. Instale as dependências
npm install

# 4. Inicie o frontend
npm run dev
```

✅ Frontend rodando em: http://localhost:3000

---

### 4️⃣ Integre o index.html Original

```bash
cd trusthire

# 1. Abra o index.html
# 2. No final do arquivo, antes de </body>, adicione:
```

```html
<script src="https://raw.githubusercontent.com/seu-usuario/trusthire/main/api-integration.js"></script>
```

**OU** copie todo o conteúdo do arquivo `api-integration.js` diretamente no `index.html`.

✅ Interface original integrada!

---

## 🎯 Testar a Integração

### Teste 1: Backend está funcionando?
```bash
curl http://localhost:8000/health
# Deve retornar: {"status":"online","version":"2.0.0"}
```

### Teste 2: Frontend conecta ao Backend?
1. Acesse http://localhost:3000
2. Tente fazer login ou registro
3. Analise uma mensagem de teste

### Teste 3: index.html conecta ao Backend?
1. Abra http://localhost:8080 (ou sirva o index.html)
2. Cole uma mensagem no analisador
3. Clique em "Analisar"
4. Deve chamar a API em http://localhost:8000/api/analyze

---

## 📝 Estrutura de Arquivos Necessários

### trusthire-backend/
```
.env                    # ⚠️ Configure suas API keys aqui
main.py                 # Entry point
api/
  ├── analysis.py       # Análise de mensagens
  ├── auth.py           # Autenticação
  ├── billing.py        # Pagamentos Stripe
  └── resume.py         # Otimização de currículos
core/
  └── analyzer.py       # Lógica principal
engine/
  ├── ai_layer.py       # Claude AI
  ├── pattern_engine.py # Detecção de padrões
  └── risk_scoring.py   # Cálculo de risco
models/
services/
requirements.txt
```

### trusthire-frontend/
```
.env                    # Configure VITE_API_URL aqui
package.json
src/
  ├── components/       # Componentes React
  ├── services/
  │   └── api.ts        # ⚠️ Configuração Axios
  ├── pages/
  └── types/
```

### trusthire/
```
index.html              # ⚠️ Adicione api-integration.js aqui
```

---

## 🔑 Variáveis de Ambiente Obrigatórias

### Backend (.env)
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...        # Obrigatório
SECRET_KEY=sua-chave-jwt-aleatoria        # Obrigatório
STRIPE_SECRET_KEY=sk_test_...             # Para pagamentos
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000        # Obrigatório
VITE_STRIPE_PUBLIC_KEY=pk_test_...        # Para pagamentos
```

---

## 🚨 Problemas Comuns

### ❌ Erro: "Failed to fetch" no frontend
**Solução:** Verifique se o backend está rodando e se o CORS está configurado:

```python
# trusthire-backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### ❌ Erro: "401 Unauthorized"
**Solução:** O token JWT não está sendo enviado. Verifique se:
1. Você fez login
2. O token está no localStorage
3. O header Authorization está sendo enviado

### ❌ Backend não inicia
**Solução:** Faltam dependências ou variáveis de ambiente:
```bash
pip install -r requirements.txt
cat .env  # Verifique se todas as variáveis existem
```

---

## 📦 Deploy para Produção

### Backend (Railway)
```bash
cd trusthire-backend
railway login
railway init
railway up
```

Configure as variáveis de ambiente no painel do Railway.

### Frontend (Vercel)
```bash
cd trusthire-frontend
vercel
```

Configure `VITE_API_URL` para a URL do Railway no painel da Vercel.

### Atualizar index.html
Mude a `baseURL` no código JavaScript:
```javascript
const API_CONFIG = {
  baseURL: 'https://trusthire-backend.up.railway.app',
  // ...
};
```

---

## 📚 Próximos Passos

1. ✅ Teste localmente tudo funcionando
2. ✅ Configure Stripe para pagamentos
3. ✅ Adicione suas chaves da Anthropic
4. ✅ Faça deploy do backend
5. ✅ Faça deploy do frontend
6. ✅ Atualize URLs de produção
7. ✅ Teste em produção

---

## 🆘 Precisa de Ajuda?

- **Documentação Completa:** Veja `GUIA_INTEGRACAO_TRUSTHIRE.md`
- **Backend API Docs:** http://localhost:8000/docs
- **GitHub Issues:** Abra uma issue no repositório relevante

---

## ✨ Features Integradas

✅ **Análise de Mensagens** - Detecta scams com IA  
✅ **Autenticação JWT** - Login/registro seguro  
✅ **Otimização de Currículo** - Upload e análise de CVs  
✅ **Pagamentos Stripe** - Planos PRO e Enterprise  
✅ **Multi-idioma** - PT, EN, ES  
✅ **Rate Limiting** - Proteção contra abuso  
✅ **CORS Configurado** - Frontend e backend comunicam  

---

Feito com ❤️ para TrustHire
