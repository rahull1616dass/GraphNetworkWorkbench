import torch


def set_up_device(seed: int = 42) -> torch.device:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        device = torch.device("cuda")
        torch.cuda.manual_seed(seed)
    else:
        device = torch.device("cpu")
    return device
