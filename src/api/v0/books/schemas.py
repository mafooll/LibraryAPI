from uuid import UUID

from pydantic import BaseModel


class BooksCreate(BaseModel):
    title: str
    author: str
    year: int
    isbn: str
    count: int


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

    class Config:
        from_attributes = True
