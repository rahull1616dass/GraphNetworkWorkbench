import os

import torch
from snakecase import convert
from healthcheck import HealthCheck
from requests import get as http_get
import torch_geometric.transforms as T
from pandas import DataFrame, read_csv
from flask import Flask, request, jsonify
from flask import Response as FlaskResponse
from requests import Response as RequestsResponse
from torch_geometric.data import Data as TorchGeoData

import utils
from task_type import TaskType
from ml_result import MLResult
from ml_request import MLRequest
from node_classifier import NodeClassifier
from models.link_prediction import LinkPredictor


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

app = Flask(__name__)
health = HealthCheck()


def response(status: int, data: dict) -> FlaskResponse:
    data |= {"status": status}
    print(jsonify(data))
    return jsonify(data)


def node_classification(request: MLRequest, tgData: TorchGeoData) -> FlaskResponse:
    node_classifier = NodeClassifier(tgData)
    
    # Need to set them first before creating the MLResult dataclass
    # since train,predict,evaluate has to happen in a consecutive manner
    losses: list[float] = node_classifier.train(request.epochs)
    predictions: list[int] = node_classifier.predict()
    accuracy: float = node_classifier.evaluate()

    return response(
        200,
        MLResult(
            message="Training complete",
            losses=losses,
            predictions=predictions,
            accuracy=accuracy,
        ).__dict__,
    )
    
  
def edge_prediction(data: TorchGeoData):
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


@app.route("/", methods=["GET", "POST"])
def index() -> FlaskResponse:
    if request.method == "POST":
        try:
            print(request.json)
            request_json_snake_case = {}
            # For each key in the request, convert it to snake case
            for k in request.json.keys(): # type: ignore
                request_json_snake_case[convert(k)] = request.json[k] # type: ignore
            return parse_request(MLRequest(**request_json_snake_case))
        except Exception as e:
            print(e)
            return response(400, {"error": str(e)})
    return response(400, {"error": "Not a POST request"})


app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())


if __name__ == "__main__":
    app.run(debug=False)
