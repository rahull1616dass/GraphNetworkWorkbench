from pydantic import BaseSettings


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: str = "6379"
    rabbitmq_host: str = "localhost"
    rabbitmq_port: str = "5672"
    rabbitmq_user: str = "guest"
    rabbitmq_password: str = "guest"

    class Config:
        env_file = ".env"
