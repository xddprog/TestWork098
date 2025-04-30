from pydantic import BaseModel, EmailStr

from backend.core.dto.user_dto import BaseUserModel



class RegisterForm(BaseModel):
    name: str
    password: str
    email: EmailStr


class LoginForm(BaseModel):
    email: EmailStr
    password: str


class TokensModel(BaseModel):
    user: BaseUserModel
    access_token: str
    refresh_token: str
