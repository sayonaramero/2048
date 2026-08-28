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
import time
from logic import Verbosity, Movement
import copy
import json

torch.set_default_device(ai.device)

BATCHES = 4
DEFAULT_VERBOSITY = Verbosity.NO_DEBUG
models = [ai.model() for _ in range(2)]
cycles = 1000

crit = torch.nn.MSELoss()

def get_game_matrix(games: list[logic.Game]) -> list:
    #success = game.generate_random_block()
    #if not success:
    #    game.check_game_over()
    matrix = []
    for row in game.position_matrix:
        for item in row:
            matrix.append(item)
    return matrix

best_weights = {}

while True:
    do_load = input("Load past weights? [y/n]\n> ")
    if do_load.lower() == "y":
        print("Loading past weights...")
        weights = torch.load('weights.pth', weights_only=True)
        for md in models:
            md.load_state_dict(weights)
        print("Done!")
        break
    elif do_load.lower() == "n":
        weights = torch.load('weights.pth', weights_only=True)
        torch.save(weights, 'weights.pth.backup')
        break

try:
    for life_id in range(1000):
        max_moves = []
        rewards_ind = torch.tensor([0 for _ in range(len(models))], dtype=torch.float32)
        rewards = [[] for _ in range(len(models))]
        games = [logic.Game(DEFAULT_VERBOSITY) for _ in range(len(models))]
        for game_id, model in enumerate(models):
            game = games[game_id]
            for game_loop in range(cycles):
                #while True:
                dataset = get_game_matrix(game)
                game.generate_random_block()

                #print(torch.randn(4, ai.INPUT_LAYER_DIM))        
                prediction = model(torch.tensor(dataset, dtype=torch.float32))
                #print(pred)

                while True:
                    choices = model.choose(prediction).tolist()
                    mtr_b = copy.deepcopy(game.position_matrix)
                    _rww, moved_tiles = game.move(Movement(choices[0] + 1))

                    moved_tiles = sum(moved_tiles)

                    mtr_af = copy.deepcopy(game.position_matrix)
                    if mtr_b == mtr_af and not game.check_game_over():
                        prediction[choices[0]] = -float('inf')
                    else:
                        break
                #if rewards[i] <= 10:
                '''
                _reward = torch.tensor([0 for _ in range(logic.GRID_UNITS**2)], dtype=torch.float32)
                for r_idx in range((logic.GRID_UNITS**2) - 1):
                    #print(r_idx)
                    _reward[r_idx + 1] = (_reward[r_idx] / 2)

                _reward *= 1.4

                _reward = _reward - torch.tensor(dataset, dtype=torch.float32)
                _rw = (game.get_empty_squares() + _rww) * (game_loop / cycles)
                if _rww < 1:
                    rwt = len(rewards[game_id])
                    _rw = 0 - ((sum(rewards[game_id]) / (rwt + 0.01)) / 2)
                #print(_rw)
                '''
                if game.is_game_over:
                    print("GAME OVER!")
                    break
                reward = moved_tiles
                reward += 0.1 * game.get_empty_squares()

                rewards[game_id].append(reward)
                rewards_ind[game_id] += reward
                new_state = torch.tensor(get_game_matrix(games), dtype=torch.float32)
                loss = model.calculate_loss(torch.max(prediction, dim=0)[0], new_state, reward, crit)
                loss.backward()
                model.zero_grad()
            max_moves.append(game.moves)
        id = torch.argmax(rewards_ind)

        best_weights = copy.deepcopy(models[id].state_dict())

        for i in range(len(models)):
            if i != id:
                models[i].load_state_dict(best_weights)

        mtrx_str = f"{games[id].position_matrix}".replace("],", "]\n")
        games[id].log(f"\n{mtrx_str}", 0)
        rwt = len(rewards[id])
        
        print(f"Rewards on life #{life_id + 1} - {sum(rewards[id]) / rwt} - Moves: {cycles}/{games[id].moves}")
        #if rewards[id] < -1 and cycles >= 60:
        #    cycles -= 10
        #if life_id % 5 == 0:
        #    cycles += 3
except KeyboardInterrupt:
    print("Exiting...")
finally:
    torch.save(best_weights, 'weights.pth')
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
