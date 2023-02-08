from typing import List
from pydantic import BaseModel, AnyHttpUrl


class NodeClassResponse(BaseModel):
    losses: List[float]
    predictions: List[int]
    accuracy: float


class EdgePredResponse(BaseModel):
    losses: List[int]
    score: float
    validation_scores: List[float]
    predictions: List[List[int]]


class MLTask(BaseModel):
    nodes_file_url: AnyHttpUrl
    edges_file_url: AnyHttpUrl
    epochs: int = 100
    train_percentage: float = 0.85
    val_percentage: float = 0.1
