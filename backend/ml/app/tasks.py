from celery import chain

from core.typing import MLTask
from celery_queue import celery_queue
from celery_queue.pipe_running import run_pipe

# TODO: create functions signatures
load_network_files = celery_queue.signature("app.loading.download_network_files")
create_graph_data = celery_queue.signature("app.parsing.from_dataframe")
train_and_estimate_link_pred = celery_queue.signature("ml.link_prediction.predict_edges")

async def link_prediction_task(task: MLTask):
    pipe = chain(load_network_files.s(task), create_graph_data.s(task), train_and_estimate_link_pred.s(task))
    return await run_pipe(pipe)