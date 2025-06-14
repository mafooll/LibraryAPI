from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, func, Integer, String

from src.database.models.base import BaseModel
from src.database.models.mixins import ModelWithUUIDMixin


class Token(BaseModel, ModelWithUUIDMixin):
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    refresh_token: Mapped[str] = mapped_column(
        String, nullable=False, index=True
    )
    refresh_expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    is_valid: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
