from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BooksRead(BaseModel):
    uuid: UUID
    title: str
    author: str
    year: int
    isbn: str
    count: int

    model_config = ConfigDict(from_attributes=True)
