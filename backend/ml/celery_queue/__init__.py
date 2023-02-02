"""Celery config"""
from celery import Celery

from app.loading import download_network_files
from app.parsing import from_dataframe
from ml.link_prediction import predict_edges

celery_queue = Celery(
    __name__,
    broker="amqp://localhost:5672",
    backend="redis://localhost:6379"
)

celery_queue.conf.update(
    accept_content={"pickle"},
    task_serializer="pickle",
    result_serializer="pickle",
    event_serializer="pickle",
)

# TODO: assign celery tasks
celery_queue.task(download_network_files)
celery_queue.task(from_dataframe)
celery_queue.task(predict_edges)
