from dependency_injector import containers, providers

from src.api.v0.auth.repository import TokenRepository
from src.api.v0.auth.repository import LibrarianRepository

from src.api.v0.auth.service import AuthService

from src.security.jwt import TokenHelper
from src.security.hasher import PasswordHasher


class AuthContainer(containers.DeclarativeContainer):
    scoped_session = providers.Dependency()     # type: ignore
    settings = providers.Dependency()           # type: ignore

    token_repo = providers.Factory(
        TokenRepository,
        session=scoped_session
    )
    librarian_repo = providers.Factory(
        LibrarianRepository,
        session=scoped_session
    )

    token_helper = providers.Factory(
        TokenHelper,
        settings=settings
    )
    hasher = providers.Factory(
        PasswordHasher
    )

    service = providers.Factory(
        AuthService,
        token_repo=token_repo,
        librarian_repo=librarian_repo,
        settings=settings,
        token_helper=token_helper,
        hasher=hasher
    )
