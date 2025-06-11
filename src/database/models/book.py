from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel
from src.database.models.mixins import (
    ModelWithTimeMixin,
    ModelWithUUIDMixin,
)


class Book(
    BaseModel,
    ModelWithTimeMixin,
    ModelWithUUIDMixin,
):
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    author: Mapped[str] = mapped_column(String(128), nullable=False)
    year: Mapped[int] = mapped_column(nullable=True)
    isbn: Mapped[str] = mapped_column(String(32), unique=True, nullable=True)
    count: Mapped[int] = mapped_column(default=1, nullable=False)
