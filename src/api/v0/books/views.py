from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from dependency_injector.wiring import Provide, inject

from src.api.v0.books.container import BooksContainer
from src.api.v0.books.schemas import BooksCreate, BooksUpdate, BooksRead

from src.api.v0.auth import auth_required

books_router = APIRouter(
    prefix="/books", tags=["books"], dependencies=[Depends(auth_required)]
)


@books_router.post("/", response_model=BooksRead)
@inject
async def create(
    data: BooksCreate,
    repo: Annotated[
        BooksContainer, Depends(Provide[BooksContainer.books_repo])
    ],
):
    book = await repo.create(data)
    if not book:
        raise HTTPException(status_code=400, detail="Could not create book")
    return book


@books_router.get("/{uuid}", response_model=BooksRead)
@inject
async def get_by_uuid(
    uuid: UUID,
    repo: Annotated[
        BooksContainer, Depends(Provide[BooksContainer.books_repo])
    ],
):
    book = await repo.get_by_uuid(uuid)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@books_router.put("/{uuid}", response_model=BooksRead)
@inject
async def update_by_uuid(
    uuid: UUID,
    data: BooksUpdate,
    repo: Annotated[
        BooksContainer, Depends(Provide[BooksContainer.books_repo])
    ],
):
    updated_book = await repo.update_by_uuid(uuid, data)
    if not updated_book:
        raise HTTPException(
            status_code=404, detail="Book not found or no changes"
        )
    return updated_book


@books_router.delete("/{uuid}", response_model=BooksRead)
@inject
async def delete_by_uuid(
    uuid: UUID,
    repo: Annotated[
        BooksContainer, Depends(Provide[BooksContainer.books_repo])
    ],
):
    deleted_book = await repo.delete_by_uuid(uuid)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book


@books_router.put("/isbn/{isbn}", response_model=BooksRead)
@inject
async def update_by_isbn(
    isbn: str,
    data: BooksUpdate,
    repo: Annotated[
        BooksContainer, Depends(Provide[BooksContainer.books_repo])
    ],
):
    updated_book = await repo.update_by_isbn(isbn, data)
    if not updated_book:
        raise HTTPException(
            status_code=404, detail="Book not found or no changes"
        )
    return updated_book


@books_router.delete("/isbn/{isbn}", response_model=BooksRead)
@inject
async def delete_by_isbn(
    isbn: str,
    repo: Annotated[
        BooksContainer, Depends(Provide[BooksContainer.books_repo])
    ],
):
    deleted_book = await repo.delete_by_isbn(isbn)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book


@books_router.get("/author/{author}", response_model=list[BooksRead])
@inject
async def get_by_author(
    author: str,
    repo: Annotated[
        BooksContainer, Depends(Provide[BooksContainer.books_repo])
    ],
):
    books = await repo.get_by_author(author)
    return books or []


@books_router.get("/title/{title}", response_model=list[BooksRead])
@inject
async def get_by_title(
    title: str,
    repo: Annotated[
        BooksContainer, Depends(Provide[BooksContainer.books_repo])
    ],
):
    books = await repo.get_by_title(title)
    return books or []


@books_router.get("/year/{year}", response_model=list[BooksRead])
@inject
async def get_by_year(
    year: int,
    repo: Annotated[
        BooksContainer, Depends(Provide[BooksContainer.books_repo])
    ],
):
    books = await repo.get_by_year(year)
    return books or []
