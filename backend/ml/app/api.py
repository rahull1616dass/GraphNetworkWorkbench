"""REST API"""
from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse, FileResponse

from core.typing import MLTask
from core.logging_helpers import get_logger
from app.workflows import link_prediction_workflow

api = APIRouter()
logger = get_logger(__name__)

# TODO: implement node classification and edge prediction endpoints


@api.post("/link_pred")
async def link_prediction(task: MLTask = Body()):
    return await link_prediction_workflow(task)


@api.get("/node_class")
async def node_classification():
    return {"msg": "Node classification is not implemented"}


@api.get("/")
async def index():
    return RedirectResponse("/docs")

@api.get("/nodes")
async def get_nodes():
    return FileResponse("nodes.csv")

@api.get("/edges")
async def get_nodes():
    return FileResponse("edges.csv")
