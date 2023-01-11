from dataclasses import dataclass
from task_type import TaskType

@dataclass
class MLRequest:
    task_type: TaskType
    nodes_file_url: str
    edges_file_url: str
    epochs: int
    train_percentage: float