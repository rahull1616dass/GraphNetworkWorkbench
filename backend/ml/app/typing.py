from enum import Enum
from dataclasses import dataclass


class TaskType(Enum):
    NODE_CLASSIFICATION = "nodeClassification"
    EDGE_CLASSIFICATION = "edgeClassification"


@dataclass
class MLResult:
    message: str
    losses: list[float]
    predictions: list[int]
    accuracy: float


@dataclass
class MLResult:
    message: str
    losses: list[float]
    predictions: list[int]
    accuracy: float
