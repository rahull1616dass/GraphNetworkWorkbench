import mlflow

from config import settings

mlflow.set_tracking_uri(f"file:{settings.mlflow_uri}")
