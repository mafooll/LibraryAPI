from typing import Sequence

from src.common.interfaces.repository import BaseRepository
from src.database.repositories.crud import CRUDRepository
from src.database.models.book import Book


class InfoRepository(BaseRepository[Book]):
    @property
    def crud(self) -> CRUDRepository[Book]:
        return CRUDRepository(self.session, self.model)

    @property
    def model(self) -> type[Book]:
        return Book

    async def get_all(self) -> Sequence[Book] | None:
        return await self.crud.select_all()
