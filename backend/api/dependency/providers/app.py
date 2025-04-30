import asyncio
from dishka import Provider, Scope, provide
from fastapi import Request

from backend.infrastructure.config.database_configs import DB_CONFIG
from backend.infrastructure.database.connection.postgres_connection import DatabaseConnection


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_db_connection(self) -> DatabaseConnection:
        return DatabaseConnection(DB_CONFIG)
