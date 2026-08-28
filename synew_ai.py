'''
import ai
import torch

model = ai.model()
inp_dummy = torch.randn(4, ai.INPUT_LAYER_DIM)
inp_dummy2 = torch.randn(4, ai.INPUT_LAYER_DIM)
correct = torch.randn(4, ai.OUTPUT_LAYER_DIM)

crit = ai.DEFAULT_ERROR_CRITERION()
optim = torch.optim.SGD(model.parameters(), lr=0.01)

prediction = model(inp_dummy)
choices = model.choose(prediction)
print(choices)
#print(f"ABC \n{prediction.gather(dim=1, index=choices.unsqueeze(1))} \n - 123 - \n{prediction.gather(dim=1, index=choices.unsqueeze(1)).unsqueeze(1)}")
criterion = ai.DEFAULT_ERROR_CRITERION()
loss = model.calculate_loss(prediction.gather(dim=1, index=choices.unsqueeze(1)).squeeze(1), inp_dummy2, -1, criterion)
loss.backward()

prediction = model(inp_dummy)
choices = model.choose(prediction)
print(choices)
#optim.step()

#print(f"Initial Loss: {loss.item():.4f}")
#print("Model update successful!")
'''

import ai
import torch
import logic
from logic import Verbosity, Movement

BATCHES = 4
DEFAULT_VERBOSITY = Verbosity.BASIC_DEBUG
model = ai.model()
lifes = 2

while True:
    for game_loop in range(lifes):
        games = [logic.Game(DEFAULT_VERBOSITY) for _ in range(BATCHES)]

        dataset = []

        for game in games:
            matrix = []
            for row in game.position_matrix:
                for item in row:
                    matrix.append(item)
            dataset.append(matrix)
        #print(torch.randn(4, ai.INPUT_LAYER_DIM))        
        prediction = model(torch.tensor(dataset, dtype=torch.float32))
        choices = model.choose(prediction)
        print(choices)
    lifes += 1
    break
exit()
'''
game = logic.Game(Verbosity.FULL_DEBUG)

inp_dummy = torch.randn(4, ai.INPUT_LAYER_DIM)
inp_dummy2 = torch.randn(4, ai.INPUT_LAYER_DIM)
correct = torch.randn(4, ai.OUTPUT_LAYER_DIM)

#crit = ai.DEFAULT_ERROR_CRITERION()
#optim = torch.optim.SGD(model.parameters(), lr=0.01)

print(choices)
#print(f"ABC \n{prediction.gather(dim=1, index=choices.unsqueeze(1))} \n - 123 - \n{prediction.gather(dim=1, index=choices.unsqueeze(1)).unsqueeze(1)}")
criterion = ai.DEFAULT_ERROR_CRITERION()
loss = model.calculate_loss(prediction.gather(dim=1, index=choices.unsqueeze(1)).squeeze(1), inp_dummy2, -1, criterion)
loss.backward()

prediction = model(inp_dummy)
choices = model.choose(prediction)
print(choices)
#optim.step()

#print(f"Initial Loss: {loss.item():.4f}")
#print("Model update successful!")
'''