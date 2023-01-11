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
    epochs: int
    
    def __post_init__(self): pass
    
    def train(self) -> list[float]:
        self.model = SingleLayerGCN(self.data.x.shape[0], len(np.unique(self.data.y)))
        optimizer: Adam = Adam(self.model.parameters(), lr=0.01, weight_decay=5e-4)

        self.losses: list[float] = []
        for _ in range(self.epochs):
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
    
    
    @staticmethod
    def generate_train_mask(dataset_size: int, train_percentage: float) -> torch.Tensor:
        train_count: int = ceil(train_percentage * dataset_size)
        test_count: int = dataset_size - train_count
        train_mask: torch.Tensor = torch.tensor([True] * train_count + [False] * test_count)

        # Randomly shuffle the train_mask
        return train_mask[torch.randperm(train_mask.size(0))]
  

    @staticmethod
    def from_dataframe(nodes: DataFrame, edges: DataFrame, train_percentage:float = 0.8) -> TorchGeoData:
        y: np.ndarray = nodes["groups"].to_numpy()
        train_mask: torch.Tensor = NodeClassifier.generate_train_mask(y.shape[0], train_percentage)
        
        edge_sources: torch.Tensor = torch.Tensor(edges["source"].to_numpy())
        edge_targets: torch.Tensor = torch.Tensor(edges["target"].to_numpy())
        edges_tensor: torch.Tensor = torch.Tensor(edges.to_numpy())
        return TorchGeoData(
            x=torch.from_numpy(np.eye(nodes.shape[0])).to(torch.float32),
            y=torch.from_numpy(nodes["groups"].to_numpy()),
            edge_index= torch.Tensor(edges.to_numpy()).t().contiguous().to(torch.int64),
            train_mask=train_mask,
            test_mask=~train_mask
        )