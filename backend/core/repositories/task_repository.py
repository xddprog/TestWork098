from datetime import datetime
from sqlalchemy import or_, select
from backend.core.repositories.base import SqlAlchemyRepository
from backend.infrastructure.database.models.task import Task
from backend.utils.enums import TaskStatuses


class TaskRepository(SqlAlchemyRepository[Task]):
    def __init__(self, session):
        super().__init__(session, Task)

    async def get_tasks_by_substring(self, substring: str) -> list[Task]:
        query = (
            select(self.model)
            .where(
                self.model.title.contains(substring) |
                self.model.description.contains(substring)
            )
        )
        return (await self.session.execute(query)).scalars().all()
    
    async def get_filtered_tasks(
        self, 
        status: TaskStatuses | None, 
        priority: int | None,
        date_from: datetime | None,
        date_to: datetime | None
    ) -> list[Task]:
        query = select(self.model)
        
        if status is not None:
            query = query.where(self.model.status == status)

        if priority is not None:
            query = query.where(self.model.priority == priority)

        if date_from is not None:
            query = query.where(self.model.created_at >= date_from)

        if date_to is not None:
            query = query.where(self.model.created_at <= date_to)
        return (await self.session.execute(query)).scalars().all()