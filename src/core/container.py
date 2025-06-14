from dependency_injector import containers, providers

from sqlalchemy.ext.asyncio import async_scoped_session

from src.database.utils.scoped import get_context
from src.database.setup import create_engine, create_session_factory

from src.core.settings import get_settings

from src.api.v0.container import V0Container


class CoreContainer(containers.DeclarativeContainer):
    settings = providers.ThreadSafeSingleton(get_settings)

    engine = providers.ThreadSafeSingleton(create_engine, settings)

    session_factory = providers.Factory(
        create_session_factory, settings=settings, engine=engine
    )

    scoped_session = providers.ThreadSafeSingleton(
        async_scoped_session,
        session_factory=session_factory,
        scopefunc=get_context,
    )

    v0_api = providers.Container(
        V0Container,
        engine=engine,
        scoped_session=scoped_session,
        settings=settings,
    )
