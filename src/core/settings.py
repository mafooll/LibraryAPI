from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from sqlalchemy.engine import URL

from src.core.const import env_path


class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="SERVER_",
        extra="ignore",
    )
    host: str = "0.0.0.0"
    port: int = 8000
    origins: list[str] | None = None
    methods: list[str] | None = None
    headers: list[str] | None = None

    @field_validator("origins", "methods", "headers", mode="before")
    @classmethod
    def parse_list(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [
                v.strip() for v in value.strip("[]").split(",") if v.strip()
            ]
        return value


class PostgresqlSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="POSTGRES_",
        extra="ignore",
    )
    user: str = "postgres"
    password: str = "postgres"
    database: str = "postgres"
    host: str = "postgresql_container"
    port: int = 5432

    @property
    def url(self) -> str:
        return URL.create(
                drivername="postgresql+asyncpg",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
            ).render_as_string(hide_password=False)


class AlchemySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="ALCHEMY_",
        extra="ignore",
    )
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 25
    pool_recycle: int = 3600
    pool_timeout: int = 10
    max_overflow: int = 50
    autoflush: bool = False
    expire_on_commit: bool = False


class Settings(BaseSettings):
    server: ServerSettings = ServerSettings()
    database: PostgresqlSettings = PostgresqlSettings()
    alchemy: AlchemySettings = AlchemySettings()


def get_settings() -> Settings:
    return Settings()
