#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
fail(){ echo "ERROR: $*" >&2; exit 1; }
command -v docker >/dev/null 2>&1 || fail "Docker is not installed. Install Docker Engine/Desktop first: https://docs.docker.com/get-docker/"
docker info >/dev/null 2>&1 || fail "Docker is installed but the Docker daemon is not running. Start Docker and run this script again."
docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is required (docker compose)."
if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example."
fi
# Fill only blank values. Never overwrite an existing secret or user configuration.
set_env_if_blank(){ local key="$1" value="$2"; if grep -qE "^${key}=$" .env; then sed -i "s|^${key}=$|${key}=${value}|" .env; elif ! grep -qE "^${key}=" .env; then printf '%s=%s\n' "$key" "$value" >> .env; fi; }
random_secret(){ openssl rand -hex 32 2>/dev/null || od -An -N32 -tx1 /dev/urandom | tr -d ' \n'; }
set_env_if_blank APP_SECRET_KEY "$(random_secret)"
set_env_if_blank DB_PASSWORD "$(random_secret)"
# Validate the required secret fields without printing their values.
for key in APP_SECRET_KEY DB_PASSWORD; do
  value="$(grep -m1 "^${key}=" .env | cut -d= -f2-)"
  [[ -n "$value" ]] || fail "$key is empty in .env. Set it and retry."
done
if ! grep -q '^GEMINI_API_KEY=' .env || [[ -z "$(grep -m1 '^GEMINI_API_KEY=' .env | cut -d= -f2-)" ]]; then
  echo "Gemini key not configured. The app will start, but AI generation remains disabled until GEMINI_API_KEY is added to .env."
fi
echo "Building and starting the application. The first run may take several minutes..."
docker compose --env-file .env up --build -d
wait_for(){ local url="$1" label="$2" attempts="${3:-60}"; for ((i=1;i<=attempts;i++)); do if curl -fsS "$url" >/dev/null 2>&1; then echo "$label is ready."; return 0; fi; sleep 2; done; echo "Timed out waiting for $label. Recent logs:" >&2; docker compose logs --tail=80 >&2; return 1; }
wait_for "http://localhost:${API_PORT:-8000}/health/ready" "Backend API" 60 || fail "Backend did not become ready. See logs above."
wait_for "http://localhost:${WEB_PORT:-3000}" "Frontend" 60 || fail "Frontend did not become ready. See logs above."
echo
echo "API Documentation Generator is running."
echo "  Web app:       http://localhost:${WEB_PORT:-3000}"
echo "  Backend API:   http://localhost:${API_PORT:-8000}"
echo "  API reference: http://localhost:${API_PORT:-8000}/docs"
echo "  Health:        http://localhost:${API_PORT:-8000}/health/ready"
echo
echo "Useful commands:"
echo "  docker compose logs -f"
echo "  docker compose down"
echo "  ./scripts/backup.sh"
