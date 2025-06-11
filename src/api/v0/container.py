from dependency_injector import containers, providers

from src.api.v0.hello.container import HelloContainer


class V0Container(containers.DeclarativeContainer):
    engine = providers.Dependency()             # type: ignore
    scoped_session = providers.Dependency()     # type: ignore

    hello_container = providers.Container(
        HelloContainer,
        scoped_session=scoped_session
    )
