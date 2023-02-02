"""REST API"""
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

api = APIRouter()

# TODO: implement node classification and edge prediction endpoints


@api.get("/link_pred")
async def link_prediction():
    return {"msg": "Link pred is not implemented"}


@api.get("/node_class")
async def node_classification():
    return {"msg": "Node classification is not implemented"}


@api.get("/")
def index():
    return RedirectResponse("/docs")
