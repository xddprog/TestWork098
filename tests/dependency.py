from dishka import provide, Scope
from backend.api.dependency.providers.app import AppProvider
from backend.infrastructure.config.database_configs import DB_CONFIG
from backend.infrastructure.database.connection.postgres_connection import DatabaseConnection
from tests.config import TEST_DB_CONFIG


class TestAppProvider(AppProvider):
    @provide(scope=Scope.APP)
    async def get_db_connection(self) -> DatabaseConnection:
        return DatabaseConnection(TEST_DB_CONFIG)