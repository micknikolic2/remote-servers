from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict

class Settings(BaseSettings):
    """
    This class defines every setting our backend needs.
    Pydantic automatically loads them from the environment (such as Github secrets),
    .env files, or Docker env vars. This way, we avoid hard-coded secrets and keep configuration centralized.
    """
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )

    ENV: str = Field(default="local")

    # hardcode token and email for development and testing purposes (bypassing authorization)
    DEV_BEARER_TOKEN: str = "secret-dev-key"
    DEV_USER_EMAIL: str = "admin"

    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://postgres:Haldi2014!@127.0.0.1:5432/postgres"
    )
    TEST_DATABASE_URL: str | None = None

    SUPABASE_URL: str | None = None
    SUPABASE_ANON_KEY: str | None = None
    SUPABASE_JWT_SECRET: str | None = None

    POSTGRES_DB: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None


settings = Settings()