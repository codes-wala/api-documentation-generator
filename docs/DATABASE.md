# Database

PostgreSQL stores accounts, server-side sessions, projects, source text and analysis metadata, documents, immutable document versions, share-link metadata, and generation history.

## Migrations

Alembic is configured under `apps/api/migrations`. The initial migration establishes the SQLAlchemy metadata schema. Apply migrations from the API directory with:

```bash
alembic upgrade head
```

The API container runs migrations before starting Uvicorn. Production deployments with multiple API replicas should run migrations once as a controlled deployment step rather than letting every replica race.

## Persistence

Docker Compose stores database files in the named `postgres_data` volume. Rebuilding the web or API container does not remove this volume. Avoid `docker compose down -v` unless you intentionally want to delete local database data.

## Backup

Run `./scripts/backup.sh` to create a compressed SQL dump in `backups/`. Run `./scripts/restore.sh <backup-file>` to restore after confirming the destructive operation. Backups should be copied to protected off-host storage for production. The current implementation stores source text in PostgreSQL, so a PostgreSQL dump includes it.
