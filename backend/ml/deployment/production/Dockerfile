FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip setuptools
COPY ./requirements.yaml ./requirements.yaml
RUN conda env update --file ./requirements.yaml