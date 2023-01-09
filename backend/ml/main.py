import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from flask import Flask, request, jsonify, Response
from fields import Fields
from task_type import TaskType

app = Flask(__name__)

def response(status: int, data: dict = None) -> Response:
    data |= {"status": status}
    print(jsonify(data))
    return jsonify(data)

def parse_request(request) -> Response:
    if request.json is None:
        return response(400, {"error": "No task type found"})
   
    match request.json.get(Fields.TASK_TYPE.value):
        case TaskType.NODE_CLASSIFICATION.value: 
            return response(200, {"message": "Node prediction"})
        case TaskType.GRAPH_CLASSIFICATION.value: 
            return response(200, {"message": "Graph prediction"})
        case _:
            return response(400, {"error": "Invalid task type"})
    
        

@app.route("/", methods=["GET", "POST"])
def index() -> Response:
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