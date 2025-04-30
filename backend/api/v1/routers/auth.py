from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse

from backend.core import services
from backend.core.dto.auth_dto import LoginForm, TokensModel, RegisterForm
from backend.core.dto.user_dto import BaseUserModel


router = APIRouter()


@router.get("/current_user")
@inject
async def get_current_user(
    current_user: FromDishka[BaseUserModel],
) -> BaseUserModel:
    return current_user


@router.post("/login")
@inject
async def login_user(
    form: LoginForm,
    auth_service: FromDishka[services.AuthService]
) -> TokensModel:
    user, access_token, refresh_token = await auth_service.login_user(form)
    return TokensModel(
        user=user,
        access_token=access_token, 
        refresh_token=refresh_token
    )


@router.post("/refresh")
@inject
async def refresh_token(
    refresh_token: str,
    auth_service: FromDishka[services.AuthService]
) -> TokensModel:
    user = await auth_service.verify_token(refresh_token, is_refresh=True)
    access_token = await auth_service.create_access_token(user.id)
    return TokensModel(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token
    )
    

@router.post("/register", status_code=201)
@inject
async def register_user(
    form: RegisterForm,
    auth_service: FromDishka[services.AuthService],
) -> BaseUserModel:
    await auth_service.register_user(form)
    return JSONResponse(
        content={"message": "User successfully registered. Please login."}
    )
