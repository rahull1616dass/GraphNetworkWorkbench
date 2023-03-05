"""REST API"""
from celery import chain
from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse, FileResponse

from core.loggers import get_logger
from app.workflows import (
    link_prediction_workflow,
    node_classification_workflow
)
from app.workflows import run_workflow
from core.requests import MLRequest, ClassificationRequest
from core.responses import NodeClassResponse, EdgePredResponse
from task_manager.tasks import get_class_expert_opinion_task, get_pred_expert_opinion_task

api = APIRouter()
logger = get_logger(__name__)


@api.post("/link_pred")
async def link_prediction(request: MLRequest = Body()):
    losses, val_scores, test_score, predictions =  await link_prediction_workflow(request)
    expert_opinion = await run_workflow(chain(get_pred_expert_opinion_task.s(request, losses, val_scores, test_score)))
    response = EdgePredResponse(
        losses=losses,
        score=test_score,
        validation_scores=val_scores,
        predictions=predictions,
        expert_opinion=expert_opinion
    )
    return response


@api.post("/node_class")
async def node_classification(request: ClassificationRequest = Body()):
    losses, val_acc_scores, accuracy, predictions =  await node_classification_workflow(request)
    expert_opinion = await run_workflow(chain(get_class_expert_opinion_task.s(request, losses, val_acc_scores, accuracy)))
    response = NodeClassResponse(
        losses=losses,
        predictions=predictions,
        accuracy=accuracy,
        expert_opinion=expert_opinion
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
