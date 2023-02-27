import os
from typing import Dict

import torch
import numpy as np
import pandas as pd
import networkx as nx
from torch_geometric.data import Data
from sklearn.preprocessing import LabelEncoder
from torch_geometric.utils.convert import from_networkx

from core.logging_helpers import timeit
from core.types import MLTask, ClassificationTask


def get_basic_data(data_files: Dict[str, str], task: MLTask) -> Data:
    nodes = pd.read_csv(data_files["nodes"])
    edges = pd.read_csv(data_files["edges"])

    graph = nx.Graph()
    graph.add_edges_from(list(edges.itertuples(index=False)))

    list(
        map(
            lambda column_name: nx.set_node_attributes(graph, nodes[column_name].to_dict(), column_name),
            task.x_columns
        )
    )

    os.remove(data_files["nodes"])
    os.remove(data_files["edges"])

    if len(task.x_columns) == 0:
        graph_data: Data = from_networkx(graph)
        graph_data.x = torch.from_numpy(np.eye(nodes.shape[0])).to(torch.float32)
    else:
        graph_data: Data = from_networkx(graph, task.x_columns)
        graph_data.x = graph_data.x.to(torch.float32)

    if isinstance(task, ClassificationTask):
        task: ClassificationTask = task
        graph_data.y = torch.tensor(LabelEncoder().fit_transform(nodes[task.y_column]))

    return graph_data


@timeit
def to_class_graph_data(data_files: Dict[str, str], task: ClassificationTask) -> Data:
    return get_basic_data(data_files, task)


@timeit
def to_pred_graph_data(data_files: Dict[str, str], task: MLTask) -> Data:
    return get_basic_data(data_files, task)
