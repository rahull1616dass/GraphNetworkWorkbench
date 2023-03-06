from typing import List

from pydantic import BaseModel


class NodeClassResponse(BaseModel):
    losses: List[float]
    predictions: List[int]
    accuracy: float


class EdgePredResponse(BaseModel):
    losses: List[int]
    score: float
    validation_scores: List[float]
    predictions: List[List[int]]
