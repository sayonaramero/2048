from enum import Enum, StrEnum
from random import randint
from colorama import Style, Fore
import copy
import math

# alliases (ignore)



# Base Parameters (DO NOT CHANGE UNLESS YOU MODIFIED THE BASE GAME)

GRID_UNITS = 4
GRID_SIZE = (GRID_UNITS, GRID_UNITS)

# Enums

class Verbosity(Enum):
    '''
    Defines the level of Verbosity
    '''
    NO_DEBUG = 0
    BASIC_DEBUG = 1
    FULL_DEBUG = 2

class Orientation(Enum):
    ROW = 0
    COLUMN = 1

class DebugType(StrEnum):
    LOG = f"{Fore.GREEN}[i]{Style.RESET_ALL}"
    WARNING = f"{Fore.YELLOW}[W]{Style.RESET_ALL}"
    ERROR = f"{Fore.RED}[!]{Style.RESET_ALL}"

class Movement(Enum):
    '''
    Defines movement direction
    '''
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

# Data-Processing Methods

def _movement_step_indexer(i: int, move: Movement):
    '''
    Gives the layer to process from the movement (e.g. DOWN, 0 -> 2, ROW)
    '''
    is_positive = move == Movement.UP or move == Movement.RIGHT
    _ = Orientation.ROW if move == Movement.DOWN or move == Movement.UP else Orientation.COLUMN 
    return i if not is_positive else (GRID_UNITS - 1)-i, _

def _flip_matrix(matrix: list[list]) -> list:
    matrix_copy = copy.deepcopy(matrix)
    try:
        for r, rv in enumerate(matrix):
            for c, cell_value in enumerate(rv):
                matrix_copy[(GRID_UNITS - 1) - c][(GRID_UNITS - 1) - r] = cell_value
        return matrix_copy
    except IndexError:
        print(f"{DebugType.ERROR.value} YOU CAN ONLY USE A aXa dimensional list [matrix]")


def _direction_to_absolute_mov_dir(move: Movement) -> tuple[list[int,int], bool]:
    '''
    Tells the direction which the cell value will be added
    '''
    is_column = move == Movement.DOWN or move == Movement.UP
    is_positive = move == Movement.UP or move == Movement.RIGHT
    abs_dir = 0

    if is_positive:
        abs_dir = -1
    else:
        abs_dir = 1

    return abs_dir, is_column


print("Game Logic Engine Starting!")

class Game():
    def check_game_over(self) -> bool:
        '''
        Checks for the Game Over
        '''
        for row in range(GRID_UNITS):
            for column in range(GRID_UNITS):
                if self.position_matrix[row][column] == 0:
                    return False
                if column < GRID_UNITS - 1 and self.position_matrix[row][column] == self.position_matrix[row][column + 1]:
                    return False
                if column > 0 and self.position_matrix[row][column] == self.position_matrix[row][column - 1]:
                    return False
                if row < GRID_UNITS - 1 and self.position_matrix[row][column] == self.position_matrix[row + 1][column]:
                    return False
                if row > 0 and self.position_matrix[row][column] == self.position_matrix[row - 1][column]:
                    return False
        self.is_game_over = True
        return True

    def log(self, msg: str, verbosity_lvl: int, debug_type: DebugType=DebugType.LOG):
        if self.verbosity.value >= verbosity_lvl:
            print(f"{debug_type.value} {msg}")
    
    def reset_matrix(self):
        if self.verbosity.value > 0:
            print("Reseting Matrix")
        self.position_matrix = self.position_matrix = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]
    def get_empty_squares(self):
        empty_squares: list[list[int, int]] = []
        # Checks the empty squares
        for row in range(GRID_SIZE[1]):
            for column in range(GRID_SIZE[0]):
                if self.position_matrix[row][column] == 0:
                    empty_squares.append([row, column])
        return len(empty_squares)
    def generate_random_block(self) -> bool:
        '''
        Generates random blocks in the grid
        '''
        empty_squares: list[list[int, int]] = []

        # Checks the empty squares
        
        for row in range(GRID_SIZE[1]):
            for column in range(GRID_SIZE[0]):
                if self.position_matrix[row][column] == 0:
                    empty_squares.append([row, column])
        if len(empty_squares) == 0:
            self.check_game_over()
            return False

        random_square = empty_squares[randint(0, len(empty_squares) - 1)]

        square_value = 2 if randint(1,10) != 10 else 4
        self.position_matrix[random_square[0]][random_square[1]] = square_value

        
        #print(f"Generating {square_value} at X {random_square[0]} Y {random_square[1]}")
        self.log(f"Generating {square_value} at X {random_square[0]} Y {random_square[1]}", 1)
        return True

    def move(self, direction: Movement) -> int:
        '''
        Moves the matrix
        '''
        self.moves += 1
        merged = []
        # Counts how many unions were made
        unions = 0

        new_matrix = copy.deepcopy(self.position_matrix)
        mv, is_column = _direction_to_absolute_mov_dir(direction)
        self.log(f"Is movement Column? <{is_column}> MV: <{mv}>", 2)
        if not is_column:
            #mv = 0 - mv
            self.log(f"old Matrix <{new_matrix}>", 2)
            new_matrix = _flip_matrix(new_matrix)
        matrix_str = str(new_matrix).replace('],', ']\n')
        self.log(f"Old Matrix <\n{matrix_str}>", 2)
        for batch in range(GRID_UNITS - 1):
            for step in range(GRID_UNITS - 1):
                #step = _step + batch
                #self.log(f"{step} | {batch} | {_step}", 1)
                index, orientation = _movement_step_indexer(step, direction)
                #print
                for item_index in range(GRID_UNITS):
                    operator = new_matrix[index][item_index]
                    operated = new_matrix[index + mv][item_index]
                    if (operated == operator and batch == 0) or operated == 0:
                        if operated == operator and operated != 0 and batch == 0:
                            #print(new_matrix)
                            merged.append(math.log2(operated))
                            unions += 1
                        new_matrix[index + mv][item_index] = operated + operator
                        new_matrix[index][item_index] = 0
            mtrx_str = f"{new_matrix}".replace("],", "]\n")
            self.log(f'\n{mtrx_str}', 1)

        if not is_column:
            new_matrix = _flip_matrix(new_matrix)
        mtrx_str = f"{new_matrix}".replace("],", "]\n")
        self.log(f'\n{mtrx_str}', 1)
        self.position_matrix = new_matrix

        return unions, merged

    def __init__(self, verbosity: Verbosity):
        self.verbosity = verbosity
        #print("Game Started", 1)
        self.moves = 0
        self.is_game_over: bool = False
        self.position_matrix = self.position_matrix = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]

# Example Game Client (Terminal)

'''

gm = Game(Verbosity.FULL_DEBUG)

try:
    while True:
        inp = input("Key: ")
        keycode = {"w": Movement.UP, "a": Movement.LEFT, "s": Movement.DOWN, "d": Movement.RIGHT}
        move = keycode.get(inp.lower())
        if move:
            gm.move(move)
            gm.generate_random_block()
            gm_pos = str(gm.position_matrix).replace('],', ']\n')
            gm.log(f"BOARD:\n{Fore.BLUE}{gm_pos}{Style.RESET_ALL}", 1)
        else:
            gm.log("Invalid Key", 0, DebugType.WARNING)
except KeyboardInterrupt:
    print("Exiting...")

'''