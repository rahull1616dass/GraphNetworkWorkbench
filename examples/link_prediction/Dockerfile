FROM lsx-harbor.informatik.uni-wuerzburg.de/common-containers/jupyter/pytorch-notebook-gpu:latest

RUN conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.6 -c pytorch -c conda-forge
RUN conda install -c conda-forge sentence-transformers
RUN conda install pyg -c pyg