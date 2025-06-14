from typing import Annotated

from fastapi import Request

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from dependency_injector.wiring import Provide, inject

from src.api.v0.auth.container import AuthContainer
from src.security.jwt import TokenHelper


class AuthMiddleware(BaseHTTPMiddleware):
    @inject
    def __init__(
        self,
        app,
        token_helper: Annotated[
            TokenHelper, Provide[AuthContainer.token_helper]
        ],
    ):
        super().__init__(app)
        self.token_helper = token_helper

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        request.state.user = None

        access_token = request.cookies.get("access_token")
        if access_token:
            try:
                payload = self.token_helper.verify(access_token)
                user_id = payload.get("sub")
                if user_id:
                    request.state.user = type(
                        "User", (), {"id": user_id, "is_authenticated": True}
                    )()
            except Exception:
                pass

        response = await call_next(request)
        return response
