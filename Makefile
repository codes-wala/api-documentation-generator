.PHONY: up down logs test-api
up:
	./scripts/start.sh
down:
	./scripts/stop.sh
logs:
	docker compose --env-file .env logs -f
test-api:
	cd apps/api && pytest
