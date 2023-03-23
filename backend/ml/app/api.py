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
    losses, val_scores, accuracy, precision, recall, f1, auc_roc, predictions = await link_prediction_workflow(request)
    expert_opinion = await run_workflow(
        chain(get_pred_expert_opinion_task.s(request, losses, val_scores, accuracy, precision, recall, f1, auc_roc)))

    response = EdgePredResponse(
        losses=losses,
        valScores=val_scores,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1=f1,
        auc=auc_roc,
        predictions=predictions,
        expertOpinion=expert_opinion
    )
    return response.dict(by_alias=True)


@api.post("/node_class")
async def node_classification(request: ClassificationRequest = Body()):
    losses, val_scores, accuracy, precision, recall, f1, auc_roc, predictions, train_percentage = \
        await node_classification_workflow(request)
    request.train_percentage = train_percentage
    expert_opinion = await run_workflow(
        chain(get_class_expert_opinion_task.s(request, losses, val_scores, accuracy, precision, recall, f1, auc_roc)))

    response = NodeClassResponse(
        losses=losses,
        valScores=val_scores,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1=f1,
        auc=auc_roc,
        predictions=predictions,
        expertOpinion=expert_opinion
    )
    return response.dict(by_alias=True)


@api.get("/")
async def index():
    return RedirectResponse("/docs")
