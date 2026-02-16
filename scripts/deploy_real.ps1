param(
  [int]$HealthcheckTimeoutSeconds = 240,
  [int]$HealthcheckIntervalSeconds = 8,
  [string]$PublicApiUrl = ""
)

$ErrorActionPreference = 'Stop'

function Step($message) {
  Write-Host "`n==> $message"
}

function Fail($message) {
  Write-Host "`n❌ $message"
  exit 1
}

function Require-Cmd($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
    Fail "Comando obrigatório não encontrado: $name"
  }
}

Step "Validando pré-requisitos"
Require-Cmd python
Require-Cmd pip
Require-Cmd curl
Require-Cmd git
Require-Cmd railway

if (-not $env:RAILWAY_TOKEN) {
  Fail "Defina RAILWAY_TOKEN para deploy não-interativo."
}

& git diff --quiet
if ($LASTEXITCODE -ne 0) {
  Fail "Há alterações não commitadas. Faça commit antes do deploy."
}

& git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
  Fail "Há alterações em staging não commitadas. Faça commit antes do deploy."
}

Step "Instalando dependências de runtime/teste"
& pip install -r requirements.txt | Out-Null
if ($LASTEXITCODE -ne 0) { Fail "Falha ao instalar requirements.txt" }

& pip install pytest | Out-Null
if ($LASTEXITCODE -ne 0) { Fail "Falha ao instalar pytest" }

Step "Executando testes"
& pytest -q
if ($LASTEXITCODE -ne 0) { Fail "Testes falharam" }

Step "Publicando nova versão no Railway"
& railway up --ci
if ($LASTEXITCODE -ne 0) { Fail "Falha no railway up --ci" }

Step "Detectando URL pública"
if ([string]::IsNullOrWhiteSpace($PublicApiUrl)) {
  try {
    $domainOutput = & railway domain 2>$null
    if ($LASTEXITCODE -eq 0 -and $domainOutput) {
      foreach ($line in $domainOutput) {
        if ($line -match '(https?://[^\s]+|[\w.-]+\.(?:up\.railway\.app|railway\.app))') {
          $detected = $Matches[1]
          if ($detected -match '^https?://') {
            $PublicApiUrl = $detected
          } else {
            $PublicApiUrl = "https://$detected"
          }
          break
        }
      }
    }
  } catch {
    # fallback handled below
  }
}

if ([string]::IsNullOrWhiteSpace($PublicApiUrl)) {
  Fail "Não foi possível detectar domínio automaticamente. Informe -PublicApiUrl e rode novamente."
}

$healthUrl = "{0}/health" -f $PublicApiUrl.TrimEnd('/')
Step "Aguardando healthcheck em $healthUrl"

$start = Get-Date
while ($true) {
  try {
    $response = Invoke-WebRequest -Uri $healthUrl -Method GET -TimeoutSec 20
    if ($response.StatusCode -eq 200) {
      break
    }
  } catch {
    # retry
  }

  $elapsed = (Get-Date) - $start
  if ($elapsed.TotalSeconds -ge $HealthcheckTimeoutSeconds) {
    Fail "Timeout no healthcheck (${HealthcheckTimeoutSeconds}s). Verifique logs: railway logs"
  }

  Start-Sleep -Seconds $HealthcheckIntervalSeconds
}

Write-Host "`n✅ Deploy concluído com sucesso."
Write-Host "URL: $PublicApiUrl"
Write-Host "Health: $healthUrl`n"

try {
  $healthJson = Invoke-RestMethod -Uri $healthUrl -Method GET -TimeoutSec 20
  $healthJson | ConvertTo-Json -Depth 8
} catch {
  Write-Host "Não foi possível imprimir JSON do healthcheck, mas endpoint respondeu 200."
}
