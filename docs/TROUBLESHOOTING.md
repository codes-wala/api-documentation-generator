# Troubleshooting

## Docker is unavailable

Start Docker Desktop or the Docker daemon, then rerun `./scripts/start.sh`.

## Port conflict

Change `WEB_PORT` or `API_PORT` in `.env`. If the public browser-facing API URL changes, update `NEXT_PUBLIC_API_BASE_URL` and rebuild the web image.

## API health check fails

Run:

```bash
docker compose --env-file .env logs --tail=150 db api
```

Look for database credentials, migration errors, or missing configuration.

## Gemini generation fails

- Missing key: configure `GEMINI_API_KEY` in `.env` and recreate the API container.
- 403: check key/project permissions and model availability.
- 429: check provider quota/rate limits and retry later.
- 503: the provider may be temporarily overloaded; wait and retry.

## Shared link is unavailable

The link may have been revoked or expired. Confirm `PUBLIC_APP_URL` matches the URL recipients use.

## Login/cookie issues

Use one hostname consistently. `localhost` and `127.0.0.1` are different cookie hosts. Check `CORS_ORIGINS` and the frontend API URL.
