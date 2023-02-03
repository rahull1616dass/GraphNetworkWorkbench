"""REST API"""
from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse, FileResponse

from core.typing import MLTask
from core.logging_helpers import get_logger
from app.workflows import (
    link_prediction_workflow,
    node_prediction_workflow
)

api = APIRouter()
logger = get_logger(__name__)

# TODO: implement node classification and edge prediction endpoints


@api.post("/link_pred")
async def link_prediction(task: MLTask = Body()):
    return await link_prediction_workflow(task)


@api.post("/node_class")
async def node_classification(task: MLTask = Body()):
    return await node_prediction_workflow(task)


@api.get("/")
async def index():
    return RedirectResponse("/docs")

@api.get("/nodes")
async def get_nodes():
    return FileResponse("nodes.csv")

@api.get("/edges")
async def get_nodes():
    return FileResponse("edges.csv")
