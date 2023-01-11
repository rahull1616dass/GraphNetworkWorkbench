## Interactive Graph Learning Workbench

### The task:

An interactive user interface/webpage with following minimal functionalities:

    - Upload data
    - Fetch data from online repos : e.g. OGB, netzschleuder, PyTorch datasets
    - Visualise/plot networks+data 
    - Select GNN models (GCN,DeepWalk,GIN…) + ML task i.e. node classification / link prediction 
    - Train/test  GNN 
    - Visualise learned representations
    - Compare predictions for different models/hyperparameter values
    - Interactive manipulation of node or edge features

# Working with Anaconda

The backend with all the PyTorch/PyTorch Geometric modules installed is available as a conda environment out of the box. To use it, run:
```bash
conda env create --file backend/backend_env.yml
```

The environment with the modules it uses can be exported via:
```bash
conda env export --no-builds > environment.yml
```

To create the environment from the exported file, run:
```bash
conda env create -f environment.yml
```