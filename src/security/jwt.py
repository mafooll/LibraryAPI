from typing import Any
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from jose import jwt, JWTError, ExpiredSignatureError  # type: ignore

from src.core.settings import Settings


class TokenHelper:
    def __init__(self, settings: Settings):
        self.settings = settings

    def _create_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            self.settings.token.secret_key,
            self.settings.token.algorithm,
        )

    def create_access(self, data: dict) -> str:
        return self._create_token(
            data, timedelta(seconds=self.settings.token.access_seconds)
        )

    def create_refresh(self, data: dict) -> str:
        return self._create_token(
            data, timedelta(seconds=self.settings.token.refresh_seconds)
        )

    def verify(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                self.settings.token.secret_key,
                algorithms=[self.settings.token.algorithm],
            )
            return payload
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
