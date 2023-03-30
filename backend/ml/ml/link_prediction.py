from typing import Callable

import torch
import mlflow
import torch.nn
from tqdm import tqdm
from torch.optim import Adam
from torch_geometric.data import Data
from sklearn.decomposition import PCA
from torch.nn import BCEWithLogitsLoss
import torch_geometric.transforms as T
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score
from torch_geometric.utils import negative_sampling

from core.loggers import timeit
from core.params import MLParams
from ml.helpers import set_up_device
from core.nets import EdgePredictionNet


class LinkPredictor:
    def __init__(self, features_number: int, device: torch.device, params: MLParams):
        self.model = EdgePredictionNet(params.ml_model_type, features_number, params.hidden_layer_sizes).to(device)
        self.optimizer = Adam(params=self.model.parameters(), lr=params.learning_rate)
        self.criterion = BCEWithLogitsLoss()

    def train(self, train_data: Data, val_data: Data, epochs: int = 100):
        losses, val_roc_auc_scores = [], []
        for every_step in tqdm(range(1, epochs + 1), desc="Link prediction progress..."):

            loss = self.__train_iter(train_data)
            losses += [loss]
            mlflow.log_metric("loss", loss, every_step)

            val_acc = self.test(val_data)
            val_roc_auc_scores += [val_acc]
            mlflow.log_metric("val_roc_auc_score", val_acc, every_step)

        return losses, val_roc_auc_scores

    def __train_iter(self, train_data: Data):
        self.model.train()
        self.optimizer.zero_grad()
        z = self.model.encode(train_data.x, train_data.edge_index)

        # We perform a new round of negative sampling for every training epoch:
        neg_edge_index = negative_sampling(
            edge_index=train_data.edge_index, num_nodes=train_data.num_nodes,
            num_neg_samples=train_data.edge_label_index.size(1), method='sparse')

        edge_label_index = torch.cat(
            [train_data.edge_label_index, neg_edge_index],
            dim=-1,
        )
        edge_label = torch.cat([
            train_data.edge_label,
            train_data.edge_label.new_zeros(neg_edge_index.size(1))
        ], dim=0)

        out = self.model.decode(z, edge_label_index).view(-1)
        loss = self.criterion(out, edge_label)
        loss.backward()
        self.optimizer.step()
        return round(loss.item(), 4)

    def __get_y_pred(self, data: Data):
        self.model.eval()
        z = self.model.encode(data.x, data.edge_index)
        out = self.model.decode(z, data.edge_label_index).view(-1).sigmoid()
        y_true = data.edge_label.cpu().numpy()
        return y_true, out.detach().cpu()

    @torch.no_grad()
    def test(self, data: Data):
        y_true, out = self.__get_y_pred(data)
        y_pred = out.numpy()
        return round(roc_auc_score(y_true, y_pred), 4)

    def get_all_metrics(self, data: Data):
        y_true, out = self.__get_y_pred(data)
        y_bin_pred = torch.where(out >= 0.5, 1.0, 0.0).numpy()
        y_cont_pred = out.numpy()

        accuracy = round(accuracy_score(y_true, y_bin_pred), 4)
        mlflow.log_metric("accuracy", accuracy)

        precision = round(precision_score(y_true, y_bin_pred), 4)
        mlflow.log_metric("precision", precision)

        recall = round(recall_score(y_true, y_bin_pred), 4)
        mlflow.log_metric("recall", recall)

        f1 = round(f1_score(y_true, y_bin_pred), 4)
        mlflow.log_metric("f1", f1)

        roc_auc = round(roc_auc_score(y_true, y_cont_pred), 4)
        mlflow.log_metric("ROC AUC", roc_auc)

        return accuracy, precision, recall, f1, roc_auc

    @torch.no_grad()
    def predict(self, data: Data):
        self.model.eval()
        z = self.model.encode(data.x, data.edge_index)
        return self.model.decode_all(z).cpu().numpy()

    @torch.no_grad()
    def get_2d_node_embeddings(self, data: Data):
        self.model.eval()
        embeddings = self.model.non_act_layers(data.x, data.edge_index)
        embeddings_2d = PCA(n_components=2).fit_transform(embeddings.detach().cpu().numpy())
        return embeddings_2d


@timeit
def predict_edges(data: Data, params: MLParams):
    mlflow.set_experiment("Link Prediction")

    with mlflow.start_run():
        mlflow.log_params(params.dict())

        device = set_up_device(params.seed)

        common_transform = T.Compose([
            T.NormalizeFeatures(),
            T.ToDevice(device)
        ])
        data_to_use = common_transform(data)

        split_transform = T.RandomLinkSplit(
                num_val=0,
                num_test=1 - params.train_percentage,
                is_undirected=False, add_negative_train_samples=False)
        train_data, _, test_data = split_transform(data_to_use)

        predictor = LinkPredictor(data.num_features, device, params)

        losses, val_roc_auc_scores = predictor.train(train_data, test_data, params.epochs)

        accuracy, precision, recall, f1, roc_auc = predictor.get_all_metrics(test_data)

        predictions = predictor.predict(test_data)

        edge_index = test_data.edge_index.cpu().numpy().tolist()
        real_pairs = [(source, target) for source, target in zip(edge_index[0], edge_index[1])]
        predicted_pairs = {f"{source}-{target}": (source, target) in real_pairs
                           for source, target in zip(predictions[0], predictions[1])}

        embeddings = predictor.get_2d_node_embeddings(data_to_use)

    return (
        losses,
        val_roc_auc_scores,
        accuracy,
        precision,
        recall,
        f1,
        roc_auc,
        predicted_pairs,
        embeddings.tolist()
    )
