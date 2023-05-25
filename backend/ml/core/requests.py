from typing import List
from pydantic import AnyHttpUrl

from core.camel import CamelModel


class MLRequest(CamelModel):
    nodes_file_url: AnyHttpUrl
    edges_file_url: AnyHttpUrl
    epochs: int = 100
    x_columns: List[str]
    train_percentage: float
    hidden_layer_sizes: List[int]
    learning_rate: float = 0.01
    ml_model_type: str
    seed: int = 42
    use_custom_split: bool = False


class ClassificationRequest(MLRequest):
    y_column: str
    train_percentage: float | None = None
