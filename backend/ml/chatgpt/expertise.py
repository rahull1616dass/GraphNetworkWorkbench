from typing import List, Tuple

import openai

from chatgpt import settings
from core.loggers import timeit
from core.requests import MLRequest, ClassificationRequest


def get_basic_arguments(request: MLRequest, losses: List[float], validation_scores: List[float])-> Tuple:
    return (
        len(request.hidden_layer_sizes),
        request.ml_model_type,
        "[" + ", ".join(map(str, request.hidden_layer_sizes)) + "]",
        len(request.x_columns),
        request.train_percentage,
        1 - request.train_percentage,
        request.learning_rate,
        request.epochs,
        "[" + ", ".join(map(str, losses)) + "]",
        "[" + ", ".join(map(str, validation_scores)) + "]"
    )


@timeit
async def get_expert_advice_about_class(
        request: ClassificationRequest, losses: List[float], validation_scores: List[float], test_score: float):
    layers, model, layers_sizes, features, train, val, lr, epochs, losses_str, vals_str = \
        get_basic_arguments(request, losses, validation_scores)
    prompt = f"We have trained a graph neural network for node classification task by using " \
             f"{layers} hidden layers with {layers_sizes} layers sizes with {model} model. After each layer the " \
             f"Relu activation function was used and the output layer has the LogSoftmax activation function. " \
             f"We have used {features} nodes features for it. The data set was divided into train and validation " \
             f"datasets with {train} and {val} frequencies respectively. During the training we have used negative " \
             f"log likelihood loss function and ADAM optimizer with the learning rate {lr}. We trained model during " \
             f"{epochs} epochs. We got such list of losses {losses_str} and such list of validation accuracy scores " \
             f"{vals_str}. The final model accuracy is {test_score}. User can only control type of the model, number " \
             f"of layers and their sizes. Also learning rate, feature, target columns and number of iterations." \
             f"Which advice would you give to such user based on below data how to optimize the model?"
    response = await openai.Completion.acreate(engine=settings.expert_model, prompt=prompt, max_tokens=200)
    return response.choices[0].text


@timeit
async def get_expert_advice_about_pred(
        request: MLRequest, losses: List[float], roc_auc_val_scores: List[float], roc_auc_test_score: float):
    layers, model, layers_sizes, features, train, val, lr, epochs, losses_str, vals_str = \
        get_basic_arguments(request, losses, roc_auc_val_scores)
    prompt = f"We have trained a graph neural network for edge prediction task by using " \
             f"{layers} hidden layers with {layers_sizes} layers sizes with {model} model. We have used " \
             f"{features} nodes features for it. The data set was divided into train and validation datasets with " \
             f"{train} and {val} frequencies respectively. The model described before was using in encoding part. " \
             f"Each iteration we first calculated the encodings, then the negative sampling had place and finally " \
             f"the decoding part was done on both positive and negative edge indexes. The BCEWithLogitsLoss was used " \
             f"as loss function and ADAM with the learning rate {lr} was used as optimizer. We trained model during " \
             f"{epochs} epochs. We got such list of losses {losses_str} and such list of test ROC AUC scores " \
             f"{vals_str}. The final model ROC AUC score is {roc_auc_test_score}. User can only control type of the " \
             f"model, number of layers and their sizes. Also learning rate, feature columns and number of iterations." \
             f"Which advice would you give to such user based on below data how to optimize the model?"
    response = await openai.Completion.acreate(engine=settings.expert_model, prompt=prompt, max_tokens=200)
    return response.choices[0].text
