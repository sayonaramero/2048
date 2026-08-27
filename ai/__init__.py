import torch
from torch import nn
from torch import optim
from colorama import Fore, Style

# -------- Constants -------- #

INPUT_LAYER_DIM = 16
HIDDEN_LAYER_DIM = 200
OUTPUT_LAYER_DIM = 4

# --------------------------- #

FALLBACK_DEVICE = "cpu"

# --------------------------- #

print(f"{Fore.GREEN}-- CUDA Available ({Fore.BLUE}{torch.cuda.get_device_name(0)}{Fore.GREEN}) --{Style.RESET_ALL}" if torch.cuda.is_available() else f"{Fore.RED}-- CUDA Unavailable, using fallback device ({Fore.BLUE}{FALLBACK_DEVICE}{Fore.RED}) --{Style.RESET_ALL}")

device = torch.device("cuda" if torch.cuda.is_available() else FALLBACK_DEVICE)

class model(nn.Module):
    def __init__(self):
        super(model, self).__init__()
        self.layers: list[nn.Linear | nn.ReLU] = [nn.Linear(INPUT_LAYER_DIM, HIDDEN_LAYER_DIM), nn.ReLU(), nn.Linear(HIDDEN_LAYER_DIM, OUTPUT_LAYER_DIM)]
    def forward(self, input: torch.Tensor):
        out = input
        for i, layer in enumerate(self.layers):
            out = layer(out)
        return out