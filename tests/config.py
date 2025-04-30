from environs import Env
from pydantic import BaseModel

from backend.infrastructure.config.database_configs import DatabaseConfig


env = Env()
env.read_env(".env.tests")

class TestDatabaseConfig(BaseModel):
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_HOST: str
    TEST_DB_PORT: str


    def get_postgres_url(self, is_async: bool = True):
        if is_async:
            return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        return f"postgresql://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"


TEST_DB_CONFIG = TestDatabaseConfig(
    **{field: env(field.upper()) for field in TestDatabaseConfig.model_fields}
)

