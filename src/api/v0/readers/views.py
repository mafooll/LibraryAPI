from typing import Annotated  # , List

from fastapi import APIRouter, Depends, HTTPException

from dependency_injector.wiring import Provide, inject

from src.api.v0.readers.container import ReadersContainer
from src.api.v0.readers.schemas import ReaderCreate, ReaderUpdate, ReaderRead

from src.api.v0.auth import auth_required

readers_router = APIRouter(
    prefix="/readers", tags=["readers"], dependencies=[Depends(auth_required)]
)


@readers_router.post("/", response_model=ReaderRead)
@inject
async def create(
    data: ReaderCreate,
    repo: Annotated[
        ReadersContainer, Depends(Provide[ReadersContainer.readers_repo])
    ],
):
    reader = await repo.create(data)
    if not reader:
        raise HTTPException(status_code=400, detail="Could not create reader")
    return reader


@readers_router.get("/{reader_id}", response_model=ReaderRead)
@inject
async def get(
    reader_id: int,
    repo: Annotated[
        ReadersContainer, Depends(Provide[ReadersContainer.readers_repo])
    ],
):
    reader = await repo.get_by_id(reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader


@readers_router.get("/", response_model=list[ReaderRead])
@inject
async def get_all(
    repo: Annotated[
        ReadersContainer, Depends(Provide[ReadersContainer.readers_repo])
    ],
):
    return await repo.get_all()


@readers_router.put("/{reader_id}", response_model=ReaderRead)
@inject
async def update(
    reader_id: int,
    data: ReaderUpdate,
    repo: Annotated[
        ReadersContainer, Depends(Provide[ReadersContainer.readers_repo])
    ],
):
    updated_reader = await repo.update_by_id(reader_id, data)
    if not updated_reader:
        raise HTTPException(
            status_code=404, detail="Reader not found or no changes"
        )
    return updated_reader


@readers_router.delete("/{reader_id}", response_model=ReaderRead)
@inject
async def delete(
    reader_id: int,
    repo: Annotated[
        ReadersContainer, Depends(Provide[ReadersContainer.readers_repo])
    ],
):
    deleted_reader = await repo.delete_by_id(reader_id)
    if not deleted_reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return deleted_reader
