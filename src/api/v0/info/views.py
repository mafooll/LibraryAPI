# src/api/v0/info/router.py
from typing import Annotated, List

from fastapi import APIRouter, Depends

from dependency_injector.wiring import Provide, inject

from src.api.v0.info.container import InfoContainer
from src.api.v0.info.schemas import BooksRead


info_router = APIRouter(prefix="/info", tags=["info"])


@info_router.post("/healthcheck", response_model=dict)
async def healthcheck():
    return {"message": "good"}


@info_router.get("/all_books", response_model=List[BooksRead])
@inject
async def all_books(
    repo: Annotated[InfoContainer, Depends(Provide[InfoContainer.info_repo])],
):
    books = await repo.get_all()
    return books
