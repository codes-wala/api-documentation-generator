import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from app.config import settings

_hasher = PasswordHasher()
def hash_password(password: str) -> str:
    return _hasher.hash(password)
def verify_password(password: str, password_hash: str) -> bool:
    try: return _hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError): return False
def new_session_token() -> str:
    return secrets.token_urlsafe(32)
def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
def session_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(seconds=settings.session_max_age)
def new_csrf_token() -> str:
    return secrets.token_urlsafe(32)
