import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from flask import Flask, request, jsonify
from flask import Response as FlaskResponse
from flask import Request as FlaskRequest
from requests import get as http_get
from requests import Response as RequestsResponse
from fields import Fields
from task_type import TaskType

app = Flask(__name__)


def response(status: int, data: dict) -> FlaskResponse:
    data |= {"status": status}
    print(jsonify(data))
    return jsonify(data)


def get_file(file_url: str) -> RequestsResponse:
    return http_get(file_url, stream=True, headers={"Content-Type": "text/csv"})


def download_network_files(request) -> FlaskResponse:
    if request.get(Fields.NODES_FILE_URL.value) is None:
        return response(400, {"error": "No nodes file url found"})
    elif request.get(Fields.EDGES_FILE_URL.value) is None:
        return response(400, {"error": "No edges file url found"})

    nodesFileResponse: RequestsResponse = get_file(
        request.get(Fields.NODES_FILE_URL.value)
    )
    if nodesFileResponse.status_code != 200:
        return response(
            400,
            {
                "error": f"""
                              Error downloading nodesFile at {request.get(Fields.NODES_FILE_URL.value)}
                              Reason: {nodesFileResponse.reason}
                              """
            },
        )

    edgesFileResponse = get_file(request.get(Fields.EDGES_FILE_URL.value))
    if edgesFileResponse.status_code != 200:
        return response(
            400,
            {
                "error": f"""
                              Error downloading nodesFile at {request.get(Fields.EDGES_FILE_URL.value)}
                              Reason: {edgesFileResponse.reason}
                              """
            },
        )
    
    return FlaskResponse()

def parse_request(request: FlaskRequest) -> FlaskResponse:
    if request.json is None:
        return response(400, {"error": "No task type found"})

    match request.json.get(Fields.TASK_TYPE.value):
        case TaskType.NODE_CLASSIFICATION.value:
            download_network_files(request.json)
            return response(200, {"message": "Node prediction"})
        case TaskType.GRAPH_CLASSIFICATION.value:
            return response(200, {"message": "Graph prediction"})
        case _:
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
    app.run(debug=True)
