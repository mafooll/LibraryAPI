from typing import Sequence
from uuid import UUID

from src.common.interfaces.repository import BaseRepository
from src.database.repositories.crud import CRUDRepository
from src.database.models.book import Book
from src.database.utils.transactional import transactional
from src.api.v0.books.schemas import BooksCreate, BooksUpdate


class BooksRepository(BaseRepository[Book]):
    @property
    def crud(self) -> CRUDRepository[Book]:
        return CRUDRepository(self.session, self.model)

    @property
    def model(self) -> type[Book]:
        return Book

    @transactional
    async def create(self, data: BooksCreate) -> Book | None:
        existing = await self.get_by_isbn(data.isbn)
        if existing:
            raise ValueError(f"Book with ISBN {data.isbn} already exists.")
        return await self.crud.insert(**data.model_dump())

    async def get_by_uuid(self, uuid: UUID) -> Book | None:
        return await self.crud.select(self.model.uuid == uuid)

    async def get_by_isbn(self, isbn: str) -> Book | None:
        return await self.crud.select(self.model.isbn == isbn)

    async def get_by_title(self, title: str) -> Sequence[Book] | None:
        return await self.crud.select_many(self.model.title == title)

    async def get_by_author(self, author: str) -> Sequence[Book] | None:
        return await self.crud.select_many(self.model.author == author)

    async def get_by_year(self, year: int) -> Sequence[Book] | None:
        return await self.crud.select_many(self.model.year == year)

    @transactional
    async def update_by_isbn(
        self, isbn: str, data: BooksUpdate
    ) -> Book | None:
        new_isbn = data.isbn
        book = await self.get_by_isbn(isbn)
        if book:
            if new_isbn and new_isbn != book.isbn:
                existing = await self.get_by_isbn(new_isbn)
                if existing:
                    raise ValueError(f"ISBN {new_isbn} is already in use")
        result = await self.crud.update(
            self.model.isbn == isbn, **data.model_dump(exclude_unset=True)
        )
        return result[0] if result else None

    @transactional
    async def update_by_uuid(
        self, uuid: UUID, data: BooksUpdate
    ) -> Book | None:
        new_isbn = data.isbn
        book = await self.get_by_uuid(uuid)
        if book:
            if new_isbn and new_isbn != book.isbn:
                existing = await self.get_by_isbn(new_isbn)
                if existing:
                    raise ValueError(f"ISBN {new_isbn} is already in use")
        result = await self.crud.update(
            self.model.uuid == uuid, **data.model_dump(exclude_unset=True)
        )
        return result[0] if result else None

    @transactional
    async def delete_by_uuid(self, uuid: UUID) -> Book | None:
        result = await self.crud.delete(self.model.uuid == uuid)
        return result[0] if result else None

    @transactional
    async def delete_by_isbn(self, isbn: str) -> Book | None:
        result = await self.crud.delete(self.model.isbn == isbn)
        return result[0] if result else None
