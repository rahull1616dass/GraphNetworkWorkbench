from fastapi_healthchecks.checks.redis import RedisCheck
from fastapi_healthchecks.checks.rabbit_mq import RabbitMqCheck
from fastapi_healthchecks.api.router import HealthcheckRouter, Probe, Check, CheckResult

from config import settings
from task_manager import celery_instance

class CeleryCheck(Check):
    async def __call__(self, *args, **kwargs) -> CheckResult:
        result = celery_instance.control.inspect().active()
        if result:
            return CheckResult(name="Celery", passed=True)
        else:
            return CheckResult(name="Celery", passed=False, details="No Celery worker")

healthcheck_router = HealthcheckRouter(
    Probe(
        name="health",
        checks=[
            RedisCheck(host=settings.redis_host, port=int(settings.redis_port)),
            RabbitMqCheck(host=settings.rabbitmq_host, port=int(settings.rabbitmq_port), user=settings.rabbitmq_user, password=settings.rabbitmq_password, secure=False),
            CeleryCheck()
        ]
    )
)
