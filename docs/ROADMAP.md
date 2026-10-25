# Implementation status and roadmap

## Included in this first implementation

- Registration, login, logout, session expiration, and password change.
- PostgreSQL models and initial Alembic migration.
- Project create/list/update/archive/restore/delete.
- Source upload and deletion with JSON/Python/partial JavaScript/TypeScript analysis.
- Gemini Markdown generation with provider error messages.
- Document create/edit/archive/restore/delete.
- Markdown editor and live preview.
- Version history and restoration.
- Read-only share links, expiration, revocation, and download permission.
- Markdown and sanitized HTML export.
- Project ZIP export.
- Docker Compose startup and database backup/restore scripts.
- Initial unit tests for analyzers and token/password helpers.

## Known limitations to address before public production use

- Add API-level and end-to-end tests for authentication, ownership isolation, share revocation, versions, exports, and migration flows.
- Add robust rate limiting for authentication, upload, share creation, and AI generation.
- Add password reset and email verification if account recovery is required.
- Add proper OpenAPI YAML parsing; YAML is currently accepted as text only.
- Replace JavaScript/TypeScript pattern analysis with AST-based parsing.
- Add request size limits and response-size controls at the reverse proxy as well as the application.
- Split the initial API route module into dedicated route and service modules.
- Add production-grade trusted-host/security-header configuration and deployment-specific monitoring.
- Add CI checks for frontend build, type checks, backend tests, migrations, and browser workflows.
- Add a proper project ZIP export policy for source files and sensitive data.
- Add automated conflict handling and richer editor collaboration later if required.

This roadmap is intentionally explicit: do not claim the items above are implemented until they are coded and verified.
