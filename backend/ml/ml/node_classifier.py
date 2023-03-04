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

        out = self.model(data.x, data.edge_index)

        loss = F.nll_loss(out, data.y)

        loss.backward()
        self.optimizer.step()
        return loss.item()
    
    def train(self, data: Data, epochs: int = 100):

        losses, val_acc_scores = [], []
        for every_epoch in tqdm(range(epochs), desc="Node classification progress..."):
            loss = self.__train_iter(data[data.train_mask])
            mlflow.log_metric("loss", loss, every_epoch)
            losses.append(loss)

            val_acc_score = self.test(data[data.test_mask])
            mlflow.log_metric("validation accuracy score", val_acc_score, every_epoch)
            val_acc_scores.append(val_acc_score)
        return losses, val_acc_scores

    def test(self, data: Data) -> float:
        self.model.eval()
        out = self.model(data.x, data.edge_index)
        return accuracy_score(data.y, out)

    def predict(self, data: Data) -> List:
        self.model.eval()
        return self.model(data.x, data.edge_index).tolist()


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

        final_accuracy: float = node_classifier.test(data_to_use[data_to_use.test_mask])
        mlflow.log_metric("accuracy", final_accuracy)

        predictions: List = encoder.inverse_transform(node_classifier.predict(data_to_use[data_to_use.test_mask]))

    return losses, val_acc_scores, final_accuracy, predictions
    