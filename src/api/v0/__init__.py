from fastapi import APIRouter, FastAPI

from src.api.v0.auth.views import auth_router
from src.api.v0.readers.views import readers_router
from src.api.v0.books.views import books_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(readers_router)
router.include_router(books_router)


def setup_v0_routers(app: FastAPI) -> None:
    app.include_router(router, prefix="/api/v0", tags=["v0"])
