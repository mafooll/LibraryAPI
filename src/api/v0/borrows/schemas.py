from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class BorrowingCreate(BaseModel):
    book_uuid: UUID
    reader_id: int
    responsible_id: int


class BorrowingReturn(BaseModel):
    book_uuid: UUID
    reader_id: int


class BorrowingRead(BaseModel):
    uuid: UUID
    book_uuid: UUID
    reader_id: int
    responsible_id: int
    borrow_date: datetime
    return_date: datetime | None

    class Config:
        from_attributes = True
