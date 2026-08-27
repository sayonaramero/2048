import random
import pygame
import sys
from logic import Game, Movement, Verbosity
import copy
# Configuration

OFFSET_Y = 130
OFFSET_X = 70
SCREENSIZE = 640
CONTAINER = 490
PADDING = 10
TILE_SIZE = 110
BGCOLOR = (70, 80, 84)
CONTAINERBG = (39, 46, 48)


# Initialization

pygame.init()
screen = pygame.display.set_mode((SCREENSIZE, SCREENSIZE))
pygame.display.set_caption("Synew")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 32, bold=True, italic=False)
SCORE_TITLE_FONT = pygame.font.SysFont("arial", 16, bold=True)
SCORE_VAL_FONT = pygame.font.SysFont("arial", 20, bold=True)
Running = True

# I can see colors!!

pallete = {
     0: (75, 98, 107),
     2: (71, 143, 186),
     4: (65, 237, 224),
     8: (131, 161, 250),
     16: (127, 123, 194),
     32: (74, 25, 125),
     64: (163, 114, 204),
     128: (158, 98, 135),
     256: (186, 121, 81),
     512: (94, 163, 54),
     1024: (188, 11, 16),
     2048: (240, 5, 227),
     4096: (240, 5, 5)
}

# Fetch the grid

def fetch_grid(x, y):

    dx = (PADDING + x * (TILE_SIZE + PADDING)) + OFFSET_X
    dy = (PADDING + y * (TILE_SIZE + PADDING)) + OFFSET_Y

    return dx, dy


# Self-explanatory

class run_game:
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.bestscore = 0
        self.lastmove = "None"
        self.moving = False
        self.animations = []
        self.isanimating = False
        self.game_over = False

        self.generate_cell()
        self.generate_cell()
    
    def reset(self):
        if self.game_over == True:
            self.grid = [[0] * 4 for _ in range(4)]
            self.score = 0
            self.bestscore = 0
            self.lastmove = "None"
            self.moving = False
            self.animations = []
            self.isanimating = False

            self.generate_cell()
            self.generate_cell()
    
    def renderBoard(self): # draw

        self.draw_score_box("SCORE", self.score, OFFSET_X + CONTAINER - 210)
        self.draw_score_box("BEST", self.bestscore, OFFSET_X + CONTAINER - 100)

        pygame.draw.rect(screen, CONTAINERBG, (OFFSET_X, OFFSET_Y, CONTAINER, CONTAINER), border_radius=4)


        animating_origins = []
        if self.isanimating:
            for anim in self.animations:
                animating_origins.append((anim["start_x"], anim["start_y"]))

                
         
        for a in range(4):
            for b in range(4):
                px, py = fetch_grid(a, b)
                gridval = self.grid[b][a]
                if self.isanimating and (a, b) in animating_origins:
                    self.draw_single_tile(px, py, 0)
                else:
                    self.draw_single_tile(px, py, gridval)

        if self.isanimating:
            for anim in self.animations:
                self.draw_single_tile(anim["c_x"], anim["c_y"], anim["value"])
        

    def generate_cell(self): # Render a cell

        all_empty_cells = []
        for y in range(4):
            for x in range(4):
                if self.grid[y][x] == 0:
                    all_empty_cells.append((y, x))


        if all_empty_cells:
            y, x = random.choice(all_empty_cells) # choose a cell

            self.grid[y][x] = 2 if random.random() < .8 else 4

    def add_animation(self, val, start_x, start_y, target_x, target_y):
        start_dx, start_dy = fetch_grid(start_x, start_y)
        end_dx, end_dy = fetch_grid(target_x, target_y)

        self.animations.append({
            "value": val,
            "start_x": start_x,
            "start_y": start_y,
            "c_x": int(start_dx),
            "c_y": int(start_dy),
            "target_x": int(end_dx),
            "target_y": int(end_dy)
        })
        self.isanimating = True

    def get_animations(self):
        if not self.animations:
            self.isanimating = False
            return

        speed = 30  #px
        isfinished = True

        for anim in self.animations:
            # le horizontal movement 🤩
            if anim['c_x'] < anim['target_x']:
                anim['c_x'] = min(anim['c_x'] + speed, anim['target_x'])
                isfinished = False
            elif anim['c_x'] > anim['target_x']:
                anim['c_x'] = max(anim['c_x'] - speed, anim['target_x'])
                isfinished = False

            # vertical movement
            if anim['c_y'] < anim['target_y']:
                anim['c_y'] = min(anim['c_y'] + speed, anim['target_y'])
                isfinished = False
            elif anim['c_y'] > anim['target_y']:
                anim['c_y'] = max(anim['c_y'] - speed, anim['target_y'])
                isfinished = False

        if isfinished:
            self.animations.clear()
            self.isanimating = False


    def draw_score_box(self, label, value, x_pos):
        box_w, box_h = 100, 50
        y_pos = 40
        pygame.draw.rect(screen, CONTAINERBG, (x_pos, y_pos, box_w, box_h), border_radius=6)
        
        # label
        lbl_surf = SCORE_TITLE_FONT.render(label, True, (150, 160, 165))
        lbl_rect = lbl_surf.get_rect(center=(x_pos + box_w // 2, y_pos + 14))
        screen.blit(lbl_surf, lbl_rect)

        # value
        val_surf = SCORE_VAL_FONT.render(str(value), True, (255, 255, 255))
        val_rect = val_surf.get_rect(center=(x_pos + box_w // 2, y_pos + 34))
        screen.blit(val_surf, val_rect)
        
    def draw_single_tile(self, px, py, val):
        getcolor = pallete.get(val, (75, 98, 107))
        pygame.draw.rect(screen, getcolor, (px, py, TILE_SIZE, TILE_SIZE), border_radius=8)
        if val > 0:
            text = FONT.render(str(val), True, (254, 255, 120))
            text_rect = text.get_rect(center=(px + TILE_SIZE // 2, py + TILE_SIZE // 2))
            screen.blit(text, text_rect)


    def move_cell(self, Direction):
        moving = self.moving
        if Direction == "left":
            moving = False

            for y in range(4):

                m = [False] * 4

                for x in range(1, 4):
                    if self.grid[y][x] != 0:
                        target = x

                        while target > 0 and self.grid[y][target - 1] == 0:
                            target -= 1

                        if target > 0 and self.grid[y][target-1] == self.grid[y][x] and not m[target-1]:
                            self.add_animation(self.grid[y][x], x, y, target - 1, y)
                            self.grid[y][target-1] *= 2
                            self.score += self.grid[y][target - 1]
                            self.grid[y][x] = 0
                            m[target-1] = True
                            moving = True
                        elif target != x:
                            self.add_animation(self.grid[y][x], x, y, target, y)
                            self.grid[y][target] = self.grid[y][x]
                            self.grid[y][x] = 0
                            moving = True
            if moving:
                self.generate_cell()

        elif Direction == "right":
            moving = False

            for y in range(4):

                m = [False] * 4

                for x in range(2, -1, -1):
                    if self.grid[y][x] != 0:
                        target = x

                        while target < 3 and self.grid[y][target + 1] == 0:
                            target += 1

                        if target < 3 and self.grid[y][target+1] == self.grid[y][x] and not m[target+1]:
                            self.add_animation(self.grid[y][x], x, y, target + 1, y)
                            self.grid[y][target+1] *= 2
                            self.score += self.grid[y][target + 1]
                            self.grid[y][x] = 0
                            m[target+1] = True
                            moving = True
                        elif target != x:
                            self.add_animation(self.grid[y][x], x, y, target, y)
                            self.grid[y][target] = self.grid[y][x]
                            self.grid[y][x] = 0
                            moving = True
            if moving:
                self.generate_cell()
        
        elif Direction == "up":
            moving = False

            for x in range(4):

                m = [False] *4

                for y in range(1, 4):
                    if self.grid[y][x] != 0:
                        target = y

                        while target > 0 and self.grid[target-1][x] == 0:
                            target -= 1

                        if target > 0 and self.grid[target-1][x] == self.grid[y][x] and not m[target-1]:
                            self.add_animation(self.grid[y][x], x, y, x, target - 1)
                            self.grid[target-1][x] *= 2
                            self.score += self.grid[target - 1][x]
                            self.grid[y][x] = 0
                            m[target-1] = True
                            moving = True
                        elif target != y:
                            self.add_animation(self.grid[y][x], x, y, x, target)
                            self.grid[target][x] = self.grid[y][x]
                            self.grid[y][x] = 0
                            moving = True
            if moving:
                self.generate_cell()

        elif Direction == "down":
            moving = False

            for x in range(4):

                m = [False] *4

                for y in range(2, -1, -1):
                    if self.grid[y][x] != 0:
                        target = y

                        while target < 3 and self.grid[target+1][x] == 0:
                            target += 1

                        if target < 3 and self.grid[target+1][x] == self.grid[y][x] and not m[target+1]:
                            self.add_animation(self.grid[y][x], x, y, x, target + 1)
                            self.grid[target+1][x] *= 2
                            self.score += self.grid[target + 1][x]
                            self.grid[y][x] = 0
                            m[target+1] = True
                            moving = True
                        elif target != y:
                            self.add_animation(self.grid[y][x], x, y, x, target)
                            self.grid[target][x] = self.grid[y][x]
                            self.grid[y][x] = 0
                            moving = True                            

            if moving:
                self.generate_cell()

        if self.checkgameover():
            self.game_over = True
            print("GAME OVER")

        
        

    def checkgameover(self):

        for y in range(4):
            for x in range(4):
                if self.grid[y][x] == 0:
                    return False

        for y in range(4):
            for x in range(3):
                if self.grid[y][x] == self.grid[y][x + 1]:
                    return False

        for y in range(3):
            for x in range(4):
                if self.grid[y][x] == self.grid[y + 1][x]:
                    return False

        return True

        


                


    
def get_ai_move(current_grid):
    """Validates or invalidates the AI's next step and shoots it through."""
    best_move = None
    best_score = -1
    valid_moves = []
    
    for direction in [Movement.UP, Movement.DOWN, Movement.LEFT, Movement.RIGHT]:
        sim = Game(Verbosity.NO_DEBUG)
        sim.position_matrix = copy.deepcopy(current_grid)
        sim.move(direction)
        
        if sim.position_matrix != current_grid:
            valid_moves.append(direction)
            empty_spaces = sum(row.count(0) for row in sim.position_matrix)
            
            if empty_spaces > best_score:
                best_score = empty_spaces
                best_move = direction
                
    if best_move is None and valid_moves:
        game = run_game()
        game.checkgameover()
        return valid_moves[0]
        
    return best_move
# @suji
def synew():
    
    AI_ENABLED = False
    DELAY = 750 # miliseconds
    game = run_game()
    last_move = pygame.time.get_ticks()

    directions = {
        Movement.UP: "up",
        Movement.DOWN: "down",
        Movement.LEFT: "left",
        Movement.RIGHT: "right"

    }
    
    while True:
        time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not AI_ENABLED and not game.isanimating:
                if event.key == pygame.K_a: game.move_cell("left")
                elif event.key == pygame.K_d: game.move_cell("right")
                elif event.key == pygame.K_w: game.move_cell("up")
                elif event.key == pygame.K_s: game.move_cell("down")        

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: game.reset()
                if event.key == pygame.K_TAB:
                    AI_ENABLED = not AI_ENABLED
                    print(f"ai enabled: {AI_ENABLED}")


        if AI_ENABLED and (time - last_move > DELAY) and not game.isanimating:

            chosen_move = get_ai_move(game.grid)

            if chosen_move:

                game.move_cell(directions[chosen_move])

                last_move = time
            else:
                game.checkgameover()

        game.get_animations()
        screen.fill(BGCOLOR)
        game.renderBoard()

        pygame.display.flip()
        clock.tick(60)

synew()