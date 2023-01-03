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
The environment with the modules it uses can be exported via:
```
conda env export --no-builds > environment.yml
```

To create the environment from the exported file, run:
```
conda env create -f environment.yml
```