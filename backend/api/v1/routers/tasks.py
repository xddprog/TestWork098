from datetime import datetime
from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from backend.core import services
from backend.core.dto.task_dto import CreateTaskModel, TaskModel, UpdateTaskModel
from backend.core.dto.user_dto import BaseUserModel
from backend.utils.enums import TaskStatuses



router = APIRouter()


@router.post("", status_code=201)
@inject
async def create_task(
    form: CreateTaskModel,
    task_service: FromDishka[services.TaskService],
    current_user: FromDishka[BaseUserModel]
) -> TaskModel:
    return await task_service.create_task(form, current_user.id)


@router.get("/search")
@inject
async def search_tasks(
    q: str,
    task_service: FromDishka[services.TaskService],
    current_user: FromDishka[BaseUserModel]
) -> list[TaskModel]:
    return await task_service.search_tasks(q)


@router.put('/{task_id}')
@inject
async def update_task(
    task_id: int,
    form: UpdateTaskModel,
    task_service: FromDishka[services.TaskService],
    current_user: FromDishka[BaseUserModel]
) -> TaskModel:
    return await task_service.update_task(task_id, form)


@router.get("")
@inject
async def get_filtered_tasks(
    task_service: FromDishka[services.TaskService],
    current_user: FromDishka[BaseUserModel],
    status: TaskStatuses | None = None,
    priority: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[TaskModel]:
    return await task_service.get_filtered_tasks(status, priority, date_from, date_to)