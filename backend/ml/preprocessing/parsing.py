from typing import Dict

import pandas as pd
import networkx as nx
from torch_geometric.data import Data
from torch_geometric.utils.convert import from_networkx

from core.types import MLTask
from core.logging_helpers import timeit


@timeit
def to_graph_data(data_files: Dict[str, str], task: MLTask) -> Data:
    nodes = pd.read_csv(data_files["nodes"], index_col="index")
    edges = pd.read_csv(data_files["edges"])

    graph = nx.DiGraph()
    graph.add_edges_from(list(edges.itertuples(index=False)))

    features = list(set(nodes.columns) - {"name"})
    list(map(lambda column_name: nx.set_node_attributes(graph, nodes[column_name].to_dict(), column_name), features))

    return from_networkx(graph, features)
