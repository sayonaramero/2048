import random
import pygame
import sys

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
        self.lastmove = "None"
        self.moving = False

    

    def renderBoard(self): # draw
        pygame.draw.rect(screen, CONTAINERBG, (OFFSET_X, OFFSET_Y, CONTAINER, CONTAINER), border_radius=4)

        for a in range(4):
            for b in range(4):
                px, py = fetch_grid(a, b)
                gridval = self.grid[b][a]
                getcolor = pallete.get(gridval, (75, 98, 107))
                pygame.draw.rect(screen, getcolor, (px, py, TILE_SIZE, TILE_SIZE), border_radius=8)
                if gridval > 0:
                    text = FONT.render(str(gridval), True, (254, 255, 120))
                    text_rect = text.get_rect(center=(px + TILE_SIZE // 2, py + TILE_SIZE // 2))
                    screen.blit(text, text_rect)
        

    def generate_cell(self): # Render a cell

        all_empty_cells = []
        for y in range(4):
            for x in range(4):
                if self.grid[y][x] == 0:
                    all_empty_cells.append((y, x))


        if all_empty_cells:
            y, x = random.choice(all_empty_cells) # choose a cell
            # You parasite.

            self.grid[y][x] = 2 if random.random() < .8 else 4

        


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
                            self.grid[y][target-1] *= 2
                            self.grid[y][x] = 0
                            m[target-1] = True
                            moving = True
                        elif target != x:
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
                            self.grid[y][target+1] *= 2
                            self.grid[y][x] = 0
                            m[target+1] = True
                            moving = True
                        elif target != x:
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
                            self.grid[target-1][x] *= 2
                            self.grid[y][x] = 0
                            m[target-1] = True
                            moving = True
                        elif target != y:
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
                            self.grid[target+1][x] *= 2
                            self.grid[y][x] = 0
                            m[target+1] = True
                            moving = True
                        elif target != y:
                            self.grid[target][x] = self.grid[y][x]
                            self.grid[y][x] = 0
                            moving = True                            

            if moving:
                self.generate_cell()

        if self.checkgameover():
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

        


                


    
def get_ai_state(x):
    # We're getting the AI's decisions here ;)

    Actions = ['LEFT', 'RIGHT', 'UP', 'DOWN']

# @suji
def synew():
    game = run_game()

    
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    game.generate_cell()
                if event.key == pygame.K_a:
                    game.move_cell("left")
                elif event.key == pygame.K_d:
                    game.move_cell("right")
                elif event.key == pygame.K_w:
                    game.move_cell("up")
                elif event.key == pygame.K_s:
                    game.move_cell("down")        
        
        screen.fill(BGCOLOR)
        game.renderBoard()

        pygame.display.flip()
        clock.tick(48)

synew()