import torch.nn
from tqdm import tqdm
from torch.optim import Adam
from torch_geometric.data import Data
from torch.nn import BCEWithLogitsLoss
from torch_geometric.utils import negative_sampling
from sklearn.metrics import accuracy_score, roc_auc_score

from .models.link_pred import Net


class LinkPredictor:
    def __init__(self, features_number: int, device: torch.device, learning_rate=0.0001):
        self.model = Net(features_number).to(device)
        self.optimizer = Adam(params=self.model.parameters(), lr=learning_rate)
        self.criterion = BCEWithLogitsLoss()

    def train(self, train_data: Data, val_data: Data, epochs: int = 100):
        loss, train_acc, test_acc = [], [], []
        for _ in tqdm(range(1, epochs + 1), desc="Training epochs"):
            loss += [self.__train_iter(train_data)]
            train_acc += [self.test(train_data)]
            test_acc += [self.test(val_data)]
        return loss, train_acc, test_acc

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
        return loss

    @torch.no_grad()
    def test(self, test_data: Data):
        self.model.eval()
        z = self.model.encode(test_data.x, test_data.edge_index)
        out = self.model.decode(z, test_data.edge_label_index).view(-1).sigmoid()
        return roc_auc_score(test_data.edge_label.cpu().numpy(), out.cpu().numpy())


