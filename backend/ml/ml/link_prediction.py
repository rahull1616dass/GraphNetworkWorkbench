import torch
import torch.nn
from tqdm import tqdm
from torch.optim import Adam
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
from torch.nn import BCEWithLogitsLoss
import torch_geometric.transforms as T
from sklearn.metrics import roc_auc_score
from torch_geometric.utils import negative_sampling

from core.typing import MLTask
from core.logging_helpers import timeit


class Net(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels = 128, out_channels=64):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def encode(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        return self.conv2(x, edge_index)

    def decode(self, z, edge_label_index):
        return (z[edge_label_index[0]] * z[edge_label_index[1]]).sum(dim=-1)

    def decode_all(self, z):
        prob_adj = z @ z.t()
        return (prob_adj > 0).nonzero(as_tuple=False).t()


class LinkPredictor:
    def __init__(self, features_number: int, device: torch.device, learning_rate=0.0001):
        self.model = Net(features_number).to(device)
        self.optimizer = Adam(params=self.model.parameters(), lr=learning_rate)
        self.criterion = BCEWithLogitsLoss()

    def train(self, train_data: Data, val_data: Data, epochs: int = 100):
        loss, test_acc = [], []
        for _ in tqdm(range(1, epochs + 1), desc="Training epochs"):
            loss += [self.__train_iter(train_data)]
            test_acc += [self.test(val_data)]
        return loss, test_acc

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
        return loss.cpu().detach().numpy()

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
def predict_edges(data: Data, task: MLTask):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    transform = T.Compose([
        T.NormalizeFeatures(),
        T.ToDevice(device),
        T.RandomLinkSplit(num_val=0.1, num_test=0.1, is_undirected=False, add_negative_train_samples=False)
    ])
    train_data, val_data, test_data = transform(data)
    predictor = LinkPredictor(data.num_features, device, learning_rate=0.001)
    train_loss, val_roc_auc_score = predictor.train(train_data, val_data, epochs=2000)
    test_roc_auc_score = predictor.test(test_data)
    return train_loss, val_roc_auc_score, test_roc_auc_score