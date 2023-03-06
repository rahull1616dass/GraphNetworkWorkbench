import asyncio

from celery import chain

from task_manager.tasks import (
    convert_for_pred_task,
    convert_for_class_task,
    download_task,
    edge_prediction_task,
    node_classification_task
)
from core.params import MLParams, ClassificationParams
from core.loggers import get_logger
from core.requests import MLRequest, ClassificationRequest

logger = get_logger(__name__)


async def run_workflow(pipe):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pipe().get)


async def link_prediction_workflow(request: MLRequest):
    params: MLParams = MLParams(**request.dict(exclude={"nodes_file_url", "edges_file_url"}))
    pipe = chain(download_task.s(request), convert_for_pred_task.s(params), edge_prediction_task.s(params))
    return await run_workflow(pipe)

async def node_classification_workflow(request: ClassificationRequest):
    params: MLParams = ClassificationParams(**request.dict(exclude={"nodes_file_url", "edges_file_url"}))
    pipe = chain(download_task.s(request), convert_for_class_task.s(params), node_classification_task.s(params))
    return await run_workflow(pipe)
