"""REST API"""
from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse, FileResponse

from core.loggers import get_logger
from app.workflows import (
    link_prediction_workflow,
    node_classification_workflow
)
from core.requests import MLRequest, ClassificationRequest
from core.responses import NodeClassResponse, EdgePredResponse

api = APIRouter()
logger = get_logger(__name__)


@api.post("/link_pred")
async def link_prediction(task: MLRequest = Body()):
    losses, val_scores, test_score, predictions =  await link_prediction_workflow(task)
    response = EdgePredResponse(
        losses=losses,
        score=test_score,
        validation_scores=val_scores,
        predictions=predictions
    )
    return response


@api.post("/node_class")
async def node_classification(task: ClassificationRequest = Body()):
    losses, predictions, accuracy =  await node_classification_workflow(task)
    response = NodeClassResponse(
        losses=losses,
        predictions=predictions,
        accuracy=accuracy
    )
    return response


@api.get("/")
async def index():
    return RedirectResponse("/docs")


@api.get("/n")
async def n():
    return FileResponse("nodes.csv")


@api.get("/e")
async def e():
    return FileResponse("edges.csv")
