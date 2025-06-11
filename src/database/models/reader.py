from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel
from src.database.models.mixins import (
    ModelWithIDMixin,
    ModelWithEmailMixin,
    ModelWithTimeMixin,
)


class Reader(
    BaseModel,
    ModelWithIDMixin,
    ModelWithEmailMixin,
    ModelWithTimeMixin,
):
    username: Mapped[str] = mapped_column(String(32), nullable=True)
