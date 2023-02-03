import asyncio
from celery import chain

from task_manager_queue.tasks import (
    convert_task,
    download_task,
    edge_prediction_task
)
from core.typing import MLTask
from core.logging_helpers import get_logger

logger = get_logger(__name__)


async def run_workflow(pipe):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pipe().get)


async def link_prediction_workflow(task: MLTask):
    logger.info("The link prediction workflow is run")
    pipe = chain(download_task.s(task), convert_task.s(task), edge_prediction_task.s(task))
    return await run_workflow(pipe)