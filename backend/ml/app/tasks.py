import asyncio
from celery import chain, Celery

import celery_queue
from core.typing import MLTask


celery_instance = Celery(
    __name__,
    broker="amqp://localhost:5672",
    backend="redis://localhost:6379"
)

celery_instance.conf.update(
    accept_content={"pickle"},
    task_serializer="pickle",
    result_serializer="pickle",
    event_serializer="pickle"
)

download_task = celery_instance.signature("preprocessing.loading.download_network_files")
parse_task = celery_instance.signature("preprocessing.parsing.from_dataframe")
edge_predict_task = celery_instance.signature("ml.link_prediction.predict_edges")


async def run_pipe(chain):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, chain.get)


async def link_prediction_task(task: MLTask):
    pipe = chain(download_task(task), parse_task(task), edge_predict_task(task))
    return await run_pipe(pipe)