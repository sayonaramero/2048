from enum import Enum
from random import randint

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
    _ = Orientation.ROW if move == Movement.DOWN or move == Movement.UP else Orientation.COLUMN 
    return 2-i, _

def _direction_to_absolute_mov_dir(move: Movement)
    is_column = move == Movement.DOWN or move == Movement.UP
    is_positive = move == Movement.UP or move == Movement.RIGHT
    abs_dir = [0, 0]

    if is_column:
        if is_positive:
            abs_dir[1] = -1
        else:
            abs_dir[1] = 1
    else:
        if is_positive:
            abs_dir[0] = -1
        else:
            abs_dir[0] = 1


print("Game Logic Engine Starting!")

class Game():
    def reset_matrix(self):
        if self.verbosity.value > 0:
            print("Reseting Matrix")
        self.position_matrix = self.position_matrix = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]

    def generate_random_block(self):
        '''
        Generates random blocks in the grid
        '''
        empty_squares: list[list[int, int]] = []

        # Checks the empty squares

        for row in range(GRID_SIZE[1]):
            for column in range(GRID_SIZE(0)):
                if self.position_matrix[row][column] == 0:
                    empty_squares.append([row, column])

        random_square = empty_squares[randint(0, len(empty_squares))]

        square_value = 2 if randint(1,10) != 10 else 4
        self.position_matrix[random_square[0], random_square[1]] = square_value

        if self.verbosity.value > 0:
            print(f"Generating {square_value} at X {random_square[0]} Y {random_square[1]}")

    def move(direction: Movement):
        '''
        Moves the matrix
        '''
        pass

        for step in range(GRID_UNITS - 1):
            index, orientation = _movement_step_indexer(step, direction)


    def __init__(self, verbosity: Verbosity):
        self.verbosity = verbosity
        print("Game Started")
        
        self.position_matrix = self.position_matrix = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]

    