from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status, Response, Request

from src.core.settings import Settings
from src.security.jwt import TokenHelper
from src.security.hasher import PasswordHasher

from src.api.v0.auth.repository import TokenRepository
from src.api.v0.auth.repository import LibrarianRepository

from src.api.v0.auth.schemas import (
    LibrarianCreate,
    AuthUserResponse,
    LoginRequest,
    RegisterRequest,
)


class AuthService:
    def __init__(
        self,
        settings: Settings,
        token_helper: TokenHelper,
        hasher: PasswordHasher,
        token_repo: TokenRepository,
        librarian_repo: LibrarianRepository,
    ):
        self.settings = settings
        self.hasher = hasher
        self.token_helper = token_helper
        self.token_repo = token_repo
        self.librarian_repo = librarian_repo

    async def register(self, data: RegisterRequest) -> AuthUserResponse:
        existing = await self.librarian_repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )

        user = await self.librarian_repo.create(
            LibrarianCreate(
                username=data.username,
                email=data.email,
                password=self.hasher.hash(data.password),
            )
        )
        return AuthUserResponse(
            id=user.id, username=user.username, email=user.email
        )

    async def login(self, data: LoginRequest, response: Response) -> dict:
        user = await self.librarian_repo.get_by_email(data.email)
        if not user or not self.hasher.verify(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        access_token = self.token_helper.create_access({"sub": str(user.id)})
        refresh_token = self.token_helper.create_refresh({"sub": str(user.id)})

        refresh_exp = datetime.now(timezone.utc) + timedelta(
            seconds=self.settings.token.refresh_seconds
        )
        await self.token_repo.create(
            user_id=int(user.id),
            refresh_token=refresh_token,
            refresh_expires_at=refresh_exp,
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=self.settings.token.access_seconds,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=self.settings.token.refresh_seconds,
        )

        return {"message": "Logged in successfully"}

    async def refresh_tokens(
        self, request: Request, response: Response
    ) -> dict:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=401, detail="Missing refresh token"
            )

        payload = self.token_helper.verify(refresh_token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        token_entry = await self.token_repo.get_valid_by_token(refresh_token)
        if not token_entry:
            raise HTTPException(
                status_code=403, detail="Refresh token invalid"
            )

        new_access = self.token_helper.create_access({"sub": user_id})
        new_refresh = self.token_helper.create_refresh({"sub": user_id})

        await self.token_repo.invalidate(refresh_token)

        refresh_exp = datetime.now(timezone.utc) + timedelta(
            seconds=self.settings.token.refresh_seconds
        )
        await self.token_repo.create(
            user_id=int(user_id),
            refresh_token=new_refresh,
            refresh_expires_at=refresh_exp,
        )

        response.set_cookie(
            key="access_token",
            value=new_access,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=self.settings.token.access_seconds,
        )
        response.set_cookie(
            key="refresh_token",
            value=new_refresh,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=self.settings.token.refresh_seconds,
        )

        return {"message": "Tokens refreshed"}

    async def logout(self, request: Request, response: Response) -> None:
        refresh_token = request.cookies.get("refresh_token")
        if refresh_token:
            await self.token_repo.invalidate(refresh_token)

        response.delete_cookie(key="access_token", httponly=True, secure=True)
        response.delete_cookie(key="refresh_token", httponly=True, secure=True)
