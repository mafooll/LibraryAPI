from dependency_injector import containers, providers

from src.security.jwt import TokenHelper
from src.security.hasher import PasswordHasher

from src.api.v0.readers.repository import ReadersRepository


class ReadersContainer(containers.DeclarativeContainer):
    scoped_session = providers.Dependency()  # type: ignore
    settings = providers.Dependency()  # type: ignore

    token_helper = providers.Factory(TokenHelper, settings=settings)
    hasher = providers.Factory(PasswordHasher)

    readers_repo = providers.Factory(ReadersRepository, session=scoped_session)
