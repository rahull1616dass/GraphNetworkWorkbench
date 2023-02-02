"""REST API"""
from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse

from core.typing import MLTask
from app.tasks import link_prediction_task

api = APIRouter()

# TODO: implement node classification and edge prediction endpoints


@api.post("/link_pred")
async def link_prediction(task: MLTask = Body()):
    return await link_prediction_task(task)


@api.get("/node_class")
async def node_classification():
    return {"msg": "Node classification is not implemented"}


@api.get("/")
async def index():
    return RedirectResponse("/docs")
