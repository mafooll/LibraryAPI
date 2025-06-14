from typing import Any, Sequence

from sqlalchemy import insert, select, update, delete, ColumnExpressionArgument
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from src.database.models.base import BaseModel
from src.common.interfaces.crud import AbstractCRUDRepository


class CRUDRepository[ModelType: BaseModel](AbstractCRUDRepository[ModelType]):
    def __init__(
        self,
        session: async_scoped_session[AsyncSession],
        model: type[ModelType],
    ):
        super().__init__(model)
        self.session = session()

    async def insert(self, **values: Any) -> ModelType | None:
        stmt = insert(self.model).values(**values).returning(self.model)
        print(stmt)
        return (await self.session.execute(stmt)).scalars().first()

    async def select(
        self, *clauses: ColumnExpressionArgument[bool]
    ) -> ModelType | None:
        stmt = select(self.model).where(*clauses)
        return (await self.session.execute(stmt)).scalars().first()

    async def select_many(
        self, *clauses: ColumnExpressionArgument[bool]
    ) -> Sequence[ModelType]:
        stmt = select(self.model).where(*clauses)
        return (await self.session.execute(stmt)).scalars().all()

    async def update(
        self, *clauses: ColumnExpressionArgument[bool], **values: Any
    ) -> Sequence[ModelType]:
        stmt = (
            update(self.model)
            .where(*clauses)
            .values(**values)
            .returning(self.model)
        )
        return (await self.session.execute(stmt)).scalars().all()

    async def delete(
        self, *clauses: ColumnExpressionArgument[bool]
    ) -> Sequence[ModelType]:
        stmt = delete(self.model).where(*clauses).returning(self.model)
        return (await self.session.execute(stmt)).scalars().all()
