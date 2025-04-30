from datetime import datetime
from backend.core.dto.task_dto import CreateTaskModel, TaskModel, UpdateTaskModel
from backend.core.repositories import TaskRepository
from backend.core.services.base import BaseDbModelService
from backend.infrastructure.errors.task_errors import TaskNotFoundError
from backend.utils.enums import TaskStatuses


class TaskService(BaseDbModelService[TaskRepository]):
    async def check_item(self, task_id: int):
        task = await self.repository.get_item(task_id)
        if not task:
            raise TaskNotFoundError
        
    async def create_task(self, form: CreateTaskModel, user_id: int) -> TaskModel:
        new_task = await self.repository.add_item(**form.model_dump(), owner_id=user_id)
        return TaskModel.model_validate(new_task, from_attributes=True)
    
    async def update_task(self, task_id: int, form: UpdateTaskModel) -> TaskModel:
        await self.check_item(task_id)
        task = await self.repository.update_item(task_id, **form.model_dump(exclude_none=True))
        return TaskModel.model_validate(task, from_attributes=True)
    
    async def search_tasks(self, substring: str) -> list[TaskModel]:
        tasks = await self.repository.get_tasks_by_substring(substring)
        return [
            TaskModel.model_validate(task, from_attributes=True)
            for task in tasks
        ]
        
    async def get_filtered_tasks(
        self, 
        status: TaskStatuses | None, 
        priorty: int | None, 
        date_from: datetime | None, 
        date_to: datetime | None
    ):
        tasks = await self.repository.get_filtered_tasks(status, priorty, date_from, date_to)
        return [
            TaskModel.model_validate(task, from_attributes=True)
            for task in tasks
        ]