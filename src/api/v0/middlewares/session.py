from typing import Callable, Annotated

from fastapi import Request, Response

from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    AsyncSession,
)

from dependency_injector.wiring import Provide, inject

from src.api.v0.container import V0Container
from src.database.utils.scoped import set_context, reset_context


class ScopedSessionMiddleware(BaseHTTPMiddleware):
    @inject
    def __init__(
        self,
        app,
        scoped_session: Annotated[
            async_scoped_session[AsyncSession],
            Provide[V0Container.scoped_session],
        ],
    ):
        super().__init__(app)
        self.scoped_session = scoped_session

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        request_id = str(id(request))
        try:
            set_context(request_id)
            response = await call_next(request)
        finally:
            await self.scoped_session.remove()
            reset_context()
        return response
