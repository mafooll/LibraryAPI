from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class ModelWithEmailMixin:
    email: Mapped[str] = mapped_column(
        String(128), nullable=False, index=True, unique=True
    )
