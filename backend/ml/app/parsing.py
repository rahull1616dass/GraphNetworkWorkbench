from flask import Response as FlaskResponse
from torch_geometric.data import Data as TorchGeoData

from app.typing import MLRequest



def parse_request(request: MLRequest) -> FlaskResponse:
    if request.task_type is None:
        return response(400, {"error": "No task type found"})

    files: dict[str, DataFrame] = download_network_files(request)
    tgData: TorchGeoData = utils.from_dataframe(files['nodes'], files['edges'])
    if request.task_type == TaskType.NODE_CLASSIFICATION:
        return node_classification(request, tgData)
    elif request.task_type == TaskType.EDGE_CLASSIFICATION:
        return node_classification(request, tgData)
    return response(400, {"error": "Invalid task type"})


def generate_train_mask(dataset_size: int, train_percentage: float) -> torch.Tensor:
    train_count: int = ceil(train_percentage * dataset_size)
    test_count: int = dataset_size - train_count
    train_mask: torch.Tensor = torch.tensor([True] * train_count + [False] * test_count)

    # Randomly shuffle the train_mask
    return train_mask[torch.randperm(train_mask.size(0))]


def from_dataframe(nodes: DataFrame, edges: DataFrame, train_percentage: float = 0.8) -> TorchGeoData:
    y: np.ndarray = nodes["groups"].to_numpy()
    train_mask: torch.Tensor = generate_train_mask(y.shape[0], train_percentage)

    return TorchGeoData(
        x=torch.from_numpy(np.eye(nodes.shape[0])).to(torch.float32),
        y=torch.from_numpy(nodes["groups"].to_numpy()),
        edge_index=torch.Tensor(edges.to_numpy()).t().contiguous().to(torch.int64),
        train_mask=train_mask,
        test_mask=~train_mask
    )