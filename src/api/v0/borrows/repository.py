from typing import Sequence
from uuid import UUID
from datetime import datetime, timezone

from src.common.interfaces.repository import BaseRepository
from src.database.repositories.crud import CRUDRepository

from src.database.models.borrowedbook import BorrowedBook
from src.database.models.book import Book

from src.api.v0.borrows.schemas import BorrowingCreate

from src.database.utils.transactional import transactional


class BorrowsRepository(BaseRepository[BorrowedBook]):
    @property
    def crud(self) -> CRUDRepository[BorrowedBook]:
        return CRUDRepository(self.session, self.model)

    @property
    def model(self) -> type[BorrowedBook]:
        return BorrowedBook

    @transactional
    async def borrow(self, data: BorrowingCreate) -> BorrowedBook | None:
        return await self.crud.insert(**data.model_dump())

    @transactional
    async def receive(self, borrow_uuid: UUID) -> BorrowedBook | None:
        result = await self.crud.update(
            self.model.uuid == borrow_uuid,
            return_date=datetime.now(timezone.utc),
        )
        return result[0] if result else None

    async def reader_borrowed_list(
        self, reader_id: int
    ) -> Sequence[BorrowedBook]:
        return await self.crud.select_many(
            (self.model.reader_id == reader_id)
            & (self.model.return_date.is_(None))
        )

    async def all_active_borrowed(self) -> Sequence[BorrowedBook]:
        return await self.crud.select_many(self.model.return_date.is_(None))

    async def all_received(self) -> Sequence[BorrowedBook]:
        return await self.crud.select_many(self.model.return_date.is_not(None))


class BooksRepository(BaseRepository[Book]):
    @property
    def crud(self) -> CRUDRepository[Book]:
        return CRUDRepository(self.session, self.model)

    @property
    def model(self) -> type[Book]:
        return Book

    async def in_stock(self, uuid: UUID) -> int | None:
        book = await self.crud.select(self.model.uuid == uuid)
        if book:
            return book.count
        return None

    @transactional
    async def inc(self, uuid: UUID) -> bool:
        book = await self.crud.select(self.model.uuid == uuid)
        if not book:
            return False
        new_count = book.count + 1
        await self.crud.update(
            self.model.uuid == uuid,
            **{"count": new_count}
        )
        return True

    @transactional
    async def decr(self, uuid: UUID) -> bool:
        book = await self.crud.select(self.model.uuid == uuid)
        if not book or book.count <= 0:
            return False
        new_count = book.count - 1
        await self.crud.update(
            self.model.uuid == uuid,
            **{"count": new_count}
        )
        return True
