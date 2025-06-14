from typing import Any, Sequence, Mapping
from abc import ABC, abstractmethod


class AbstractCRUDRepository[EntryType](ABC):
    def __init__(self, model: type[EntryType]):
        self.model = model

    @abstractmethod
    async def insert(self, **values: Any) -> EntryType | None:
        raise NotImplementedError

    @abstractmethod
    async def select(self, *clauses: Any) -> EntryType | None:
        raise NotImplementedError

    @abstractmethod
    async def select_many(self, *clauses: Any) -> Sequence[EntryType]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, *clauses: Any, **values: Mapping[str, Any]
    ) -> Sequence[EntryType]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *clauses: Any) -> Sequence[EntryType]:
        raise NotImplementedError
