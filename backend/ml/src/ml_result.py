from dataclasses import dataclass

@dataclass
class MLResult:
    message: str
    losses: list[float]
    predictions: list[int]
    accuracy: float