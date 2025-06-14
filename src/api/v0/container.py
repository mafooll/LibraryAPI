from dependency_injector import containers, providers

from src.api.v0.auth.container import AuthContainer
from src.api.v0.readers.container import ReadersContainer


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
