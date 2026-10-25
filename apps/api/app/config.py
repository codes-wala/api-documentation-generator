from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "API Documentation Generator"
    app_env: str = "development"
    app_secret_key: str = ""
    database_url: str = "postgresql+psycopg://app:app@db:5432/api_docs"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.5-flash-lite"
    frontend_url: str = "http://localhost:3000"
    cors_origins: str = "http://localhost:3000"
    public_app_url: str = "http://localhost:3000"
    session_cookie_name: str = "api_docs_session"
    session_cookie_secure: bool = False
    session_max_age: int = 60 * 60 * 24 * 7
    max_upload_size_mb: int = 5
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
