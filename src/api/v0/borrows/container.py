from dependency_injector import containers, providers

from src.api.v0.borrows.repository import BorrowsRepository
from src.api.v0.borrows.repository import BooksRepository

from src.api.v0.borrows.service import BorrowsService


class BorrowsContainer(containers.DeclarativeContainer):
    scoped_session = providers.Dependency()  # type: ignore
    settings = providers.Dependency()  # type: ignore

    borrows_repo = providers.Factory(BorrowsRepository, session=scoped_session)
    books_repo = providers.Factory(BooksRepository, session=scoped_session)

    service = providers.Factory(
        BorrowsService,
        borrows_repo=borrows_repo,
        books_repo=books_repo,
        settings=settings,
    )
