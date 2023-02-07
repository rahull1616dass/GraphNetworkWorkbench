"""Celery tasks"""
from celery import shared_task

from task_manager import celery_instance
from ml.link_prediction import predict_edges
from ml.node_classifier import classify_nodes
from preprocessing.parsing import from_dataframe
from preprocessing.loading import download_network_files

@shared_task
def download_task(*args, **kwargs):
    return download_network_files(*args, **kwargs)


@shared_task
def convert_task(*args, **kwargs):
    return from_dataframe(*args, **kwargs)


@shared_task
def edge_prediction_task(*args, **kwargs):
    return predict_edges(*args, **kwargs)


@shared_task
def node_classification_task(*args, **kwargs):
    return classify_nodes(*args, **kwargs)
