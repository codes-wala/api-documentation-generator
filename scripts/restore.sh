#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if [[ $# -ne 1 || ! -f "$1" ]]; then echo "Usage: ./scripts/restore.sh backups/backup.sql.gz" >&2; exit 2; fi
[[ -f .env ]] || { echo "Missing .env." >&2; exit 1; }
echo "WARNING: this restore can overwrite existing database objects and data."
read -r -p "Type RESTORE to continue: " confirm
[[ "$confirm" == "RESTORE" ]] || { echo "Cancelled."; exit 1; }
set -a; source .env; set +a
docker compose --env-file .env exec -T db psql -v ON_ERROR_STOP=1 -U "${POSTGRES_USER:-app}" -d "${POSTGRES_DB:-api_docs}" -c 'DROP SCHEMA public CASCADE; CREATE SCHEMA public;'
gzip -dc "$1" | docker compose --env-file .env exec -T db psql -v ON_ERROR_STOP=1 -U "${POSTGRES_USER:-app}" -d "${POSTGRES_DB:-api_docs}"
echo "Restore command completed. Review application logs before using the data."
