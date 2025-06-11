from asyncio import run

from src.core.server import run_uvicorn
from src.api.setup import init_app


async def main():
    app = init_app()
    await run_uvicorn(app)


if __name__ == "__main__":
    run(main())
