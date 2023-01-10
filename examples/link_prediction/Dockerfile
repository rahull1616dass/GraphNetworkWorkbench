FROM jupyter/datascience-notebook:lab-3.5.2

USER root
RUN apt update && apt upgrade -y
RUN apt install build-essential -y
USER $NB_UID

RUN conda install \
    numpy \
    pandas \
    scikit-learn \
    plotly

RUN conda install -c pytorch -c nvidia \
    pytorch  \
    torchvision  \
    torchaudio  \
    pytorch-cuda=11.6

RUN conda install -c conda-forge torch-scatter
RUN conda install -c ostrokach-forge torch-sparse
RUN conda install pyg -c pyg