# Deployment guide

## Local Compose

Run `./scripts/start.sh`. It creates `.env` when absent, fills blank application/database secrets, builds the containers, starts PostgreSQL, applies migrations, and waits for the API and frontend health checks.

## Public deployment checklist

1. Use a managed PostgreSQL service or a hardened private PostgreSQL deployment.
2. Configure a domain and terminate TLS at a trusted reverse proxy or platform ingress.
3. Set `APP_ENV=production`, `SESSION_COOKIE_SECURE=true`, and strong unique secrets.
4. Configure `FRONTEND_URL`, `CORS_ORIGINS`, `PUBLIC_APP_URL`, and `NEXT_PUBLIC_API_BASE_URL` for the actual deployment. Rebuild the web image when the `NEXT_PUBLIC_*` value changes.
5. Do not expose PostgreSQL to the public internet.
6. Configure backups, restoration drills, monitoring, rate limits, and a secret rotation process.
7. Run migrations once during the release process and verify readiness before directing traffic.
8. Review proxy headers, allowed hosts, security headers, logging, and upload limits.
9. Keep secrets out of images, source control, logs, and browser bundles.

The provided Compose file binds web and API ports to loopback by default. This is a safe local default, not a complete internet-facing deployment topology.
