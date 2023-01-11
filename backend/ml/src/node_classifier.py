from models.single_layer_gcn import SingleLayerGCN
import torch
import torch.nn.functional as F
from torch.optim import Adam
from torch_geometric.data import Data as TorchGeoData
from dataclasses import dataclass
import numpy as np
from pandas import DataFrame
from math import ceil
@dataclass
class NodeClassifier:
    data: TorchGeoData
    
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
    