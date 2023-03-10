"""Celery tasks"""
import asyncio

from celery import shared_task

from task_manager import celery_instance
from ml.link_prediction import predict_edges
from ml.node_classifier import classify_nodes
from preprocessing.loading import download_network_files
from preprocessing.parsing import to_class_graph_data, to_pred_graph_data
from chatgpt.expertise import get_expert_advice_about_class, get_expert_advice_about_pred


@shared_task
def download_task(*args, **kwargs):
    return asyncio.run(download_network_files(*args, **kwargs))


@shared_task
def convert_for_pred_task(*args, **kwargs):
    return to_pred_graph_data(*args, **kwargs)


@shared_task
def convert_for_class_task(*args, **kwargs):
    return to_class_graph_data(*args, **kwargs)


@shared_task
def edge_prediction_task(*args, **kwargs):
    return predict_edges(*args, **kwargs)


@shared_task
def node_classification_task(*args, **kwargs):
    return classify_nodes(*args, **kwargs)


@shared_task
def get_class_expert_opinion_task(*args, **kwargs):
    return asyncio.run(get_expert_advice_about_class(*args, **kwargs))


@shared_task
def get_pred_expert_opinion_task(*args, **kwargs):
    return asyncio.run(get_expert_advice_about_pred(*args, **kwargs))
