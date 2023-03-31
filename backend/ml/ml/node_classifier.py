from typing import List, Tuple

import torch
import mlflow
from tqdm import tqdm
from torch.optim import Adam
import torch.nn.functional as F
from dataclasses import dataclass
from torch_geometric.data import Data
from sklearn.decomposition import PCA
import torch_geometric.transforms as T
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from core.loggers import timeit
from core.params import MLParams
from ml.helpers import set_up_device
from core.nets import NodeClassificationNet


@dataclass
class NodeClassifier:
    data: Data | None = None
    device: torch.device | None = None
    lr: float = 0.01

    def __init__(self, features_number: int, device: torch.device, params: MLParams, classes_number: int):
        self.model = NodeClassificationNet(params.ml_model_type, features_number, params.hidden_layer_sizes, classes_number).to(device)
        self.optimizer = Adam(params=self.model.parameters(), lr=params.learning_rate, weight_decay=5e-4)

    def __train_iter(self, data: Data):
        self.model.train()
        self.optimizer.zero_grad()

        out = self.model(data.x, data.edge_index)

        loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])

        loss.backward()
        self.optimizer.step()
        return round(loss.item(), 4)
    
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

    def __get_data_to_compare(self, data: Data):
        self.model.eval()
        out = self.model(data.x, data.edge_index)
        y_true = data.y[data.test_mask].cpu().numpy()
        y_pred_prob = out.cpu().numpy()
        y_predicted_class = torch.argmax(out[data.test_mask], dim=1).unsqueeze(1).cpu().numpy()
        return y_true, y_predicted_class, y_pred_prob

    def test(self, data: Data) -> float:
        y_true, y_predicted, _ = self.__get_data_to_compare(data)
        return round(accuracy_score(y_true, y_predicted), 4)

    def get_all_metrics(self, data: Data) -> Tuple:
        y_true, y_predicted_class, y_pred_prob = self.__get_data_to_compare(data)

        accuracy = round(accuracy_score(y_true, y_predicted_class), 4)
        mlflow.log_metric("accuracy", accuracy)

        precision = round(precision_score(y_true, y_predicted_class, average="macro"), 4)
        mlflow.log_metric("precision", precision)

        recall = round(recall_score(y_true, y_predicted_class, average="macro"), 4)
        mlflow.log_metric("recall", recall)

        f1 = round(f1_score(y_true, y_predicted_class, average="macro"), 4)
        mlflow.log_metric("f1", f1)

        roc_auc = round(roc_auc_score(y_true, y_pred_prob, multi_class="ovr", average="macro"), 4)
        mlflow.log_metric("ROC AUC", roc_auc)

        return accuracy, precision, recall, f1, roc_auc

    def predict(self, data: Data) -> List:
        self.model.eval()
        out = self.model(data.x, data.edge_index)
        predicted_classes = torch.argmax(out[data.test_mask], dim=1)
        return predicted_classes.detach().cpu().numpy().tolist()

    def get_2d_node_embeddings(self, data: Data):
        self.model.eval()
        embeddings = self.model.non_act_layers(data.x, data.edge_index)
        embeddings_2d = PCA(n_components=2).fit_transform(embeddings.detach().cpu().numpy())
        return embeddings_2d


@timeit
def classify_nodes(data: Data, params: MLParams, encoder: LabelEncoder):
    mlflow.set_experiment("Node Classification")

    with mlflow.start_run():
        mlflow.log_params(params.dict())

        device = set_up_device(params.seed)

        if params.train_percentage is None:
            transforms = T.ToDevice(device)
            used_for_training = torch.sum(data.train_mask).item()
            all_nodes = torch.numel(data.train_mask)
            train_percentage = round(used_for_training / all_nodes, 4)
        else:
            transforms = T.Compose([
                T.RandomNodeSplit(split="train_rest", num_test=1-params.train_percentage, num_val=0),
                T.ToDevice(device)
            ])
            train_percentage = params.train_percentage
        data_to_use: Data = transforms(data)

        node_classifier = NodeClassifier(data_to_use.num_features, device, params, len(encoder.classes_))
        losses, val_acc_scores = node_classifier.train(data_to_use, params.epochs)

        accuracy, precision, recall, f1, roc_auc = node_classifier.get_all_metrics(data_to_use)

        predictions: List = encoder.inverse_transform(node_classifier.predict(data_to_use))
        test_node_indices = torch.unique(data_to_use.edge_index)[data_to_use.test_mask].cpu().numpy().tolist()
        node_idx_pred_class_pairs = {node_idx: str(pred_class)
                                     for node_idx, pred_class in zip(test_node_indices, predictions)}

        embeddings = node_classifier.get_2d_node_embeddings(data_to_use)
        embeddings_dict = {idx: (round(float(x_y_pair[0]), 4), round(float(x_y_pair[1]), 4))
                           for idx, x_y_pair in enumerate(embeddings)}

    return (
        losses,
        val_acc_scores,
        accuracy,
        precision,
        recall,
        f1,
        roc_auc,
        node_idx_pred_class_pairs,
        embeddings_dict,
        train_percentage
    )
    