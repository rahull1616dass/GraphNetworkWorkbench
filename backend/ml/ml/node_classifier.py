from typing import List

import torch
import mlflow
from tqdm import tqdm
from torch.optim import Adam
import torch.nn.functional as F
from dataclasses import dataclass
from torch_geometric.data import Data
import torch_geometric.transforms as T
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

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

    def __train_iter(self, data: Data):
        self.model.train()
        self.optimizer.zero_grad()

        out = self.model.layers(data.x, data.edge_index)

        loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])

        loss.backward()
        self.optimizer.step()
        return loss.item()
    
    def train(self, data: Data, epochs: int = 100):

        losses, val_acc_scores = [], []
        for every_epoch in tqdm(range(epochs), desc="Node classification progress..."):
            loss = self.__train_iter(data)
            mlflow.log_metric("loss", loss, every_epoch)
            losses.append(loss)

            val_acc_score = self.test(data)
            mlflow.log_metric("validation accuracy score", val_acc_score, every_epoch)
            val_acc_scores.append(val_acc_score)
        return losses, val_acc_scores

    def test(self, data: Data) -> float:
        self.model.eval()
        out = self.model.layers(data.x, data.edge_index)
        true = data.y[data.test_mask]
        predicted = out[data.test_mask]
        return accuracy_score(data.y[data.test_mask], out[data.test_mask])

    def predict(self, data: Data) -> List:
        self.model.eval()
        result = self.model.layers(data.x[data.test_mask], data.edge_index[data.test_mask])
        return self.model(data.x[data.test_mask], data.edge_index[data.test_mask])


@timeit
def classify_nodes(data: Data, params: MLParams, encoder: LabelEncoder):
    mlflow.set_experiment("Node Classification")

    with mlflow.start_run():
        device = set_up_device(params.seed)
        transforms = T.Compose([
            T.RandomNodeSplit(split="train_rest", num_test=0.2, num_val=0),
            T.ToDevice(device)
        ])
        data_to_use: Data = transforms(data)

        node_classifier = NodeClassifier(data_to_use.num_features, device, params)
        losses, val_acc_scores = node_classifier.train(data_to_use, params.epochs)

        final_accuracy: float = node_classifier.test(data_to_use)
        mlflow.log_metric("accuracy", final_accuracy)

        predictions: List = encoder.inverse_transform(node_classifier.predict(data_to_use))

    return losses, val_acc_scores, final_accuracy, predictions
    