from typing import Annotated

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import Provide, inject

from src.api.v0.hello.hello_repo import HelloRepository
from src.api.v0.hello.container import HelloContainer


hello_router = APIRouter()


@hello_router.get("/hello")
async def hello():
    print("hello")
    return {"message": "Hello World"}


@hello_router.get("/book/{book_uuid}")
@inject
async def get_list(
    book_uuid: UUID,
    repo: Annotated[
        HelloRepository, Depends(Provide[HelloContainer.hello_repo])
    ],
):
    try:
        return await repo.get(book_uuid)
    except Exception:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
