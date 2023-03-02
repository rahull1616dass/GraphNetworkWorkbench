import torch
import mlflow
import torch.nn
from tqdm import tqdm
from torch.optim import Adam
from torch_geometric.data import Data
from torch.nn import BCEWithLogitsLoss
import torch_geometric.transforms as T
from sklearn.metrics import roc_auc_score
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
        for every_step in tqdm(range(1, epochs + 1), desc="Link prediction progress..."):

            loss = self.__train_iter(train_data)
            mlflow.log_metric("loss", loss, every_step)

            val_acc = self.test(val_data)
            mlflow.log_metric("val_roc_auc_score", val_acc, every_step)

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
        return loss.item()

    @torch.no_grad()
    def test(self, test_data: Data):
        self.model.eval()
        z = self.model.encode(test_data.x, test_data.edge_index)
        out = self.model.decode(z, test_data.edge_label_index).view(-1).sigmoid()
        return roc_auc_score(test_data.edge_label.cpu().numpy(), out.cpu().numpy())

    @torch.no_grad()
    def predict(self, data: Data):
        self.model.eval()
        z = self.model.encode(data.x, data.edge_index)
        return self.model.decode_all(z).cpu().numpy()


@timeit
def predict_edges(data: Data, params: MLParams):
    mlflow.set_experiment("Link Prediction")

    with mlflow.start_run() as current_run:
        mlflow.log_params(params.dict())

        device = set_up_device(params.seed)

        transform = T.Compose([
            T.NormalizeFeatures(),
            T.ToDevice(device),
            T.RandomLinkSplit(
                num_val=1 - params.train_percentage,
                is_undirected=False, add_negative_train_samples=False)
        ])
        train_data, val_data, test_data = transform(data)
        predictor = LinkPredictor(data.num_features, device, params)

        predictor.train(train_data, val_data, params.epochs)

        all_loss_metrics = mlflow.tracking.MlflowClient().get_metric_history(current_run.info.run_id, "loss")
        losses = list(map(lambda metric: metric.value, all_loss_metrics))

        all_val_acc = mlflow.tracking.MlflowClient().get_metric_history(current_run.info.run_id, "val_roc_auc_score")
        val_roc_auc_score = list(map(lambda metric: metric.value, all_val_acc))

        test_roc_auc_score = predictor.test(test_data)
        mlflow.log_metric("test_roc_ayc_score", test_roc_auc_score)

        predictions = predictor.predict(test_data)

        mlflow.log_metric("test_roc_auc_curve", test_roc_auc_score)
    return losses, val_roc_auc_score, test_roc_auc_score, predictions.tolist()
