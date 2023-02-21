from celery import Celery

from config import Settings


settings = Settings()

celery_instance = Celery(
    __name__,
    broker=f"amqp://{settings.rabbitmq_host}:{settings.rabbitmq_port}",
    backend=f"redis://{settings.redis_host}:{settings.redis_port}"
)

celery_instance.conf.update(
    accept_content={"pickle"},
    task_serializer="pickle",
    result_serializer="pickle",
    event_serializer="pickle"
)
