from celery import Celery
from dill import dumps, load
from kombu.utils.encoding import str_to_bytes
from kombu.serialization import pickle_loads, pickle_protocol, registry

from config import settings


def register_dill():
    def encode(obj, dumper=dumps):
        return dumper(obj, protocol=pickle_protocol)

    def decode(s):
        return pickle_loads(str_to_bytes(s), load=load)

    registry.register(
        name='dill',
        encoder=encode,
        decoder=decode,
        content_type='application/x-python-serialize',
        content_encoding='binary'
    )


register_dill()

celery_instance = Celery(
    __name__,
    broker=f"amqp://{settings.rabbitmq_host}:{settings.rabbitmq_port}",
    backend=f"redis://{settings.redis_host}:{settings.redis_port}"
)

celery_instance.conf.update(
    accept_content={"dill"},
    task_serializer="dill",
    result_serializer="dill",
    event_serializer="dill"
)
