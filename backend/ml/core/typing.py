from pydantic import BaseModel, AnyHttpUrl


class MLResult(BaseModel):
    message: str
    losses: list[float]
    predictions: list[int]
    accuracy: float


class MLTask(BaseModel):
    nodes_file_url: AnyHttpUrl
    edges_file_url: AnyHttpUrl
    epochs: int = 100
    train_percentage: float = 0.85
    val_percentage: float = 0.1
