from pydantic import BaseSettings


class Settings(BaseSettings):
    redis_host: str
    redis_port: str
    rabbitmq_host: str
    rabbitmq_port: str

    class Config:
        env_file = ".env"
