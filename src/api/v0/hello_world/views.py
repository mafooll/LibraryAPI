# from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter

hello_router = APIRouter()


@hello_router.get("/hello")
async def hello():
    print("hello")
    return {"message": "Hello World"}
