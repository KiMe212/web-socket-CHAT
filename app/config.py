from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow", env_prefix="DB_")

    host: str = "db"
    port: int = 5432
    user: str = "mike"
    password: str = "sob"
    name: str = "chat"

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{quote_plus(self.password)}@{self.host}:{self.port}/{self.name}"

    """Add ASyncpg and fix it in database"""


class UvicornSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="UVICORN_",
        env_file=".env",
        extra="ignore",
    )

    log_level: str = "info"
    reload: bool = True
    limit_max_requests: int | None = None


class TokenSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    secret_key: str = "8334587dec44166195761c7a06ac1c0a5237269de32b5f4ad94db17e0cb43862"
    algorithim: str = "HS256"

    access_token_expire_time: int = 1
    refresh_token_expire_minutes: int = 50
    refresh_token_secret_key: str = (
        "4f5e0a05a030253b1e9824c5463919ffd086656611dee061a6516038341bcaf2"
    )


class Settings(BaseSettings, case_sensitive=False):
    model_config = SettingsConfigDict(extra="allow")
    tokens: TokenSettings = TokenSettings()

    uvicorn: UvicornSettings = UvicornSettings()
    db: DBSettings = DBSettings()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


config: Settings = get_settings()
