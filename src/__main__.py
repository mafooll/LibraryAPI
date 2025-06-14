from asyncio import run

from src.core.server import run_uvicorn
from src.api.setup import init_app

from src.database.setup import create_tables, drop_tables
from src.core.container import CoreContainer

from src.api.v0.middlewares.session import ScopedSessionMiddleware
from src.api.v0.auth.middleware import AuthMiddleware


async def main():
    container = CoreContainer()
    container.wire(modules=[__name__])

    v0_api = container.v0_api()
    v0_api.wire(packages=["src.api.v0"])

    auth_container = v0_api.auth_container()
    auth_container.wire(packages=["src.api.v0.auth"])

    readers_container = v0_api.readers_container()
    readers_container.wire(packages=["src.api.v0.readers"])

    engine = container.engine()

    await create_tables(engine=engine)

    try:
        app = init_app()
        app.add_middleware(ScopedSessionMiddleware)
        app.add_middleware(AuthMiddleware)

        await run_uvicorn(app)
    except Exception as e:
        print(e)
    finally:
        await drop_tables(engine=engine)


if __name__ == "__main__":
    run(main())
