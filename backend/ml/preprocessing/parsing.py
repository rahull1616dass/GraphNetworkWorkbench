import os
from typing import Dict

import torch
import numpy as np
import pandas as pd
import networkx as nx
from torch_geometric.data import Data
from sklearn.preprocessing import LabelEncoder
from torch_geometric.utils.convert import from_networkx

from core.loggers import timeit
from core.params import MLParams, ClassificationParams


# TODO: If this project will be further developed this parsing file has to be changed: saving graphs in two csv files makes the task of parsing different(directed/undirected, weighted/unweighted graphs) graphs really like reinventing the wheel. It is better to keep supporting .graphml files because networkx exist for both python and JS and can parse it without writing any additional code.
def get_basic_data(data_files: Dict[str, str], params: MLParams, label_encoder: LabelEncoder = None) -> Data:
    nodes = pd.read_csv(data_files["nodes"])
    edges = pd.read_csv(data_files["edges"])

    graph = nx.Graph()

    if len(edges.columns) == 2:
        graph.add_edges_from(list(edges.itertuples(index=False)))
    else:
        graph.add_weighted_edges_from(list(edges.itertuples(index=False)))

    for every_column in params.x_columns:
        if pd.api.types.is_string_dtype(nodes[every_column]):
            nodes[every_column] = LabelEncoder().fit_transform(nodes[every_column].values)
        nx.set_node_attributes(graph, nodes[every_column].to_dict(), every_column)

    os.remove(data_files["nodes"])
    os.remove(data_files["edges"])

    if len(params.x_columns) == 0:
        graph_data: Data = from_networkx(graph)
        graph_data.x = torch.from_numpy(np.eye(nodes.shape[0])).to(torch.float32)
    else:
        graph_data: Data = from_networkx(graph, params.x_columns)
        graph_data.x = graph_data.x.to(torch.float32)

    if isinstance(params, ClassificationParams):
        params: ClassificationParams = params
        graph_data.y = torch.tensor(label_encoder.fit_transform(nodes[params.y_column]))

    return graph_data


@timeit
def to_class_graph_data(data_files: Dict[str, str], params: ClassificationParams, encoder: LabelEncoder) -> Data:
    return get_basic_data(data_files, params, encoder)


@timeit
def to_pred_graph_data(data_files: Dict[str, str], params: MLParams) -> Data:
    return get_basic_data(data_files, params)
