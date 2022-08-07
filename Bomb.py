from bcolors import bcolors


class Bomb:
    def __init__(self, x, y, size, owner):
        self.x = x
        self.y = y
        self.size = size
        self.time = 6
        self.color = bcolors.UNDERLINE + bcolors.RED
        self.owner = owner

    def tick(self):
        self.time -= 1
        if self.time <= 0:
            return True

    def get_representation(self):
        return f"{self.time}"

    def get_color(self):
        return self.color

    def get_position(self):
        return self.x, self.y


class Fire:
    def __init__(self, area):
        self.area = area
        self.character = "*"
        self.color = bcolors.PINK

    def get_representation(self):
        return self.character

    def get_color(self):
        return self.color
