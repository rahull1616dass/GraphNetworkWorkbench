from fastapi import FastAPI

from app.api import api
from task_manager import celery_instance
from app.health import healthcheck_router


def create_app():
    app = FastAPI()
    app.include_router(api)
    app.include_router(healthcheck_router)
    app.task_manager = celery_instance
    return app
