import torch
from torch import nn
from torch import optim
from colorama import Fore, Style
from random import randint

# -------- Constants -------- #

INPUT_LAYER_DIM = 16
HIDDEN_LAYER_DIM = 200
OUTPUT_LAYER_DIM = 4

# --------------------------- #

FALLBACK_DEVICE = "cpu"

# --------------------------- #

DEFAULT_GAMMA = 0.85

# --------------------------- #

DEFAULT_OPTIMIZER = optim.SGD
DEFAULT_ERROR_CRITERION = nn.MSELoss

print(f"{Fore.GREEN}-- CUDA Available ({Fore.BLUE}{torch.cuda.get_device_name(0)}{Fore.GREEN}) --{Style.RESET_ALL}" if torch.cuda.is_available() else f"{Fore.RED}-- CUDA Unavailable, using fallback device ({Fore.BLUE}{FALLBACK_DEVICE}{Fore.RED}) --{Style.RESET_ALL}")

device = torch.device("cuda" if torch.cuda.is_available() else FALLBACK_DEVICE)

torch.set_default_device(device)

class model(nn.Module):
    def __init__(self):
        super(model, self).__init__()
        self.layers = nn.ModuleList([
            nn.Linear(INPUT_LAYER_DIM, HIDDEN_LAYER_DIM),
            nn.ReLU(),
            nn.Linear(HIDDEN_LAYER_DIM, OUTPUT_LAYER_DIM),
        ])
    def forward(self, input: torch.Tensor):
        out = input
        for i, layer in enumerate(self.layers):
            out = layer(out)
        #print(out)
        return out
    def choose(self, output: torch.Tensor):
        with torch.no_grad():
            actions = torch.argmax(output, dim=0)
        random_actions = torch.randint(0, OUTPUT_LAYER_DIM, size=(len(output),))
        do_random_choice = torch.rand(len(output)) > 1
        choosen_actions = torch.where(do_random_choice, random_actions, actions)
        return choosen_actions
    def calculate_loss(self, legacy_q_value, next_state: torch.Tensor, reward: float, criterion) -> torch.Tensor:
        '''
        model_out_t1 2nd Prediction
        '''
        with torch.no_grad():
            next_prediction = self(next_state)
            #print(torch.max(next_prediction, dim=1))
            target = reward + DEFAULT_GAMMA * torch.max(next_prediction, dim=0)[0]

        #print(f"-----\n{next_prediction}")
        #print(f"Predicted Value: {legacy_q_values}\n---\nCorrect Value {target}")
        loss = criterion(legacy_q_value, target)
        return loss