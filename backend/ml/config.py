import threading
from pydantic import BaseSettings


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: str = "6379"
    rabbitmq_host: str = "localhost"
    rabbitmq_port: str = "5672"
    rabbitmq_user: str = "guest"
    rabbitmq_password: str = "guest"
    mlflow_uri: str = "./mlflow"
    chatgpt_api_key: str
    expert_model: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"

    _instance = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)

        return cls._instance

settings = Settings()
