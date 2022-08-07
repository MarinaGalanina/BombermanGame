from abc import ABC, abstractmethod
from bcolors import bcolors
from Powerups import Powerups


class Block(ABC):
    def __init__(self, color, life, character, point):
        self.color = color
        self.character = character
        self.life = life
        self.point = point

    def get_point(self):
        return self.point

    def change_representation(self, character, col):
        self.color = col
        self.character = character

    @abstractmethod
    def original_representation(self):
        pass

    def __repr__(self):
        return self.color + self.character + bcolors.ENDC


class ObsidianBlock(Block):
    def __init__(self):
        super().__init__(bcolors.WHITE, 9999999, "#", 0)

    def original_representation(self):
        self.color = bcolors.WHITE
        self.character = "#"


class HardBlock(Block):
    def __init__(self):
        super().__init__(bcolors.RED, 3, "#", 5)

    def original_representation(self):
        self.color = bcolors.RED
        self.character = "#"


class MiddleBlock(Block):
    def __init__(self):
        super().__init__(bcolors.PINK, 2, "#", 3)

    def original_representation(self):
        self.color = bcolors.PINK
        self.character = "#"


class WeakBlock(Block):
    def __init__(self):
        super().__init__(bcolors.YELLOW, 1, "#", 1)

    def original_representation(self):
        self.color = bcolors.YELLOW
        self.character = "#"


class NoneBlock(Block):
    def __init__(self, is_powerup):
        super().__init__(bcolors.GREEN, 0, "!", 0)
        self.is_powerup = is_powerup
        self.powerup = None
        if self.is_powerup:
            self.character = "!"
            if self.powerup == Powerups.LIFE:
                self.color = bcolors.RED
            elif self.powerup == Powerups.BOMB_PLUS:
                self.color = bcolors.YELLOW
            else:
                self.color = bcolors.GREEN
        else:
            self.character = " "
            self.color = bcolors.ENDC

    def original_representation(self):
        if self.is_powerup:
            self.character = "!"
            if self.powerup == Powerups.LIFE:
                self.color = bcolors.RED
            elif self.powerup == Powerups.BOMB_PLUS:
                self.color = bcolors.YELLOW
            else:
                self.color = bcolors.GREEN

        else:
            self.character = " "
            self.color = bcolors.ENDC


