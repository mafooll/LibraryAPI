from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from src.api.v0 import setup_v0_routers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield


def init_app() -> FastAPI:
    app = FastAPI(title="LibAPI", lifespan=lifespan)
    setup_v0_routers(app)

    return app
