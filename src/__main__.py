from asyncio import run

from src.core.server import run_uvicorn
from src.api.setup import init_app

from src.database.setup import create_tables, drop_tables
from src.core.container import CoreContainer

from src.api.v0.middlewares.session import ScopedSessionMiddleware


async def main():
    container = CoreContainer()
    container.wire(modules=[__name__])

    v0_api = container.v0_api()
    v0_api.wire(packages=["src.api.v0"])

    hello_container = v0_api.hello_container()
    hello_container.wire(packages=["src.api.v0.hello"])

    engine = container.engine()

    await create_tables(engine=engine)

    try:
        app = init_app()
        # app.container = container
        app.add_middleware(ScopedSessionMiddleware)
        await run_uvicorn(app)
    except Exception as e:
        print(e)
    finally:
        await drop_tables(engine=engine)


if __name__ == "__main__":
    run(main())
