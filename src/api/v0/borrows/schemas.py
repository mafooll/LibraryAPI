from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)
