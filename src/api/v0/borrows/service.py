from typing import Sequence

from fastapi import HTTPException

from src.api.v0.borrows.repository import BooksRepository
from src.api.v0.borrows.repository import BorrowsRepository

from src.database.models.borrowedbook import BorrowedBook

from src.api.v0.borrows.schemas import (
    BorrowingCreate,
    BorrowingReturn,
)


class BorrowsService:
    def __init__(
        self,
        borrows_repo: BorrowsRepository,
        books_repo: BooksRepository,
    ):
        self.borrows_repo = borrows_repo
        self.books_repo = books_repo

    async def borrow(self, data: BorrowingCreate) -> dict:
        book_count = await self.books_repo.in_stock(data.book_uuid)
        if book_count is None:
            raise HTTPException(status_code=404, detail="Book not found")

        if book_count <= 0:
            raise HTTPException(
                status_code=400, detail="No available copies of the book"
            )

        borrowed = await self.borrows_repo.reader_borrowed_list(data.reader_id)
        if len(borrowed) >= 3:
            raise HTTPException(
                status_code=400,
                detail="Reader cannot borrow more than 3 books",
            )

        await self.books_repo.decr(data.book_uuid)
        borrow_record = await self.borrows_repo.borrow(data)

        return {
            "message": "Book has been borrowed",
            "borrow_id": str(borrow_record.uuid),
        }

    async def receive(self, data: BorrowingReturn) -> dict:
        active_borrowings = await self.borrows_repo.reader_borrowed_list(
            data.reader_id
        )
        borrow = next(
            (b for b in active_borrowings if b.book_uuid == data.book_uuid),
            None,
        )

        if not borrow:
            raise HTTPException(
                status_code=400,
                detail="""
                    This book was not borrowed by this reader
                    or is already returned
                """,
            )

        await self.borrows_repo.receive(borrow.uuid)
        await self.books_repo.inc(data.book_uuid)

        return {"message": "Book successfully returned"}

    async def reader_borrowed_list(
        self, reader_id: int
    ) -> Sequence[BorrowedBook]:
        return await self.borrows_repo.reader_borrowed_list(
            reader_id=reader_id
        )

    async def all_active_borrowed(self) -> Sequence[BorrowedBook]:
        return await self.borrows_repo.all_active_borrowed()

    async def all_received(self) -> Sequence[BorrowedBook]:
        return await self.borrows_repo.all_received()
