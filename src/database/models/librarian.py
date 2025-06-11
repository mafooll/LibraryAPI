from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel
from src.database.models.mixins import (
    ModelWithIDMixin,
    ModelWithEmailMixin,
    ModelWithTimeMixin,
)


class Librarian(
    BaseModel, ModelWithIDMixin,
    ModelWithEmailMixin, ModelWithTimeMixin
):
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    hashed_pass: Mapped[str] = mapped_column()
