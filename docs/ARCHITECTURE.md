# Architecture

The first release is a modular monolith deployed as three Docker Compose services: Next.js, FastAPI, and PostgreSQL. The browser talks to FastAPI over HTTP with an HttpOnly session cookie. Mutating requests include a CSRF token. The API validates ownership on private resources before reading or changing them.

## Request flow

1. The browser loads a workspace page.
2. The web app calls `/api/v1/auth/me` to validate the session.
3. FastAPI hashes the opaque cookie token and looks up its server-side session record.
4. Private routes verify the owner relationship through the database.
5. Source analysis is performed locally by a parser service; uploaded code is never executed.
6. Generation calls Gemini only after configuration is checked, and successful content is persisted as a document and initial version.
7. Export and share routes use the saved database content. Public sharing resolves only a matching active, unexpired token hash.

## Main modules

- `app/main.py`: HTTP routes and API orchestration for this first implementation.
- `app/models.py`: SQLAlchemy models.
- `app/security.py`: password hashing, session token generation, token hashing.
- `app/analyzers.py`: deterministic source analysis.
- `migrations/`: Alembic schema migration history.
- `apps/web/app`: Next.js route pages.
- `apps/web/lib/api.ts`: API client with cookie credentials and CSRF header handling.

## Architectural follow-ups

As the feature set grows, split route orchestration from `main.py` into endpoint modules and move business logic into services/repositories. Add a reverse proxy and deployment-specific secret management for public production hosting.
