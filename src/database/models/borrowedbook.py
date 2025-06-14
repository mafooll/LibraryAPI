from datetime import datetime
from uuid import UUID
from sqlalchemy import func
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel
from src.database.models.book import Book
from src.database.models.reader import Reader
from src.database.models.librarian import Librarian
from src.database.models.mixins import (
    ModelWithUUIDMixin,
)


class BorrowedBook(
    BaseModel,
    ModelWithUUIDMixin,
):
    book_uuid: Mapped[UUID] = mapped_column(
        ForeignKey(Book.uuid, ondelete="CASCADE"), nullable=False
    )
    reader_id: Mapped[int] = mapped_column(
        ForeignKey(Reader.id, ondelete="CASCADE"), nullable=False
    )
    responsible_id: Mapped[int] = mapped_column(
        ForeignKey(Librarian.id, ondelete="CASCADE"), nullable=False
    )

    borrow_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    return_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
