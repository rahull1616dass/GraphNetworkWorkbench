from typing import List
from itertools import chain

import torch
from more_itertools import windowed
from torch.nn import ReLU, Softmax
from torch_geometric.nn import (
    SAGEConv, GCNConv, GATConv, TAGConv, SGConv, MessagePassing, Sequential)

models_mapping = {every_model.__name__: every_model
                  for every_model in (SAGEConv, GCNConv, GATConv, TAGConv, SGConv)}


def create_layers_sequence(model_type: str, features_number: int, hidden_layers_sizes: List[int]) -> List:
    model_to_use: MessagePassing = models_mapping[model_type]

    """We have hidden_layers_sizes as the array of layer sizes, but for building the model we would need to have 
    the array of par value like (input_data_size, output_data_size)"""
    hidden_layers_params = list(windowed(chain([features_number], hidden_layers_sizes), 2))

    layers = []
    for layer_params in hidden_layers_params:
        layers += [(model_to_use(*layer_params), 'x, edge_index -> x'), ReLU()]
    return layers


class NodeClassificationNet(torch.nn.Module):
    def __init__(self, model_type: str, features_number: int, hidden_layers_sizes: List[int], classes_number: int):
        super().__init__()
        layers = create_layers_sequence(model_type, features_number, hidden_layers_sizes)
        layers += [
            (models_mapping[model_type](hidden_layers_sizes[-1], classes_number), 'x, edge_index -> x'),
            Softmax(dim=1)
        ]
        self.layers = Sequential('x, edge_index', layers)

    def forward(self, x, edge_index):
        return self.layers(x, edge_index)


class EdgePredictionNet(torch.nn.Module):
    def __init__(self, model_type: str, features_number: int, hidden_layers_sizes: List[int]):
        super().__init__()
        layers = create_layers_sequence(model_type, features_number, hidden_layers_sizes)
        self.layers = Sequential('x, edge_index', layers)

    def encode(self, x, edge_index):
        return self.layers(x, edge_index)

    def decode(self, z, edge_label_index):
        return (z[edge_label_index[0]] * z[edge_label_index[1]]).sum(dim=-1)

    def decode_all(self, z):
        prob_adj = z @ z.t()
        return (prob_adj > 0).nonzero(as_tuple=False).t()
