from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from src.core.settings import Settings

from src.database.models.base import BaseModel


def create_engine(settings: Settings) -> AsyncEngine:
    return create_async_engine(
        url=settings.database.url,
        echo=settings.alchemy.echo,
        echo_pool=settings.alchemy.echo_pool,
        pool_size=settings.alchemy.pool_size,
        pool_recycle=settings.alchemy.pool_recycle,
        pool_timeout=settings.alchemy.pool_timeout,
        max_overflow=settings.alchemy.max_overflow,
    )


def create_session_factory(
    settings: Settings, engine: AsyncEngine
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        autoflush=settings.alchemy.autoflush,
        expire_on_commit=settings.alchemy.expire_on_commit,
    )


async def create_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def drop_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
