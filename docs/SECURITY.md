# Security notes

## Implemented in the initial release

- Passwords are hashed using Argon2id.
- Browser sessions use random opaque tokens; only SHA-256 token hashes are stored in PostgreSQL.
- Session records have expiration and revocation fields.
- Session cookies are HttpOnly and SameSite=Lax; Secure is configurable for HTTPS deployment.
- Mutating cookie-authenticated requests require a CSRF token header matching the CSRF cookie.
- Private project, source, document, version, export, generation, and share-management routes check ownership.
- Share links use high-entropy random tokens; the database stores a hash of each token.
- Uploaded source files are treated as text and are not executed.
- Markdown rendering does not enable raw HTML in the React viewer. HTML export is sanitized.
- Gemini credentials are backend-only.

## Required before public production use

- Deploy behind HTTPS and set `SESSION_COOKIE_SECURE=true`.
- Use a production secrets manager or carefully protected secret file.
- Configure the exact trusted browser origins and public URL.
- Add a production reverse proxy with appropriate security headers and trusted-host policy.
- Add robust rate limiting for registration, login, sharing, upload, and generation endpoints at the application or ingress layer.
- Add email verification/password-reset flow before relying on account recovery.
- Review session revocation, account deletion, and retention policies.
- Add dependency scanning, image scanning, and regular security testing.
- Add explicit operational monitoring and tested backup restoration.
- Review the API against the deployment's threat model before exposing it to the public internet.

This document describes implemented safeguards and remaining work; it is not a security certification.
