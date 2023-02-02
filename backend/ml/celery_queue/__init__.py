"""Celery config"""
from celery import Celery

from celery_queue.tasks import get_random_number, count_numbers

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
