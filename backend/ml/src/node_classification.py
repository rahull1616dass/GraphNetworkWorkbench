from models.single_layer_gcn import SingleLayerGCN
import torch
import torch.nn.functional as F

def train(model, optimizer, data, device):
    model = SingleLayerGCN(dataset.num_features, dataset.num_classes)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    loss_fn = F.nll_loss

    # Train the model
    for epoch in range(200):
        model.train()
        optimizer.zero_grad()
        out = model(data.x, data.edge_index)
        loss = loss_fn(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()

def classify(nodes, edges): pass
    