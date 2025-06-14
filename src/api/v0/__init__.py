from fastapi import APIRouter, FastAPI

from src.api.v0.auth.views import auth_router

router = APIRouter()
router.include_router(auth_router)


def setup_v0_routers(app: FastAPI) -> None:
    app.include_router(router, prefix="/api/v0", tags=["v0"])
