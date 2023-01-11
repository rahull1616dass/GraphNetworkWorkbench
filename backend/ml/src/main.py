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

app = Flask(__name__)


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


def download_network_files(request: MLRequest) -> FlaskResponse:
    if request.nodes_file_url is None:
        return response(400, {"error": "No nodes file url found"})
    elif request.edges_file_url is None:
        return response(400, {"error": "No edges file url found"})
    
    node_classifier = NodeClassifier(
        NodeClassifier.from_dataframe(
            get_data_frame(request.nodes_file_url, create_index=False ),
            get_data_frame(request.edges_file_url, create_index=False),
            request.train_percentage,
        )
    )

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


def parse_request(request: MLRequest) -> FlaskResponse:
    if request.task_type is None:
        return response(400, {"error": "No task type found"})

    match request.task_type:
        case TaskType.NODE_CLASSIFICATION.value:
            return download_network_files(request)
        case TaskType.GRAPH_CLASSIFICATION.value:
            return response(200, {"message": "Graph prediction"})
    return response(400, {"error": "Invalid task type"})


@app.route("/", methods=["GET", "POST"])
def index() -> FlaskResponse:
    if request.method == "POST":
        try:
            print(request.json)
            request_json_snake_case = {}
            # For each key in the request, convert it to snake case
            for k in request.json.keys():
                request_json_snake_case[convert(k)] = request.json[k]
            return parse_request(MLRequest(**request_json_snake_case))
        except Exception as e:
            print(e)
            return response(400, {"error": str(e)})
    return response(400, {"error": "Not a POST request"})


if __name__ == "__main__":
    app.run(debug=False)
