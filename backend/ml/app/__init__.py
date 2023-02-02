from fastapi import FastAPI

from app.api import api


def create_app():
    app = FastAPI()
    app.include_router(api)
    return app
