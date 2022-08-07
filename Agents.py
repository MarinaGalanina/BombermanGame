from abc import ABC, abstractmethod
from bcolors import bcolors
from random import choice
from Bomb import Bomb
from Powerups import Powerups


class Agent(ABC):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, x, y, lifes, representation, actual_position, color, bombs):
        self.x, self.y = x, y
        self.lifes = lifes
        self.color = color
        self.representation = representation  # UP, RIGHT, DOWN, LEFT
        self.actual_position = actual_position
        self.bombs =bombs
        self.bomb_size = 1

    def put_bomb(self):
        if self.bombs:
            self.bombs -= 1
            return Bomb(self.x, self.y, self.bomb_size, self)

    def get_representation(self):
        return self.representation[self.actual_position]

    def get_color(self):
        return self.color

    def get_position(self):
        return self.x, self.y

    def move(self, direction):
        self.actual_position = direction

        if direction == Agent.UP:
            self.y -= 1
        elif direction == Agent.DOWN:
            self.y += 1
        elif direction == Agent.LEFT:
            self.x -= 1
        elif direction == Agent.RIGHT:
            self.x += 1

    def random_move(self, moves):
        if moves:
            move = choice(moves)
            self.move(move)

    def __repr__(self):
        return self.representation[self.actual_position]


class MainPlayer(Agent):
    def __init__(self, x, y):
        super().__init__(x, y, 2, ["^", ">", "V", "<"], 0, bcolors.YELLOW, 1)

    def get_powerup(self, powerup):
        if powerup == Powerups.LIFE:
            self.lifes += 1
        elif powerup == Powerups.SIZE_PLUS:
            self.bomb_size +=1
        elif powerup == Powerups.BOMB_PLUS:
            self.bombs += 1


class Ghost(Agent):
    def __init__(self, x, y):
        super().__init__(x, y, 1, ["O", "0", "O", "0"], 0, bcolors.BlUE, 0)


class BomberGhost(Agent):
    def __init__(self, x, y):
        super().__init__(x, y, 1, ["O", "0", "O", "0"], 0, bcolors.RED, 1)

