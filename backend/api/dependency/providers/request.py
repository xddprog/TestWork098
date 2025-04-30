from typing import AsyncIterable
from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import inject
from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core import repositories, services
from backend.core.dto.user_dto import BaseUserModel
from backend.infrastructure.database.connection.postgres_connection import DatabaseConnection


bearer = HTTPBearer(auto_error=False)


class RequestProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_session(self, db_connection: DatabaseConnection) -> AsyncIterable[AsyncSession]:
        session = await db_connection.get_session()
        try:
            yield session
        except:
            await session.rollback()
        finally:
            await session.close()

    @provide(scope=Scope.REQUEST)
    async def get_auth_service(self, session: AsyncSession) -> services.AuthService:
        return services.AuthService(repository=repositories.UserRepository(session=session))
    
    @provide(scope=Scope.REQUEST)
    async def get_task_service(self, session: AsyncSession) -> services.TaskService:
        return services.TaskService(repository=repositories.TaskRepository(session=session))

    @provide(scope=Scope.REQUEST)
    async def get_current_user(
        self, 
        auth_service: services.AuthService,
        request: Request
    ) -> BaseUserModel:
        token = request.headers.get('Authorization')
        user = await auth_service.verify_token(token)
        return user
