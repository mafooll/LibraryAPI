from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, HTTPException

from dependency_injector.wiring import Provide, inject

from src.api.v0.auth.container import AuthContainer
from src.api.v0.auth.service import AuthService
from src.api.v0.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    AuthUserResponse,
    MessageResponse,
    MeResponse,
)


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/me", response_model=MeResponse)
def get_me(request: Request):
    if not request.state.user or not request.state.user.is_authenticated:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"id": request.state.user.id}


@auth_router.post("/register", response_model=AuthUserResponse)
@inject
async def register(
    data: RegisterRequest,
    service: Annotated[AuthService, Depends(Provide[AuthContainer.service])],
):
    return await service.register(data)


@auth_router.post("/login", response_model=MessageResponse)
@inject
async def login(
    data: LoginRequest,
    response: Response,
    service: Annotated[AuthService, Depends(Provide[AuthContainer.service])],
):
    return await service.login(data, response)


@auth_router.post("/logout", response_model=MessageResponse)
@inject
async def logout(
    request: Request,
    response: Response,
    service: Annotated[AuthService, Depends(Provide[AuthContainer.service])],
):
    await service.logout(request, response)
    return {"message": "Logged out"}


@auth_router.post("/refresh", response_model=MessageResponse)
@inject
async def refresh(
    request: Request,
    response: Response,
    service: Annotated[AuthService, Depends(Provide[AuthContainer.service])],
):
    return await service.refresh_tokens(request, response)
