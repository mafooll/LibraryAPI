from jose import jwt  # type: ignore
from datetime import datetime, timedelta, timezone

from src.core.settings import Settings


class Token:
    def __init__(self, settings: Settings):
        self.settings = settings

    def create_access(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            seconds=self.settings.token.access_seconds
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            self.settings.token.secret_key,
            self.settings.token.algorithm,
        )

    def create_refresh(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            seconds=self.settings.token.refresh_seconds
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            self.settings.token.secret_key,
            self.settings.token.algorithm,
        )

    def verify(self): ...
