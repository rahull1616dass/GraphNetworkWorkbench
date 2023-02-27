import asyncio

from celery import chain

from task_manager.tasks import (
    convert_for_pred_task,
    convert_for_class_task,
    download_task,
    edge_prediction_task,
    node_classification_task
)
from core.types import MLTask, ClassificationTask
from core.logging_helpers import get_logger

logger = get_logger(__name__)


async def run_workflow(pipe):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pipe().get)


async def link_prediction_workflow(task: MLTask):
    pipe = chain(download_task.s(task), convert_for_pred_task.s(task), edge_prediction_task.s(task))
    return await run_workflow(pipe)

async def node_classification_workflow(task: ClassificationTask):
    pipe = chain(download_task.s(task), convert_for_class_task.s(task), node_classification_task.s(task))
    return await run_workflow(pipe)
