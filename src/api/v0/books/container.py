from dependency_injector import containers, providers

from src.security.jwt import TokenHelper
from src.security.hasher import PasswordHasher

from src.api.v0.books.repository import BooksRepository


class BooksContainer(containers.DeclarativeContainer):
    scoped_session = providers.Dependency()  # type: ignore
    settings = providers.Dependency()  # type: ignore

    token_helper = providers.Factory(TokenHelper, settings=settings)
    hasher = providers.Factory(PasswordHasher)

    books_repo = providers.Factory(BooksRepository, session=scoped_session)
