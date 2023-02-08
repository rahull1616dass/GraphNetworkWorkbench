import torch
import numpy as np
from torch.optim import Adam
import torch.nn.functional as F
from dataclasses import dataclass
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv

from core.types import MLTask
from core.logging_helpers import timeit


class SingleLayerGCN(torch.nn.Module):
    def __init__(self, in_channels, out_channels):
        super(SingleLayerGCN, self).__init__()
        self.conv1 = GCNConv(in_channels, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        return F.log_softmax(x, dim=1)

@dataclass
class NodeClassifier:
    data: Data
    
    def __post_init__(self): pass
    
    def train(self, epochs: int = 100) -> list[float]:
        self.model = SingleLayerGCN(self.data.x.shape[0], len(np.unique(self.data.y)))
        optimizer: Adam = Adam(self.model.parameters(), lr=0.01, weight_decay=5e-4)

        self.losses: list[float] = []
        for _ in range(epochs):
            self.model.train()
            optimizer.zero_grad()
            out = self.model(self.data.x, self.data.edge_index)
            loss: torch.Tensor = F.nll_loss(out[self.data.train_mask], self.data.y[self.data.train_mask])
            self.losses.append(loss.item())
            loss.backward()
            optimizer.step()
        return self.losses

    def predict(self) -> list[int]:
        self.model.eval()
        _, self.predictions = self.model(self.data.x, self.data.edge_index).max(dim=1)
        return self.predictions.tolist()
    

    def evaluate(self) -> float:
        correct = self.predictions[self.data.test_mask].eq(self.data.y[self.data.test_mask]).sum().item()
        accuracy = correct / self.data.test_mask.sum().item()
        print('Accuracy: {:.4f}'.format(accuracy))
        return accuracy


@timeit
def classify_nodes(data: Data, task: MLTask):
    node_classifier = NodeClassifier(data)

    # Need to set them first before creating the MLResult dataclass
    # since train,predict,evaluate has to happen in a consecutive manner
    losses: list[float] = node_classifier.train(task.epochs)
    predictions: list[int] = node_classifier.predict()
    accuracy: float = node_classifier.evaluate()

    return losses, predictions, accuracy
    