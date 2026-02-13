# 📚 TrustHire - Exemplos de Uso da API

## 🎯 Exemplos Práticos de Integração

Este documento contém exemplos de código prontos para usar nas diferentes partes da aplicação.

---

## 1. 🔐 AUTENTICAÇÃO

### 1.1 Registro de Novo Usuário

```javascript
// No index.html
async function handleRegister() {
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  
  try {
    const response = await fetch('http://localhost:8000/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name, email, password })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // Salvar token
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      
      alert('Conta criada com sucesso!');
      window.location.reload();
    } else {
      alert('Erro: ' + data.detail);
    }
  } catch (error) {
    console.error('Erro no registro:', error);
    alert('Erro ao criar conta. Tente novamente.');
  }
}
```

### 1.2 Login

```javascript
// No index.html
async function handleLogin() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  
  try {
    const response = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      
      alert('Login realizado com sucesso!');
      window.location.reload();
    } else {
      alert('Email ou senha incorretos.');
    }
  } catch (error) {
    console.error('Erro no login:', error);
    alert('Erro ao fazer login. Tente novamente.');
  }
}
```

### 1.3 Verificar se Está Logado

```javascript
// No index.html
function checkAuth() {
  const token = localStorage.getItem('token');
  const user = localStorage.getItem('user');
  
  if (token && user) {
    const userData = JSON.parse(user);
    updateUIForLoggedUser(userData);
    return true;
  }
  
  return false;
}

// Executar ao carregar a página
window.addEventListener('DOMContentLoaded', checkAuth);
```

---

## 2. 🔍 ANÁLISE DE MENSAGENS

### 2.1 Análise Simples

```javascript
// No index.html
async function analyzeMessage() {
  const message = document.getElementById('message-input').value;
  const token = localStorage.getItem('token');
  
  if (!message.trim()) {
    alert('Por favor, cole uma mensagem para analisar.');
    return;
  }
  
  try {
    showLoading(true);
    
    const response = await fetch('http://localhost:8000/api/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        message: message,
        language: 'pt'
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      displayResults(data);
    } else if (response.status === 401) {
      alert('Sua sessão expirou. Por favor, faça login novamente.');
      localStorage.clear();
      window.location.reload();
    } else if (response.status === 403) {
      alert('Você atingiu o limite de análises gratuitas. Faça upgrade para continuar!');
      showUpgradeModal();
    } else {
      alert('Erro: ' + data.detail);
    }
  } catch (error) {
    console.error('Erro na análise:', error);
    alert('Erro ao analisar mensagem. Tente novamente.');
  } finally {
    showLoading(false);
  }
}
```

### 2.2 Exibir Resultados com Score Visual

```javascript
// No index.html
function displayResults(data) {
  const resultsDiv = document.getElementById('results');
  
  // Determinar cor baseada no score
  const getColor = (score) => {
    if (score >= 80) return '#ff4747';  // Vermelho
    if (score >= 60) return '#ff9f0a';  // Laranja
    if (score >= 40) return '#ffd60a';  // Amarelo
    return '#34c759';                   // Verde
  };
  
  const getRiskLabel = (score) => {
    if (score >= 80) return 'RISCO CRÍTICO';
    if (score >= 60) return 'RISCO ALTO';
    if (score >= 40) return 'RISCO MODERADO';
    if (score >= 20) return 'RISCO BAIXO';
    return 'SEGURO';
  };
  
  resultsDiv.innerHTML = `
    <div class="analysis-result">
      <!-- Score Principal -->
      <div class="score-display">
        <div class="score-circle" style="border-color: ${getColor(data.risk_score)}">
          <span class="score-number" style="color: ${getColor(data.risk_score)}">
            ${data.risk_score}
          </span>
          <span class="score-label">${getRiskLabel(data.risk_score)}</span>
        </div>
      </div>
      
      <!-- Barra de Progresso -->
      <div class="progress-bar">
        <div class="progress-fill" 
             style="width: ${data.risk_score}%; background: ${getColor(data.risk_score)}">
        </div>
      </div>
      
      <!-- Sinais Detectados -->
      <div class="signals-section">
        <h3>🚨 Sinais Detectados</h3>
        ${data.signals.map(signal => `
          <div class="signal-item ${signal.severity}">
            <div class="signal-icon">${getSignalIcon(signal.severity)}</div>
            <div class="signal-content">
              <strong>${signal.type}</strong>
              <p>${signal.description}</p>
            </div>
          </div>
        `).join('')}
      </div>
      
      <!-- Recomendação -->
      <div class="recommendation-box">
        <h3>💡 Recomendação</h3>
        <p>${data.recommendation}</p>
      </div>
      
      <!-- Perguntas Sugeridas -->
      ${data.suggested_questions?.length > 0 ? `
        <div class="questions-section">
          <h3>❓ Perguntas que Você Deve Fazer</h3>
          <ul>
            ${data.suggested_questions.map(q => `<li>${q}</li>`).join('')}
          </ul>
        </div>
      ` : ''}
    </div>
  `;
}

function getSignalIcon(severity) {
  const icons = {
    critical: '🔴',
    high: '🟠',
    medium: '🟡',
    low: '🟢'
  };
  return icons[severity] || '🔵';
}
```

---

## 3. 📄 OTIMIZAÇÃO DE CURRÍCULO

### 3.1 Upload e Otimização

```javascript
// No index.html
async function optimizeResume() {
  const fileInput = document.getElementById('resume-file');
  const jobDescription = document.getElementById('job-description').value;
  const token = localStorage.getItem('token');
  
  if (!fileInput.files[0]) {
    alert('Por favor, selecione um arquivo de currículo.');
    return;
  }
  
  if (!jobDescription.trim()) {
    alert('Por favor, cole a descrição da vaga.');
    return;
  }
  
  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  formData.append('job_description', jobDescription);
  formData.append('language', 'pt');
  
  try {
    showLoading(true, 'Otimizando seu currículo...');
    
    const response = await fetch('http://localhost:8000/api/resume/optimize', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });
    
    const data = await response.json();
    
    if (response.ok) {
      displayResumeResults(data);
    } else {
      alert('Erro: ' + data.detail);
    }
  } catch (error) {
    console.error('Erro na otimização:', error);
    alert('Erro ao otimizar currículo. Tente novamente.');
  } finally {
    showLoading(false);
  }
}
```

### 3.2 Exibir Resultados da Otimização

```javascript
// No index.html
function displayResumeResults(data) {
  const resultsDiv = document.getElementById('resume-results');
  
  resultsDiv.innerHTML = `
    <div class="resume-optimization-results">
      <!-- Score de Compatibilidade -->
      <div class="compatibility-header">
        <div class="compatibility-score">
          <div class="score-ring" style="--score: ${data.compatibility_score}">
            <svg viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="45" fill="none" stroke="#1e1e1e" stroke-width="8"/>
              <circle cx="50" cy="50" r="45" fill="none" stroke="#e8ff47" stroke-width="8"
                      stroke-dasharray="${data.compatibility_score * 2.83} 283"
                      transform="rotate(-90 50 50)"/>
            </svg>
            <div class="score-text">
              <span class="score-num">${data.compatibility_score}%</span>
              <span class="score-label">Match</span>
            </div>
          </div>
        </div>
        <div class="compatibility-info">
          <h3>Análise Completa</h3>
          <p>Seu currículo foi analisado e comparado com a vaga.</p>
        </div>
      </div>
      
      <!-- Grid de Análise -->
      <div class="analysis-grid">
        <!-- Pontos Fortes -->
        <div class="analysis-card strengths">
          <h4>✅ Pontos Fortes</h4>
          <ul>
            ${data.strengths.map(s => `<li>${s}</li>`).join('')}
          </ul>
        </div>
        
        <!-- Áreas de Melhoria -->
        <div class="analysis-card suggestions">
          <h4>💡 Sugestões de Melhoria</h4>
          <ul>
            ${data.suggestions.map(s => `<li>${s}</li>`).join('')}
          </ul>
        </div>
      </div>
      
      <!-- Palavras-chave -->
      <div class="keywords-analysis">
        <h4>🔑 Análise de Palavras-chave</h4>
        
        <div class="keywords-section">
          <div class="keyword-category">
            <span class="category-label">✓ Encontradas no seu currículo:</span>
            <div class="keyword-tags">
              ${data.matched_keywords.map(k => 
                `<span class="keyword-tag matched">${k}</span>`
              ).join('')}
            </div>
          </div>
          
          <div class="keyword-category">
            <span class="category-label">⚠️ Palavras importantes que estão faltando:</span>
            <div class="keyword-tags">
              ${data.missing_keywords.map(k => 
                `<span class="keyword-tag missing">${k}</span>`
              ).join('')}
            </div>
          </div>
        </div>
      </div>
      
      <!-- Seções Recomendadas -->
      ${data.recommended_sections?.length > 0 ? `
        <div class="recommended-sections">
          <h4>📋 Seções Recomendadas para Adicionar</h4>
          <ul>
            ${data.recommended_sections.map(s => `<li>${s}</li>`).join('')}
          </ul>
        </div>
      ` : ''}
      
      <!-- Download -->
      ${data.optimized_resume_url ? `
        <div class="download-section">
          <button class="btn-download-resume" onclick="downloadResume('${data.optimized_resume_url}')">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>
            </svg>
            Baixar Currículo Otimizado
          </button>
        </div>
      ` : ''}
    </div>
  `;
  
  // Scroll suave até os resultados
  resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

function downloadResume(url) {
  const link = document.createElement('a');
  link.href = url;
  link.download = 'curriculo_otimizado.pdf';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
```

---

## 4. 💳 PAGAMENTOS E UPGRADE

### 4.1 Iniciar Checkout do Stripe

```javascript
// No index.html
async function upgradeToPro() {
  const token = localStorage.getItem('token');
  
  if (!token) {
    alert('Por favor, faça login primeiro.');
    showLoginModal();
    return;
  }
  
  try {
    const response = await fetch('http://localhost:8000/api/billing/create-checkout-session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        plan: 'pro',
        success_url: window.location.origin + '/success?payment=success',
        cancel_url: window.location.origin + '/pricing?payment=cancelled'
      })
    });
    
    const data = await response.json();
    
    if (response.ok && data.checkout_url) {
      // Redirecionar para o Stripe Checkout
      window.location.href = data.checkout_url;
    } else {
      alert('Erro ao criar sessão de pagamento: ' + data.detail);
    }
  } catch (error) {
    console.error('Erro no checkout:', error);
    alert('Erro ao processar pagamento. Tente novamente.');
  }
}
```

### 4.2 Verificar Status da Assinatura

```javascript
// No index.html
async function checkSubscriptionStatus() {
  const token = localStorage.getItem('token');
  
  if (!token) return null;
  
  try {
    const response = await fetch('http://localhost:8000/api/billing/subscription-status', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    const data = await response.json();
    
    if (response.ok) {
      updateSubscriptionUI(data);
      return data;
    }
  } catch (error) {
    console.error('Erro ao verificar assinatura:', error);
  }
  
  return null;
}

function updateSubscriptionUI(subscription) {
  const planBadge = document.getElementById('plan-badge');
  
  if (subscription.active) {
    planBadge.innerHTML = `
      <span class="badge ${subscription.plan}">
        ${subscription.plan.toUpperCase()}
      </span>
      <span class="renewal-info">
        Renova em ${new Date(subscription.renewal_date).toLocaleDateString('pt-BR')}
      </span>
    `;
  } else {
    planBadge.innerHTML = `
      <span class="badge free">FREE</span>
      <button onclick="upgradeToPro()">Upgrade</button>
    `;
  }
}
```

### 4.3 Abrir Portal de Gerenciamento

```javascript
// No index.html
async function manageSubscription() {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch('http://localhost:8000/api/billing/customer-portal', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        return_url: window.location.href
      })
    });
    
    const data = await response.json();
    
    if (response.ok && data.portal_url) {
      window.location.href = data.portal_url;
    }
  } catch (error) {
    console.error('Erro ao abrir portal:', error);
    alert('Erro ao abrir portal de gerenciamento.');
  }
}
```

---

## 5. 🔧 FUNÇÕES AUXILIARES

### 5.1 Loading State

```javascript
// No index.html
function showLoading(show, message = 'Carregando...') {
  const overlay = document.getElementById('loading-overlay');
  const text = document.getElementById('loading-text');
  
  if (overlay) {
    overlay.style.display = show ? 'flex' : 'none';
  }
  
  if (text && message) {
    text.textContent = message;
  }
}

// HTML para o loading overlay
/*
<div id="loading-overlay" style="display: none;">
  <div class="spinner"></div>
  <p id="loading-text">Carregando...</p>
</div>
*/
```

### 5.2 Notificações Toast

```javascript
// No index.html
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  
  document.body.appendChild(toast);
  
  // Mostrar com animação
  setTimeout(() => toast.classList.add('show'), 10);
  
  // Remover após 3 segundos
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Uso:
// showToast('Análise concluída!', 'success');
// showToast('Erro ao processar', 'error');
// showToast('Atenção: limite atingido', 'warning');
```

### 5.3 Validação de Email

```javascript
// No index.html
function isValidEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function validateForm() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  
  if (!isValidEmail(email)) {
    showToast('Email inválido', 'error');
    return false;
  }
  
  if (password.length < 8) {
    showToast('Senha deve ter pelo menos 8 caracteres', 'error');
    return false;
  }
  
  return true;
}
```

---

## 6. 🎨 CSS ADICIONAL PARA OS EXEMPLOS

```css
/* Adicione ao index.html */

/* Score Circle Animation */
.score-circle {
  position: relative;
  width: 150px;
  height: 150px;
}

.score-circle svg {
  width: 100%;
  height: 100%;
}

.score-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.score-num {
  font-size: 2rem;
  font-weight: 800;
  display: block;
}

/* Keyword Tags */
.keyword-tag {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  margin: 0.3rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-family: var(--mono);
}

.keyword-tag.matched {
  background: rgba(52, 199, 89, 0.15);
  border: 1px solid rgba(52, 199, 89, 0.3);
  color: #34c759;
}

.keyword-tag.missing {
  background: rgba(255, 159, 10, 0.15);
  border: 1px solid rgba(255, 159, 10, 0.3);
  color: #ff9f0a;
}

/* Toast Notifications */
.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  padding: 1rem 1.5rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  font-family: var(--mono);
  font-size: 0.9rem;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.3s ease;
  z-index: 10000;
}

.toast.show {
  opacity: 1;
  transform: translateY(0);
}

.toast-success {
  border-left: 3px solid #34c759;
}

.toast-error {
  border-left: 3px solid #ff4747;
}

.toast-warning {
  border-left: 3px solid #ff9f0a;
}

/* Loading Overlay */
#loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  z-index: 9999;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

---

## 7. 📱 EXEMPLO COMPLETO DE PÁGINA

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TrustHire - Análise de Mensagens</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <!-- Header com Auth -->
  <header>
    <div class="container">
      <h1>TrustHire</h1>
      <div id="auth-section">
        <!-- Será preenchido dinamicamente -->
      </div>
    </div>
  </header>

  <!-- Seção de Análise -->
  <section class="analyzer">
    <div class="container">
      <h2>Analisar Mensagem</h2>
      <textarea id="message-input" 
                placeholder="Cole aqui a mensagem do recrutador..."></textarea>
      <button onclick="analyzeMessage()">Analisar</button>
      
      <div id="results"></div>
    </div>
  </section>

  <!-- Seção de Currículo (Premium) -->
  <section class="resume-optimizer premium-feature">
    <div class="container">
      <h2>Otimizar Currículo</h2>
      <input type="file" id="resume-file" accept=".pdf,.doc,.docx">
      <textarea id="job-description" 
                placeholder="Cole a descrição da vaga..."></textarea>
      <button onclick="optimizeResume()">Otimizar</button>
      
      <div id="resume-results"></div>
    </div>
  </section>

  <!-- Loading Overlay -->
  <div id="loading-overlay" style="display: none;">
    <div class="spinner"></div>
    <p id="loading-text">Carregando...</p>
  </div>

  <!-- Scripts -->
  <script src="api-integration.js"></script>
  <script>
    // Código específico da página aqui
  </script>
</body>
</html>
```

---

## 🎯 Checklist de Integração

- [ ] Backend rodando em `localhost:8000`
- [ ] Frontend rodando em `localhost:3000`
- [ ] `.env` configurado com API keys
- [ ] CORS habilitado no backend
- [ ] `api-integration.js` adicionado ao `index.html`
- [ ] Funções de autenticação funcionando
- [ ] Análise de mensagens funcionando
- [ ] Upload de currículo funcionando
- [ ] Stripe configurado (se usando pagamentos)

---

**Pronto!** Agora você tem todos os exemplos necessários para integrar completamente os 3 repositórios. 🚀
