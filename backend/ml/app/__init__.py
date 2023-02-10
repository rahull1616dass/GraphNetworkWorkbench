from fastapi import FastAPI

from app.api import api
from task_manager import celery_instance


def create_app():
    app = FastAPI()
    app.include_router(api)
    app.task_manager = celery_instance
    return app
