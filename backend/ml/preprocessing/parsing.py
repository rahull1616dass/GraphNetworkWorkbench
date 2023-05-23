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


# TODO: If this project will be further developed this parsing file has to be changed: saving graphs in two csv files
#  makes the task of parsing different(directed/undirected, weighted/unweighted graphs) graphs really like reinventing
#  the wheel. It is better to keep supporting .graphml files because networkx exist for both python and JS and can
#  parse it without writing any additional code.


def generate_custom_masks(nodes_df: pd.DataFrame):
    train_mask = torch.tensor((nodes_df["is_train"]==1).values)
    test_mask = ~train_mask
    val_mask = torch.zeros_like(train_mask, dtype=torch.bool)
    return train_mask, val_mask, test_mask


def get_basic_data(data_files: Dict[str, str], params: MLParams, label_encoder: LabelEncoder = None) -> Data:
    nodes = pd.read_csv(data_files["nodes"])
    edges = pd.read_csv(data_files["edges"])

    # in case if index of nodes are not same as just numeric sequence
    nodes = nodes.set_index("index", drop=False)

    graph = nx.Graph()

    graph.add_nodes_from(nodes["index"].to_numpy())

    graph.add_edges_from(list(edges[["source", "target"]].itertuples(index=False)))

    for every_column in params.x_columns:
        if pd.api.types.is_string_dtype(nodes[every_column]):
            nodes[every_column] = LabelEncoder().fit_transform(nodes[every_column].values)
        nx.set_node_attributes(graph, nodes[every_column].to_dict(), every_column)

    os.remove(data_files["nodes"])
    os.remove(data_files["edges"])

    # check if features exist
    if len(params.x_columns) == 0:
        graph_data: Data = from_networkx(graph)
        graph_data.x = torch.from_numpy(np.eye(nodes.shape[0])).to(torch.float32)
    else:
        graph_data: Data = from_networkx(graph, params.x_columns)
        graph_data.x = torch.cat(
            (graph_data.x.to(torch.float32), torch.from_numpy(np.eye(nodes.shape[0])).to(torch.float32)),
            dim=1
        )

    # Check if it is classification task
    if isinstance(params, ClassificationParams):
        params: ClassificationParams = params
        graph_data.y = torch.tensor(label_encoder.fit_transform(nodes[params.y_column]))

        # check the custom split only in classification task
        if params.use_custom_split:
            train_mask, val_mask, test_mask = generate_custom_masks(nodes)
            graph_data.train_mask = train_mask
            graph_data.val_mask = val_mask
            graph_data.test_mask = test_mask

    return graph_data


@timeit
def to_class_graph_data(data_files: Dict[str, str], params: ClassificationParams, encoder: LabelEncoder) -> Data:
    return get_basic_data(data_files, params, encoder)


@timeit
def to_pred_graph_data(data_files: Dict[str, str], params: MLParams) -> Data:
    return get_basic_data(data_files, params)
