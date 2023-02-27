import torch
import mlflow
import numpy as np
from tqdm import tqdm
from torch.optim import Adam
import torch.nn.functional as F
from dataclasses import dataclass
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
import torch_geometric.transforms as T

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
    data: Data | None = None
    lr: float = 0.01
    
    def train(self, epochs: int = 100):
        self.model = SingleLayerGCN(self.data.x.shape[0], len(np.unique(self.data.y)))
        optimizer: Adam = Adam(self.model.parameters(), lr=self.lr, weight_decay=5e-4)

        for every_epoch in tqdm(range(epochs), desc="Node classification progress..."):
            self.model.train()
            optimizer.zero_grad()
            out = self.model(self.data.x, self.data.edge_index)
            loss = F.nll_loss(out[self.data.train_mask], self.data.y[self.data.train_mask])
            mlflow.log_metric("loss", loss.item(), every_epoch)
            loss.backward()
            optimizer.step()

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
    mlflow.set_experiment("Node Classification")

    with mlflow.start_run() as current_run:
        transformer = T.RandomNodeSplit(split="train_rest", num_test=0.2, num_val=0)
        data_to_use = transformer(data)
        node_classifier = NodeClassifier(data=data_to_use, lr=task.learning_rate)
        node_classifier.train(task.epochs)

        all_accuracy_history = mlflow.tracking.MlflowClient().get_metric_history(current_run.info.run_id, "loss")
        losses = list(map(lambda metric: metric.value, all_accuracy_history))

        predictions: list[int] = node_classifier.predict()

        accuracy: float = node_classifier.evaluate()
        mlflow.log_metric("accuracy", accuracy)

    return losses, predictions, accuracy
    