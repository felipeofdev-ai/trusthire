#!/bin/bash

# ============================================================
# TrustHire - Script de Setup Automático
# ============================================================
# Este script automatiza a configuração dos 3 repositórios
# Execute: bash setup-trusthire.sh
# ============================================================

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════╗"
echo "║                                                ║"
echo "║        TrustHire - Setup Automático           ║"
echo "║                                                ║"
echo "╚════════════════════════════════════════════════╝"
echo -e "${NC}"

# ============================================================
# 1. VERIFICAR PRÉ-REQUISITOS
# ============================================================

echo -e "${YELLOW}[1/7] Verificando pré-requisitos...${NC}"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 não encontrado. Por favor, instale Python 3.8+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $(python3 --version | cut -d' ' -f2) encontrado${NC}"

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js não encontrado. Por favor, instale Node.js 16+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js $(node --version) encontrado${NC}"

# Verificar npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm não encontrado. Por favor, instale npm${NC}"
    exit 1
fi
echo -e "${GREEN}✓ npm $(npm --version) encontrado${NC}"

# Verificar git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git não encontrado. Por favor, instale git${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Git $(git --version | cut -d' ' -f3) encontrado${NC}"

echo ""

# ============================================================
# 2. CRIAR DIRETÓRIO DE PROJETOS
# ============================================================

echo -e "${YELLOW}[2/7] Criando estrutura de diretórios...${NC}"

PROJECT_DIR="$HOME/trusthire-projects"

if [ ! -d "$PROJECT_DIR" ]; then
    mkdir -p "$PROJECT_DIR"
    echo -e "${GREEN}✓ Diretório criado: $PROJECT_DIR${NC}"
else
    echo -e "${GREEN}✓ Diretório já existe: $PROJECT_DIR${NC}"
fi

cd "$PROJECT_DIR"
echo ""

# ============================================================
# 3. CLONAR REPOSITÓRIOS
# ============================================================

echo -e "${YELLOW}[3/7] Clonando repositórios do GitHub...${NC}"

# Repositório 1: Original
if [ ! -d "trusthire" ]; then
    echo -e "${BLUE}Clonando trusthire (original)...${NC}"
    git clone https://github.com/felipeofdev-ai/trusthire.git
    echo -e "${GREEN}✓ trusthire clonado${NC}"
else
    echo -e "${GREEN}✓ trusthire já existe${NC}"
fi

# Repositório 2: Backend
if [ ! -d "trusthire-backend" ]; then
    echo -e "${BLUE}Clonando trusthire-backend...${NC}"
    git clone https://github.com/felipeofdev-ai/trusthire-backend.git
    echo -e "${GREEN}✓ trusthire-backend clonado${NC}"
else
    echo -e "${GREEN}✓ trusthire-backend já existe${NC}"
fi

# Repositório 3: Frontend
if [ ! -d "trusthire-frontend" ]; then
    echo -e "${BLUE}Clonando trusthire-frontend...${NC}"
    git clone https://github.com/felipeofdev-ai/trusthire-frontend.git
    echo -e "${GREEN}✓ trusthire-frontend clonado${NC}"
else
    echo -e "${GREEN}✓ trusthire-frontend já existe${NC}"
fi

echo ""

# ============================================================
# 4. CONFIGURAR BACKEND
# ============================================================

echo -e "${YELLOW}[4/7] Configurando backend...${NC}"

cd "$PROJECT_DIR/trusthire-backend"

# Criar ambiente virtual Python
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Criando ambiente virtual Python...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Ambiente virtual criado${NC}"
fi

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}Instalando dependências Python...${NC}"
    pip install --quiet --upgrade pip
    pip install --quiet -r requirements.txt
    echo -e "${GREEN}✓ Dependências instaladas${NC}"
else
    echo -e "${RED}⚠️  requirements.txt não encontrado${NC}"
fi

# Criar .env se não existir
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Criando arquivo .env...${NC}"
    cat > .env << EOF
# TrustHire Backend - Configuração
ANTHROPIC_API_KEY=sua-chave-anthropic-aqui
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
STRIPE_SECRET_KEY=sua-chave-stripe-aqui
STRIPE_WEBHOOK_SECRET=seu-webhook-secret-aqui
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://localhost:8080
DATABASE_URL=sqlite:///./trusthire.db
ENVIRONMENT=development
PORT=8000
LOG_LEVEL=INFO
FREE_ANALYSES_PER_DAY=3
DEFAULT_LANGUAGE=pt
SUPPORTED_LANGUAGES=pt,en,es
EOF
    echo -e "${GREEN}✓ Arquivo .env criado${NC}"
    echo -e "${YELLOW}⚠️  IMPORTANTE: Edite o arquivo .env e adicione suas API keys!${NC}"
else
    echo -e "${GREEN}✓ Arquivo .env já existe${NC}"
fi

deactivate
echo ""

# ============================================================
# 5. CONFIGURAR FRONTEND
# ============================================================

echo -e "${YELLOW}[5/7] Configurando frontend...${NC}"

cd "$PROJECT_DIR/trusthire-frontend"

# Instalar dependências
if [ -f "package.json" ]; then
    echo -e "${BLUE}Instalando dependências Node.js...${NC}"
    npm install --silent
    echo -e "${GREEN}✓ Dependências instaladas${NC}"
else
    echo -e "${RED}⚠️  package.json não encontrado${NC}"
fi

# Criar .env se não existir
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Criando arquivo .env...${NC}"
    cat > .env << EOF
VITE_API_URL=http://localhost:8000
VITE_STRIPE_PUBLIC_KEY=sua-chave-publica-stripe-aqui
EOF
    echo -e "${GREEN}✓ Arquivo .env criado${NC}"
    echo -e "${YELLOW}⚠️  IMPORTANTE: Edite o arquivo .env e adicione suas chaves!${NC}"
else
    echo -e "${GREEN}✓ Arquivo .env já existe${NC}"
fi

echo ""

# ============================================================
# 6. CRIAR SCRIPTS DE INICIALIZAÇÃO
# ============================================================

echo -e "${YELLOW}[6/7] Criando scripts de inicialização...${NC}"

# Script para iniciar backend
cd "$PROJECT_DIR/trusthire-backend"
cat > start-backend.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
echo "🚀 Iniciando TrustHire Backend..."
echo "📍 URL: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
python main.py
EOF
chmod +x start-backend.sh
echo -e "${GREEN}✓ Script start-backend.sh criado${NC}"

# Script para iniciar frontend
cd "$PROJECT_DIR/trusthire-frontend"
cat > start-frontend.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "🚀 Iniciando TrustHire Frontend..."
echo "📍 URL: http://localhost:3000"
npm run dev
EOF
chmod +x start-frontend.sh
echo -e "${GREEN}✓ Script start-frontend.sh criado${NC}"

# Script para iniciar tudo
cd "$PROJECT_DIR"
cat > start-all.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"

echo "╔════════════════════════════════════════════════╗"
echo "║      Iniciando TrustHire - Todos os Serviços  ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Função para iniciar um serviço em background
start_service() {
    local name=$1
    local script=$2
    local log=$3
    
    echo "🚀 Iniciando $name..."
    cd "$script" && ./start-*.sh > "$log" 2>&1 &
    echo "   PID: $!"
    cd - > /dev/null
}

# Criar diretório de logs
mkdir -p logs

# Iniciar backend
start_service "Backend" "trusthire-backend" "logs/backend.log"
sleep 2

# Iniciar frontend
start_service "Frontend" "trusthire-frontend" "logs/frontend.log"
sleep 2

echo ""
echo "✅ Todos os serviços foram iniciados!"
echo ""
echo "📍 URLs:"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Logs:"
echo "   Backend:  tail -f logs/backend.log"
echo "   Frontend: tail -f logs/frontend.log"
echo ""
echo "🛑 Para parar todos os serviços:"
echo "   killall -9 node python"
EOF
chmod +x start-all.sh
echo -e "${GREEN}✓ Script start-all.sh criado${NC}"

echo ""

# ============================================================
# 7. RESUMO E INSTRUÇÕES FINAIS
# ============================================================

echo -e "${YELLOW}[7/7] Setup concluído!${NC}"
echo ""

echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                ║${NC}"
echo -e "${GREEN}║              ✅ SETUP CONCLUÍDO!               ║${NC}"
echo -e "${GREEN}║                                                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}📁 Estrutura criada:${NC}"
echo "   $PROJECT_DIR/"
echo "   ├── trusthire/           (projeto original)"
echo "   ├── trusthire-backend/   (API backend)"
echo "   ├── trusthire-frontend/  (React frontend)"
echo "   ├── start-all.sh         (inicia tudo)"
echo "   └── logs/                (logs dos serviços)"
echo ""

echo -e "${YELLOW}⚠️  PRÓXIMOS PASSOS OBRIGATÓRIOS:${NC}"
echo ""
echo "1️⃣  Configure as API Keys no backend:"
echo "   ${BLUE}cd $PROJECT_DIR/trusthire-backend${NC}"
echo "   ${BLUE}nano .env${NC}"
echo "   Adicione:"
echo "   - ANTHROPIC_API_KEY (https://console.anthropic.com/)"
echo "   - STRIPE_SECRET_KEY (https://dashboard.stripe.com/)"
echo ""

echo "2️⃣  Configure as chaves no frontend:"
echo "   ${BLUE}cd $PROJECT_DIR/trusthire-frontend${NC}"
echo "   ${BLUE}nano .env${NC}"
echo "   Adicione:"
echo "   - VITE_STRIPE_PUBLIC_KEY"
echo ""

echo "3️⃣  Inicie os serviços:"
echo "   ${GREEN}cd $PROJECT_DIR${NC}"
echo "   ${GREEN}./start-all.sh${NC}"
echo ""

echo "4️⃣  Acesse as URLs:"
echo "   Backend:  ${BLUE}http://localhost:8000${NC}"
echo "   Frontend: ${BLUE}http://localhost:3000${NC}"
echo "   API Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo ""

echo -e "${BLUE}📚 Documentação:${NC}"
echo "   Guia completo: $PROJECT_DIR/GUIA_INTEGRACAO_TRUSTHIRE.md"
echo ""

echo -e "${GREEN}🎉 Tudo pronto para começar!${NC}"
echo ""

# Opcional: Abrir diretório no explorador de arquivos
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$PROJECT_DIR"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$PROJECT_DIR" 2>/dev/null || true
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    explorer "$PROJECT_DIR"
fi
