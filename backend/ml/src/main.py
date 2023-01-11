import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from flask import Flask, request, jsonify
from flask import Response as FlaskResponse
from flask import Request as FlaskRequest
from requests import get as http_get
from requests import Response as RequestsResponse
from fields import Fields
from task_type import TaskType
from pandas import DataFrame, read_csv
from node_classifier import NodeClassifier
import numpy as np
from torch_geometric.data import Data as TorchGeoData

app = Flask(__name__)

def response(status: int, data: dict) -> FlaskResponse:
    data |= {"status": status}
    print(jsonify(data))
    return jsonify(data)


def get_data_frame(file_url: str, create_index: bool = True) -> DataFrame:
    file_response: RequestsResponse = http_get(file_url, stream=True, headers={"Content-Type": "text/csv"})
    print(file_response.status_code)
    if file_response.status_code != 200:
        raise Exception(f"""
                              Error downloading file at {file_url}
                              Reason: {file_response.reason}
                              Text: {file_response.text}
                              """  
                              )
    # Parse the csv in file_response.raw with np.genfromtxt
    return read_csv(file_response.raw)

def download_network_files(request) -> FlaskResponse:
    if request.get(Fields.NODES_FILE_URL.value) is None:
        return response(400, {"error": "No nodes file url found"})
    elif request.get(Fields.EDGES_FILE_URL.value) is None:
        return response(400, {"error": "No edges file url found"})
    
    nodes: DataFrame = get_data_frame(request.get(Fields.NODES_FILE_URL.value), create_index=False)
    edges: DataFrame = get_data_frame(request.get(Fields.EDGES_FILE_URL.value), create_index=False)
    node_classifier = NodeClassifier(NodeClassifier.from_dataframe(nodes, edges), epochs=100)
    losses: list[float] = node_classifier.train()
    predictions: list[int] = node_classifier.predict()
    accuracy: float = node_classifier.evaluate()
    return response(200, {"message": "Classification complete.",
                          "losses": losses,
                          "predictions": predictions,
                          "accuracy": accuracy})

def parse_request(request: FlaskRequest) -> FlaskResponse:
    if request.json is None:
        return response(400, {"error": "No task type found"})

    match request.json.get(Fields.TASK_TYPE.value):
        case TaskType.NODE_CLASSIFICATION.value:
            return download_network_files(request.json)
        case TaskType.GRAPH_CLASSIFICATION.value:
            return response(200, {"message": "Graph prediction"})
    return response(400, {"error": "Invalid task type"})


@app.route("/", methods=["GET", "POST"])
def index() -> FlaskResponse:
    if request.method == "POST":
        try:
            print(request.json)
            return parse_request(request)
        except Exception as e:
            print(e)
            return response(400, {"error": str(e)})
    return response(400, {"error": "Not a POST request"})


if __name__ == "__main__":
    app.run(debug=False)
