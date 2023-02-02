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
class MLRequest:
    task_type: TaskType
    nodes_file_url: str
    edges_file_url: str
    epochs: int
    train_percentage: float
