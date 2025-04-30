from contextlib import asynccontextmanager
from dishka import AsyncContainer
from fastapi import FastAPI

from backend.infrastructure.database.connection.postgres_connection import DatabaseConnection


def add_bearer_scheme(app: FastAPI):
    openapi_schema = app.openapi()
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema


def create_lifespan(di_container: AsyncContainer):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        db = await di_container.get(DatabaseConnection)
        
        add_bearer_scheme(app)
        await db.create_tables()

        yield
    return lifespan
