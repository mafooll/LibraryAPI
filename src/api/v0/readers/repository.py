from typing import Sequence

from src.common.interfaces.repository import BaseRepository
from src.database.repositories.crud import CRUDRepository
from src.database.models.reader import Reader

from src.database.utils.transactional import transactional

from src.api.v0.readers.schemas import (
    ReaderCreate,
    ReaderUpdate,
)


class ReadersRepository(BaseRepository[Reader]):
    @property
    def crud(self) -> CRUDRepository[Reader]:
        return CRUDRepository(self.session, self.model)

    @property
    def model(self) -> type[Reader]:
        return Reader

    @transactional
    async def create(self, data: ReaderCreate) -> Reader | None:
        existing = await self.get_by_email(data.email)
        if existing:
            raise ValueError(f"email {data.email} is already in use")
        return await self.crud.insert(**data.model_dump())

    async def get_by_id(self, reader_id: int) -> Reader | None:
        return await self.crud.select(self.model.id == reader_id)

    async def get_by_email(self, reader_email: str) -> Reader | None:
        return await self.crud.select(self.model.email == reader_email)

    async def get_all(self) -> Sequence[Reader] | None:
        return await self.crud.select_all()

    @transactional
    async def update_by_id(self, id: int, data: ReaderUpdate) -> Reader | None:
        new_email = data.email
        user = await self.get_by_id(id)
        if user:
            if new_email and new_email != user.email:
                existing = await self.get_by_email(new_email)
                if existing:
                    raise ValueError(f"email {new_email} is already in use")
        result = await self.crud.update(
            self.model.id == id, **data.model_dump(exclude_unset=True)
        )
        return result[0] if result else None

    @transactional
    async def update_by_email(
        self, email: str, data: ReaderUpdate
    ) -> Reader | None:
        new_email = data.email
        if new_email and new_email != email:
            existing = await self.get_by_email(new_email)
            if existing:
                raise ValueError(f"email {new_email} is already in use")
        result = await self.crud.update(
            self.model.email == email, **data.model_dump(exclude_unset=True)
        )
        return result[0] if result else None

    @transactional
    async def delete_by_id(self, id: int) -> Reader | None:
        result = await self.crud.delete(self.model.id == id)
        return result[0] if result else None

    @transactional
    async def delete_by_email(self, email: str) -> Reader | None:
        result = await self.crud.delete(self.model.email == email)
        return result[0] if result else None
