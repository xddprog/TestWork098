from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi.security import HTTPAuthorizationCredentials
from jwt import InvalidTokenError, encode, decode

from backend.core.dto.auth_dto import LoginForm, RegisterForm
from backend.core.dto.user_dto import BaseUserModel
from backend.core.repositories.user_repository import UserRepository
from backend.infrastructure.config.auth_configs import JWT_CONFIG
from backend.infrastructure.database.models.user import User
from backend.infrastructure.errors.auth_errors import InvalidLoginData, InvalidToken, UserNotRegistered, UserAlreadyRegistered


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
    
    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repository.get_by_attribute("email", email, one=True)
    
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        password_bytes = plain_password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")
        try:
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except (ValueError, TypeError):
            return False

    async def hash_password(self, plain_password: str) -> str:
        password_bytes = plain_password.encode("utf-8")
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed_bytes.decode("utf-8")

    async def authenticate_user(self, form: LoginForm | RegisterForm) -> User:
        user = await self.get_user_by_email(form.email)
        if not user:
            raise UserNotRegistered
        if not await self.verify_password(form.password, user.password):
            raise InvalidLoginData
        return user

    async def create_access_token(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_CONFIG.JWT_ACCESS_TOKEN_TIME)
        data = {"exp": expire, "sub": str(user_id)}
        return encode(
            data,
            JWT_CONFIG.JWT_SECRET, 
            algorithm=JWT_CONFIG.JWT_ALGORITHM
        )
    
    async def create_refresh_token(self, user_id: int):
        expire = datetime.now(timezone.utc) + timedelta(days=JWT_CONFIG.JWT_REFRESH_TOKEN_TIME)
        data = {"exp": expire, "sub": str(user_id)}
        return encode(
            data, 
            JWT_CONFIG.JWT_SECRET, 
            algorithm=JWT_CONFIG.JWT_ALGORITHM
        )

    async def verify_token(self, token: str, is_refresh: bool = False) -> BaseUserModel:
        if not token:
            raise InvalidToken
        try:
            if not is_refresh:
                _, token = token.split()
            payload = decode(
                token,
                JWT_CONFIG.JWT_SECRET,
                algorithms=[JWT_CONFIG.JWT_ALGORITHM],
            )

            user_id = int(payload.get("sub"))
            user = await self.repository.get_item(user_id)
            if not user_id or not user:
                raise InvalidToken
            return BaseUserModel.model_validate(user, from_attributes=True)
        except (InvalidTokenError, AttributeError) as e:
            raise InvalidToken

    async def check_user_exist(self, email: str) -> BaseUserModel:
        user = await self.get_user_by_email(email)
        if user is None:
            raise InvalidToken
        return BaseUserModel.model_validate(user, from_attributes=True)

    async def register_user(self, form: RegisterForm) -> BaseUserModel:
        user = await self.get_user_by_email(form.email)
        if user:
            raise UserAlreadyRegistered

        form.password = await self.hash_password(form.password)
        new_user = await self.repository.add_item(**form.model_dump())
        return BaseUserModel.model_validate(new_user, from_attributes=True)
    
    async def login_user(self, form: LoginForm) -> BaseUserModel:
        user = await self.authenticate_user(form)
        access_token = await self.create_access_token(user.id)
        refresh_token = await self.create_refresh_token(user.id)
        return BaseUserModel.model_validate(user, from_attributes=True), access_token, refresh_token