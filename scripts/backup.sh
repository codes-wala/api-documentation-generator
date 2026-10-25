#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ -f .env ]] || { echo "Missing .env. Run ./scripts/start.sh first." >&2; exit 1; }
set -a; source .env; set +a
mkdir -p backups
file="backups/api_docs_$(date -u +%Y%m%dT%H%M%SZ).sql.gz"
docker compose --env-file .env exec -T db pg_dump -U "${POSTGRES_USER:-app}" -d "${POSTGRES_DB:-api_docs}" | gzip > "$file"
echo "Backup written to $file"
