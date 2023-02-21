from typing import List
from pydantic import BaseModel, AnyHttpUrl

from humps import camelize


def to_camel(snake_case: str):
    return camelize(snake_case)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field = True


class MLTask(CamelModel):
    nodes_file_url: AnyHttpUrl
    edges_file_url: AnyHttpUrl
    epochs: int = 100
    train_percentage: float = 0.85
    val_percentage: float = 0.1


class NodeClassResponse(BaseModel):
    losses: List[float]
    predictions: List[int]
    accuracy: float


class EdgePredResponse(BaseModel):
    losses: List[int]
    score: float
    validation_scores: List[float]
    predictions: List[List[int]]
