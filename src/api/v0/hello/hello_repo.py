from typing import Any

from uuid import UUID

from src.common.interfaces.repository import BaseRepository
from src.database.repositories.crud import CRUDRepository
from src.database.models.book import Book

from src.database.utils.transactional import transactional


class HelloRepository(BaseRepository[Book]):
    @property
    def crud(self) -> CRUDRepository[Book]:
        return CRUDRepository(self.session, self.model)

    @property
    def model(self) -> type[Book]:
        return Book

    @transactional
    async def create(self, data: Any) -> Book | None:
        return await self.crud.insert(**data.model_dump())

    async def get(self, uuid: UUID) -> Book | None:
        return await self.crud.select(self.model.id == uuid)
