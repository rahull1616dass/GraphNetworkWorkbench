from typing import List
from pydantic import BaseModel, AnyHttpUrl

from humps import camelize


def to_camel(snake_case: str):
    return camelize(snake_case)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field = True


class MLRequest(CamelModel):
    nodes_file_url: AnyHttpUrl
    edges_file_url: AnyHttpUrl
    epochs: int = 100
    x_columns: List[str]
    train_percentage: float = 0.85
    hidden_layer_sizes: List[int]
    learning_rate: float = 0.01
    ml_model_type: str
    seed: int = 42


class ClassificationRequest(MLRequest):
    y_column: str
