from fastapi import APIRouter, FastAPI

from src.api.v0.hello_world.views import hello_router

router = APIRouter()
router.include_router(hello_router)


def setup_v0_routers(app: FastAPI) -> None:
    app.include_router(router, prefix="/api/v0", tags=["v0"])
