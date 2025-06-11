from typing import Any

from uvicorn import Config, Server
from fastapi import FastAPI


async def run_uvicorn(app: FastAPI, **kw: Any) -> None:
    server = Server(
        Config(
            app,
            host="0.0.0.0",
            port=8000,
            **kw,
        )
    )
    await server.serve()
