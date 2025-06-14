from typing import Annotated

from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from src.api.v0.borrows.container import BorrowsContainer
from src.api.v0.borrows.service import BorrowsService
from src.api.v0.auth import auth_required

from src.api.v0.borrows.schemas import (
    BorrowingCreate,
    BorrowingReturn,
    BorrowingRead,
)

borrows_router = APIRouter(
    prefix="/borrows",
    tags=["borrows"],
    dependencies=[Depends(auth_required)],
)


@borrows_router.post("/", response_model=dict)
@inject
async def borrow_book(
    data: BorrowingCreate,
    service: Annotated[
        BorrowsService, Depends(Provide[BorrowsContainer.service])
    ],
):
    return await service.borrow(data)


@borrows_router.post("/return", response_model=dict)
@inject
async def return_book(
    data: BorrowingReturn,
    service: Annotated[
        BorrowsService, Depends(Provide[BorrowsContainer.service])
    ],
):
    return await service.receive(data)


@borrows_router.get("/reader/{reader_id}", response_model=list[BorrowingRead])
@inject
async def reader_borrowed_books(
    reader_id: int,
    service: Annotated[
        BorrowsService, Depends(Provide[BorrowsContainer.service])
    ],
):
    return await service.reader_borrowed_list(reader_id)


@borrows_router.get("/active", response_model=list[BorrowingRead])
@inject
async def all_active_borrows(
    service: Annotated[
        BorrowsService, Depends(Provide[BorrowsContainer.service])
    ],
):
    return await service.all_active_borrowed()


@borrows_router.get("/returned", response_model=list[BorrowingRead])
@inject
async def all_returned_borrows(
    service: Annotated[
        BorrowsService, Depends(Provide[BorrowsContainer.service])
    ],
):
    return await service.all_received()
