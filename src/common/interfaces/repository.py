from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from src.database.models.base import BaseModel
from src.common.interfaces.crud import AbstractCRUDRepository


class BaseRepository[ModelType: BaseModel]:
    def __init__(self, session: async_scoped_session[AsyncSession]):
        self.session = session

    @property
    @abstractmethod
    def model(self) -> type[ModelType]:
        raise NotImplementedError

    @property
    @abstractmethod
    def crud(self) -> AbstractCRUDRepository[ModelType]:
        raise NotImplementedError
