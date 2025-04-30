from pydantic import BaseModel


class BaseUserModel(BaseModel):
    id: int
    name: str
    email: str | None = None
