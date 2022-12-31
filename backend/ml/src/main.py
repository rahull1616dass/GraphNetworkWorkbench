import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from flask import Flask, request, jsonify
from fields import Fields
from task_type import TaskType

app = Flask(__name__)

def response(status: int, data: dict = None) -> dict:
    return jsonify( {"status": status, **data})

def parse_request(request) -> dict:
    if request.form() is None:
        return response(400, {"error": "No task type found"})
    match request.form().get(Fields.TASK_TYPE):
        case TaskType.NODE_PREDICTION: 
            return response(200, {"message": "Node prediction"})
        case TaskType.GRAPH_PREDICTION: 
            return response(200, {"message": "Graph prediction"})


@app.route("/", methods=["GET", "POST"])
def index() -> dict:
    if request.method == "POST":
        try:
            return parse_request(request)
        except Exception as e:
            return response(400, {"error": str(e)})
    return response(400, {"error": "Not a POST request"})


if __name__ == "__main__":
    app.run(debug=True)