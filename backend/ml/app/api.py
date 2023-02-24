"""REST API"""
from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse, FileResponse

from core.logging_helpers import get_logger
from app.workflows import (
    link_prediction_workflow,
    node_classification_workflow
)
from core.types import MLTask, NodeClassResponse, EdgePredResponse, ClassificationTask

api = APIRouter()
logger = get_logger(__name__)


@api.post("/link_pred")
async def link_prediction(task: MLTask = Body()):
    losses, val_scores, test_score, predictions =  await link_prediction_workflow(task)
    response = EdgePredResponse(
        losses=losses,
        score=test_score,
        validation_scores=val_scores,
        predictions=predictions
    )
    return response


@api.post("/node_class")
async def node_classification(task: ClassificationTask = Body()):
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
