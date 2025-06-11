from typing import Any, Callable, Awaitable

from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.utils.scoped import get_context


def transactional(func: Callable[..., Awaitable[Any]]):
    @wraps(func)
    async def _transactional(self: Any, *args: Any, **kwargs: Any):
        session: AsyncSession = self.session if isinstance(
            self.session, AsyncSession
        ) else self.session()

        try:
            if session.in_transaction():
                result = await func(self, *args, **kwargs)
                await session.commit()
                return result

            async with session.begin():
                result = await func(self, *args, **kwargs)

            return result

        except Exception as error:
            print(f'{error}\ncontext:{get_context()}')
            await session.rollback()
            raise

    return _transactional
