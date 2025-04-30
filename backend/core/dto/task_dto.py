from datetime import datetime
from pydantic import BaseModel

from backend.utils.enums import TaskStatuses


class CreateTaskModel(BaseModel):
    title: str
    description: str | None = None
    priority: int

    
class UpdateTaskModel(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: int | None = None
    status: TaskStatuses | None = None


class TaskModel(BaseModel):
    id: int
    owner_id: int
    created_at: datetime
    title: str
    description: str | None = None
    priority: int
    status: TaskStatuses