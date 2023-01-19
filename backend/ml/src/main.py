import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from flask import Flask, request, jsonify
from flask import Response as FlaskResponse
from requests import get as http_get
from requests import Response as RequestsResponse
from task_type import TaskType
from pandas import DataFrame, read_csv
from node_classifier import NodeClassifier
from ml_result import MLResult
from ml_request import MLRequest
from snakecase import convert
import utils
from torch_geometric.data import Data as TorchGeoData
from healthcheck import HealthCheck

app = Flask(__name__)
health = HealthCheck()


def response(status: int, data: dict) -> FlaskResponse:
    data |= {"status": status}
    print(jsonify(data))
    return jsonify(data)


def get_data_frame(file_url: str, create_index: bool = True) -> DataFrame:
    file_response: RequestsResponse = http_get(
        file_url, stream=True, headers={"Content-Type": "text/csv"}
    )
    print(file_response.status_code)
    if file_response.status_code != 200:
        raise Exception(
            f"""
                              Error downloading file at {file_url}
                              Reason: {file_response.reason}
                              Text: {file_response.text}
                              """
        )
    # Parse the csv in file_response.raw with np.genfromtxt
    return read_csv(file_response.raw)


def download_network_files(request: MLRequest) -> dict[str, DataFrame]:
    if request.nodes_file_url is None:
        raise Exception("No nodes file url found")
    elif request.edges_file_url is None:
        raise Exception("No edges file url found")
    
    return {
        'nodes': get_data_frame(request.nodes_file_url, create_index=False ),
        'edges': get_data_frame(request.edges_file_url, create_index=False),
    }


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
    
  
def edge_classification(request: MLRequest, tgData: TorchGeoData) -> FlaskResponse:
    return response(200, {"message": "Edge Classification not implemented yet"})


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
