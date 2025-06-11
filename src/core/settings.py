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
            return [v.strip() for v in value.strip("[]").split(",") if v.strip()]
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
        return str(
            URL.create(
                drivername="postgresql+asyncpg",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
            )
        )


# class AlchemySettings(BaseSettings):
#     model_config = SettingsConfigDict(
#         env_file=env_path,
#         env_file_encoding="utf-8",
#         case_sensitive=False,
#         env_prefix="ALCHEMY_",
#         extra="ignore"
#     )


class Settings(BaseSettings):
    server: ServerSettings = ServerSettings()
    database: PostgresqlSettings = PostgresqlSettings()
