$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Root

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw "Docker is not installed. Install Docker Desktop first." }
docker info *> $null
if ($LASTEXITCODE -ne 0) { throw "Docker Desktop is not running. Start it and retry." }
docker compose version *> $null
if ($LASTEXITCODE -ne 0) { throw "Docker Compose v2 is required." }
if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env"; Write-Host "Created .env from .env.example." }

function New-Secret {
  $bytes = New-Object byte[] 32
  $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
  $rng.GetBytes($bytes); $rng.Dispose()
  return (([BitConverter]::ToString($bytes) -replace "-", "")).ToLowerInvariant()
}
function Set-EnvIfBlank([string]$Key, [string]$Value) {
  $lines = @(Get-Content ".env")
  $found = $false
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "^$([regex]::Escape($Key))=") {
      $found = $true
      if ($lines[$i] -eq "$Key=") { $lines[$i] = "$Key=$Value" }
    }
  }
  if (-not $found) { $lines += "$Key=$Value" }
  Set-Content -Path ".env" -Value $lines -Encoding utf8
}
Set-EnvIfBlank "APP_SECRET_KEY" (New-Secret)
Set-EnvIfBlank "DB_PASSWORD" (New-Secret)

$envText = Get-Content ".env" -Raw
if ($envText -match '(?m)^GEMINI_API_KEY=\s*$') { Write-Host "Gemini is not configured; the application will start, but AI generation will be disabled." }
Write-Host "Building and starting the application. The first run can take several minutes."
docker compose --env-file .env up --build -d
if ($LASTEXITCODE -ne 0) { throw "Docker Compose failed. Run: docker compose --env-file .env logs --tail=100" }

function Wait-ForUrl([string]$Url, [string]$Label) {
  for ($i = 0; $i -lt 60; $i++) {
    try { $null = Invoke-WebRequest -Uri $Url -TimeoutSec 3; Write-Host "$Label is ready."; return }
    catch { Start-Sleep -Seconds 2 }
  }
  docker compose --env-file .env logs --tail=80
  throw "Timed out waiting for $Label. Review the logs above."
}
$apiPort = 8000; $webPort = 3000
if ($envText -match '(?m)^API_PORT=(\d+)') { $apiPort = [int]$Matches[1] }
if ($envText -match '(?m)^WEB_PORT=(\d+)') { $webPort = [int]$Matches[1] }
Wait-ForUrl "http://localhost:$apiPort/health/ready" "Backend API"
Wait-ForUrl "http://localhost:$webPort" "Frontend"
Write-Host ""
Write-Host "API Documentation Generator is running."
Write-Host "Web app:       http://localhost:$webPort"
Write-Host "Backend API:   http://localhost:$apiPort"
Write-Host "API reference: http://localhost:$apiPort/docs"
Write-Host "Logs:          docker compose --env-file .env logs -f"
Write-Host "Stop:          docker compose --env-file .env down"
