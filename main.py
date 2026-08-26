import sys
import random
import numpy as np
import pygame

# --- CONFIGURATION & PARAMETERS ---
PROJECT_NAME = "Synew"
SCREEN_SIZE = 640
GRID_SIZE = 4
SLOT_SIZE = 128
PADDING = 16
FPS = 48
ANIMATION_SPEED = 24.0

# --- PYGAME INITIALIZATION ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption(PROJECT_NAME)
clock = pygame.time.Clock()

# --- ASSET LOADING---
def load_image(file_path, size):
    try:
        img = pygame.image.load(file_path).convert_alpha()
        return pygame.transform.smoothscale(img, (size, size))
    except (pygame.error, FileNotFoundError):

        surf = pygame.Surface((size, size))
        surf.fill((60, 58, 50))
        return surf

SPRITES = {
    0: load_image("EmptySlotImg.png", SLOT_SIZE),
    2: load_image("n2Img.png", SLOT_SIZE),
    4: load_image("n4Img.png", SLOT_SIZE),
    8: load_image("n8Img.png", SLOT_SIZE),
    16: load_image("n16Img.png", SLOT_SIZE),
}

# --- HELPER FUNCTIONS ---
def grid_to_pos(row, col):
    
    x = PADDING + col * (SLOT_SIZE + PADDING)
    y = PADDING + row * (SLOT_SIZE + PADDING)
    return pygame.Vector2(x, y)

# --- ANIMATED TILE CLASS ---
class AnimatedTile:
    def __init__(self, value, start_row, start_col, target_row, target_col):
        self.value = value
        self.pos = grid_to_pos(start_row, start_col)
        self.target_pos = grid_to_pos(target_row, target_col)

    def update(self, dt):
        # hi
        if self.pos.distance_to(self.target_pos) > 0.5:
            self.pos += (self.target_pos - self.pos) * min(1.0, ANIMATION_SPEED * dt)
        else:
            self.pos = pygame.Vector2(self.target_pos)

    def draw(self, surface):
        sprite = SPRITES.get(self.value, SPRITES[0])
        surface.blit(sprite, self.pos)

# --- GAME ENGINE ---
class synew2048:
    def __init__(self):
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.animated_tiles = []
        self.animating = False
        self.spawn_tile()
        self.spawn_tile()
        self.sync_animated_tiles()

    def get_state(self):
        
        return self.grid.copy()

    def spawn_tile(self):
        
        empty_slots = list(zip(*np.where(self.grid == 0)))
        if empty_slots:
            row, col = random.choice(empty_slots)
            self.grid[row, col] = 2 if random.random() < 0.9 else 4

    def sync_animated_tiles(self):
       
        self.animated_tiles = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                val = self.grid[r, c]
                if val != 0:
                    self.animated_tiles.append(AnimatedTile(val, r, c, r, c))

    def compress_and_merge_row(self, row):
        non_zero = row[row != 0]
        new_row = []
        skip = False

        for i in range(len(non_zero)):
            if skip:
                skip = False
                continue
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                new_row.append(non_zero[i] * 2)
                skip = True
            else:
                new_row.append(non_zero[i])

        new_row = np.array(new_row, dtype=int)
        padding = np.zeros(GRID_SIZE - len(new_row), dtype=int)
        return np.concatenate((new_row, padding))

    def move(self, direction):
        """
        Executes a direction move: 'LEFT', 'RIGHT', 'UP', 'DOWN'.
        Tracks initial and final positions to instantiate sliding animations.
        """

        if self.animating:
            return

        rotations = {'LEFT': 0, 'UP': 1, 'RIGHT': 2, 'DOWN': 3}[direction]
        rotated_grid = np.rot90(self.grid, -rotations)
        new_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

        move_events = []
        for r in range(GRID_SIZE):
            original_row = rotated_grid[r]
            merged_row = self.compress_and_merge_row(original_row)
            new_grid[r] = merged_row
            non_zero_indices = np.where(original_row != 0)[0]
            target_col = 0
            idx = 0
            while idx < len(non_zero_indices):
                src_c = non_zero_indices[idx]
                val = original_row[src_c]
                
                if idx + 1 < len(non_zero_indices) and original_row[non_zero_indices[idx + 1]] == val:
                    move_events.append((r, src_c, r, target_col, val, val * 2))
                    move_events.append((r, non_zero_indices[idx + 1], r, target_col, val, val * 2))
                    idx += 2
                else:
                    move_events.append((r, src_c, r, target_col, val, val))
                    idx += 1
                target_col += 1

        final_grid = np.rot90(new_grid, rotations)

        if not np.array_equal(self.grid, final_grid):
            self.animated_tiles = []
            for r_rot, c_rot, tr_rot, tc_rot, val, end_val in move_events:

                r, c = self._unrotate_coords(r_rot, c_rot, rotations)
                tr, tc = self._unrotate_coords(tr_rot, tc_rot, rotations)
                self.animated_tiles.append(AnimatedTile(val, r, c, tr, tc))

            self.grid = final_grid
            self.animating = True

    def _unrotate_coords(self, r, c, rotations):
  
        arr = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        arr[r, c] = 1
        arr = np.rot90(arr, rotations)
        unrotated_pos = np.where(arr == 1)
        return int(unrotated_pos[0][0]), int(unrotated_pos[1][0])

    def update(self, dt):
       
        if not self.animating:
            return

        all_done = True
        for tile in self.animated_tiles:
            tile.update(dt)
            if tile.pos.distance_to(tile.target_pos) > 0.5:
                all_done = False

        if all_done:
            self.animating = False
            self.spawn_tile()
            self.sync_animated_tiles()

    def draw(self, surface):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                surface.blit(SPRITES[0], grid_to_pos(r, c))

        for tile in self.animated_tiles:
            tile.draw(surface)

# --- MAIN LOOP ---
def main():
    game = synew2048()

    while True:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not game.animating:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.move('LEFT')
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.move('RIGHT')
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    game.move('UP')
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    game.move('DOWN')
        game.update(dt)

        # Renders
        screen.fill((40, 36, 32))
        game.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()