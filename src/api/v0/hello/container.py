from dependency_injector import containers, providers

from src.api.v0.hello.hello_repo import HelloRepository


class HelloContainer(containers.DeclarativeContainer):
    scoped_session = providers.Dependency()     # type: ignore

    hello_repo = providers.Factory(
        HelloRepository,
        session=scoped_session                  # type: ignore
    )
