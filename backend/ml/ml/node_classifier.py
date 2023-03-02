import torch
import mlflow
import numpy as np
from tqdm import tqdm
from torch.optim import Adam
import torch.nn.functional as F
from dataclasses import dataclass
from torch_geometric.data import Data
import torch_geometric.transforms as T

from core.loggers import timeit
from core.params import MLParams
from ml.helpers import set_up_device
from core.nets import NodeClassificationNet


@dataclass
class NodeClassifier:
    data: Data | None = None
    device: torch.device | None = None
    lr: float = 0.01

    def __init__(self, features_number: int, device: torch.device, params: MLParams):
        self.model = NodeClassificationNet(params.ml_model_type, features_number, params.hidden_layer_sizes).to(device)
        self.optimizer = Adam(params=self.model.parameters(), lr=params.learning_rate, weight_decay=5e-4)
    
    def train(self, data: Data, epochs: int = 100):
        optimizer: Adam = Adam(self.model.parameters(), lr=self.lr, weight_decay=5e-4)

        for every_epoch in tqdm(range(epochs), desc="Node classification progress..."):
            self.model.train()
            optimizer.zero_grad()
            out = self.model(data.x, data.edge_index)
            loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
            mlflow.log_metric("loss", loss.item(), every_epoch)
            loss.backward()
            optimizer.step()

    def predict(self, data: Data) -> list[int]:
        self.model.eval()
        _, self.predictions = self.model(data.x, data.edge_index).max(dim=1)
        return self.predictions.tolist()
    

    def evaluate(self, data: Data) -> float:
        correct = self.predictions[data.test_mask].eq(data.y[data.test_mask]).sum().item()
        accuracy = correct / data.test_mask.sum().item()
        print('Accuracy: {:.4f}'.format(accuracy))
        return accuracy


@timeit
def classify_nodes(data: Data, params: MLParams):
    mlflow.set_experiment("Node Classification")

    with mlflow.start_run() as current_run:
        device = set_up_device(params.seed)
        transforms = T.Compose([
            T.RandomNodeSplit(split="train_rest", num_test=0.2, num_val=0),
            T.ToDevice(device)
        ])
        data_to_use: Data = transforms(data)

        node_classifier = NodeClassifier(data_to_use.num_features, device, params)
        node_classifier.train(data_to_use, params.epochs)

        all_accuracy_history = mlflow.tracking.MlflowClient().get_metric_history(current_run.info.run_id, "loss")
        losses = list(map(lambda metric: metric.value, all_accuracy_history))

        predictions: list[int] = node_classifier.predict(data_to_use)

        accuracy: float = node_classifier.evaluate(data_to_use)
        mlflow.log_metric("accuracy", accuracy)

    return losses, predictions, accuracy
    