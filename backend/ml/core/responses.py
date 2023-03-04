from typing import List

from pydantic import BaseModel


class NodeClassResponse(BaseModel):
    losses: List[float]
    predictions: List
    accuracy: float
    expert_opinion: str


class EdgePredResponse(BaseModel):
    losses: List[int]
    score: float
    validation_scores: List[float]
    predictions: List
    expert_opinion: str
