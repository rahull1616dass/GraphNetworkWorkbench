"""REST API"""
from fastapi import APIRouter

api = APIRouter()

# TODO: implement node classification and edge prediction endpoints


@api.get("/link_pred")
async def link_prediction():
    return {"msg": "Link pred is not implemented"}


@api.get("/node_class")
async def node_classification():
    return {"msg": "Node classification is not implemented"}


@api.route("/", methods=["GET", "POST"])
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
