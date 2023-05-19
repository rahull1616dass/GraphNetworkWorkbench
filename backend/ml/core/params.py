from typing import List

from pydantic import BaseModel


class MLParams(BaseModel):
    epochs: int = 100
    train_percentage: float
    hidden_layer_sizes: List[int]
    learning_rate: float = 0.01
    ml_model_type: str
    seed: int = 42
    x_columns: List[str]
    use_custom_split: bool = False


class ClassificationParams(MLParams):
    y_column: str
    train_percentage: float | None = None
