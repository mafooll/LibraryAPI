from datetime import datetime, timezone

from src.common.interfaces.repository import BaseRepository
from src.database.repositories.crud import CRUDRepository
from src.database.models.token import Token
from src.database.models.librarian import Librarian

from src.database.utils.transactional import transactional

from src.api.v0.auth.schemas import LibrarianCreate


class TokenRepository(BaseRepository[Token]):
    @property
    def crud(self) -> CRUDRepository[Token]:
        return CRUDRepository(self.session, self.model)

    @property
    def model(self) -> type[Token]:
        return Token

    @transactional
    async def create(
        self, user_id: int, refresh_token: str, refresh_expires_at: datetime
    ) -> Token | None:
        return await self.crud.insert(
            user_id=user_id,
            refresh_token=refresh_token,
            refresh_expires_at=refresh_expires_at,
            is_valid=True,
        )

    @transactional
    async def invalidate(self, refresh_token: str) -> None:
        await self.crud.update(
            self.model.refresh_token == refresh_token, is_valid=False
        )

    async def get_valid_by_token(self, refresh_token: str) -> Token | None:
        token = await self.crud.select(
            (self.model.refresh_token == refresh_token)
            & (self.model.is_valid.is_(True))
            & (self.model.refresh_expires_at > datetime.now(timezone.utc))
        )
        return token if token else None


class LibrarianRepository(BaseRepository[Librarian]):
    @property
    def crud(self) -> CRUDRepository[Librarian]:
        return CRUDRepository(self.session, self.model)

    @property
    def model(self) -> type[Librarian]:
        return Librarian

    @transactional
    async def create(self, data: LibrarianCreate) -> Librarian | None:
        return await self.crud.insert(**data.model_dump())

    async def get_by_id(self, librarian_id: int) -> Librarian | None:
        return await self.crud.select(self.model.id == librarian_id)

    async def get_by_email(self, librarian_email: str) -> Librarian | None:
        return await self.crud.select(self.model.email == librarian_email)
