from typing import List, Dict

from core.camel import CamelModel


class MLResponse(CamelModel):
    losses: List[float]
    val_scores: List[float]
    accuracy: float
    precision: float
    recall: float
    f1: float
    auc: float
    expert_opinion: str
    embeddings: Dict
    predictions: Dict
