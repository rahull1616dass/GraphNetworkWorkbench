from typing import List
from itertools import chain

import torch
from torch.nn import Sequential
from more_itertools import windowed
from torch_geometric.nn import SAGEConv, GCNConv, MessagePassing
from torch.nn import ReLU, LogSoftmax

models_mapping = {every_model.__name__: every_model for every_model in (SAGEConv, GCNConv)}


class Net(torch.nn.Module):
    layers: Sequential | None = None

    def __init__(self, model_type: str, features_number: int, hidden_layers_sizes: List[int]):
        super(Net, self).__init__()
        model_to_use: MessagePassing = models_mapping[model_type]

        hidden_layers_params = list(windowed(chain([features_number], hidden_layers_sizes), 2))
        number_of_layers = len(hidden_layers_params)

        layers = []
        for layer_idx, layer_params in enumerate(hidden_layers_params):
            layers.append(model_to_use(*layer_params))
            if layer_idx + 1 == number_of_layers:
                layers.append(ReLU())

        self.layers = Sequential(*layers)


class NodeClassificationNet(Net):
    def __init__(self, *args, **kwargs):
        super(NodeClassificationNet, self).__init__(*args, **kwargs)
        self.layers.append(LogSoftmax(dim=1))

    def forward(self, x, edge_index):
        return self.layers(x, edge_index)


class EdgePredictionNet(Net):
    def encode(self, x, edge_index):
        return self.layers(x, edge_index)

    def decode(self, z, edge_label_index):
        return (z[edge_label_index[0]] * z[edge_label_index[1]]).sum(dim=-1)

    def decode_all(self, z):
        prob_adj = z @ z.t()
        return (prob_adj > 0).nonzero(as_tuple=False).t()
