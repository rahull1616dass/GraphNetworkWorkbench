from math import ceil
import torch
from pandas import DataFrame
from torch_geometric.data import Data as TorchGeoData
import numpy as np


def generate_train_mask(dataset_size: int, train_percentage: float) -> torch.Tensor:
    train_count: int = ceil(train_percentage * dataset_size)
    test_count: int = dataset_size - train_count
    train_mask: torch.Tensor = torch.tensor([True] * train_count + [False] * test_count)

    # Randomly shuffle the train_mask
    return train_mask[torch.randperm(train_mask.size(0))]
  

def from_dataframe(nodes: DataFrame, edges: DataFrame, train_percentage:float = 0.8) -> TorchGeoData:
    y: np.ndarray = nodes["groups"].to_numpy()
    train_mask: torch.Tensor = generate_train_mask(y.shape[0], train_percentage)
    
    return TorchGeoData(
        x=torch.from_numpy(np.eye(nodes.shape[0])).to(torch.float32),
        y=torch.from_numpy(nodes["groups"].to_numpy()),
        edge_index= torch.Tensor(edges.to_numpy()).t().contiguous().to(torch.int64),
        train_mask=train_mask,
        test_mask=~train_mask
    )