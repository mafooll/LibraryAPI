from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BooksCreate(BaseModel):
    title: str
    author: str
    year: int
    isbn: str
    count: int = 1


class BooksUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None
    isbn: str | None = None
    count: int | None = None


class BooksRead(BaseModel):
    uuid: UUID
    title: str
    author: str
    year: int
    isbn: str
    count: int

    model_config = ConfigDict(from_attributes=True)
