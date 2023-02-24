import os
from typing import Dict, Tuple

import torch
import numpy as np
import pandas as pd
import networkx as nx
from torch_geometric.data import Data
from sklearn.preprocessing import LabelEncoder
from torch_geometric.utils.convert import from_networkx

from core.logging_helpers import timeit
from core.types import MLTask, ClassificationTask


def get_basic_data(data_files: Dict[str, str], class_label_name: str | None = None) -> Tuple[Data, pd.Series]:
    nodes = pd.read_csv(data_files["nodes"], index_col="index")
    edges = pd.read_csv(data_files["edges"])

    graph = nx.DiGraph()
    graph.add_edges_from(list(edges.itertuples(index=False)))

    features = list(set(nodes.columns) - {"name", class_label_name})
    list(map(lambda column_name: nx.set_node_attributes(graph, nodes[column_name].to_dict(), column_name), features))

    target_classes = None
    if class_label_name is not None:
        target_classes = nodes[class_label_name]

    os.remove(data_files["nodes"])
    os.remove(data_files["edges"])

    if len(features) == 0:
        graph_data: Data = from_networkx(graph)
        graph_data.x = torch.from_numpy(np.eye(nodes.shape[0])).to(torch.float32)
    else:
        graph_data: Data = from_networkx(graph, features)
        graph_data.x = graph_data.x.to(torch.float32)

    return graph_data, target_classes


@timeit
def to_class_graph_data(data_files: Dict[str, str], task: ClassificationTask) -> Data:
    graph, class_labels = get_basic_data(data_files, task.target_variable)
    target_classes = torch.tensor(LabelEncoder().fit_transform(class_labels))
    graph.y = target_classes
    return graph


@timeit
def to_pred_graph_data(data_files: Dict[str, str], task: MLTask) -> Data:
    graph, _ = get_basic_data(data_files)
    return graph
