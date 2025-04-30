from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from backend.infrastructure.config.database_configs import DB_CONFIG, DatabaseConfig
from backend.infrastructure.database.models.base import Base

class DatabaseConnection:
    def __init__(self, settings: DatabaseConfig):    
        self.__engine = create_async_engine(
            url=settings.get_postgres_url(),
            poolclass=NullPool
        )

    async def get_session(self) -> AsyncSession:
        return AsyncSession(bind=self.__engine)

    async def create_tables(self):
        async with self.__engine.begin() as conn:
            if DB_CONFIG.DROP:
                await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
