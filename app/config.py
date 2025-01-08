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
        return f"postgresql+asyncpg://{self.user}:{quote_plus(self.password)}@{self.host}:{self.port}/{self.name}"


class UvicornSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="UVICORN_",
        env_file=".env",
        extra="ignore",
    )

    log_level: str = "info"
    reload: bool = True
    limit_max_requests: int | None = None

class Settings(BaseSettings, case_sensitive=False):
    model_config = SettingsConfigDict(extra="allow")

    uvicorn: UvicornSettings = UvicornSettings()
    db: DBSettings = DBSettings()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


config: Settings = get_settings()