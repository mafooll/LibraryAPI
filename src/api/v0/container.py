from dependency_injector import containers, providers

from src.api.v0.auth.container import AuthContainer
from src.api.v0.readers.container import ReadersContainer
from src.api.v0.books.container import BooksContainer
from src.api.v0.borrows.container import BorrowsContainer
from src.api.v0.info.container import InfoContainer


class V0Container(containers.DeclarativeContainer):
    engine = providers.Dependency()  # type: ignore
    scoped_session = providers.Dependency()  # type: ignore
    settings = providers.Dependency()  # type: ignore

    auth_container = providers.Container(
        AuthContainer, scoped_session=scoped_session, settings=settings
    )
    readers_container = providers.Container(
        ReadersContainer, scoped_session=scoped_session, settings=settings
    )
    books_container = providers.Container(
        BooksContainer, scoped_session=scoped_session, settings=settings
    )
    borrows_container = providers.Container(
        BorrowsContainer, scoped_session=scoped_session, settings=settings
    )
    info_container = providers.Container(
        InfoContainer, scoped_session=scoped_session, settings=settings
    )
