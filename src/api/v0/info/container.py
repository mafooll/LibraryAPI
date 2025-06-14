from dependency_injector import containers, providers

from src.api.v0.info.repository import InfoRepository


class InfoContainer(containers.DeclarativeContainer):
    scoped_session = providers.Dependency()  # type: ignore
    settings = providers.Dependency()  # type: ignore

    info_repo = providers.Factory(InfoRepository, session=scoped_session)
