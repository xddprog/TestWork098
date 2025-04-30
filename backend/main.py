from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from backend.api.dependency.setup import setup_container
from backend.api.v1.routers import v1_router
from backend.utils.init_app import create_lifespan


di_container = setup_container()
app = FastAPI(lifespan=create_lifespan(di_container))


setup_dishka(di_container, app)
app.include_router(v1_router, prefix="/api")
