from dishka import provide, Scope
from backend.api.dependency.providers.app import AppProvider
from backend.infrastructure.config.database_configs import DB_CONFIG
from backend.infrastructure.database.connection.postgres_connection import DatabaseConnection


class TestAppProvider(AppProvider):
    @provide(scope=Scope.APP)
    async def get_db_connection(self) -> DatabaseConnection:
        return DatabaseConnection(DB_CONFIG)