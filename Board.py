from random import randint, choice
import numpy as np
import os

from Blocks import HardBlock, MiddleBlock, WeakBlock, ObsidianBlock, NoneBlock, Block
from Agents import MainPlayer, Ghost, BomberGhost, Agent
from Bomb import Fire
from Powerups import Powerups


class Board:

    def __init__(self, rows, columns):

        self.high, self.width = rows + 2, columns + 2
        self.board = None
        self.score = 0

        self.player = None
        self.ghosts = []
        self.bomber_ghosts = []
        self.bombs = []
        self.fire = []
        self.power_ups = []

        self._init_board()

    def _init_board(self):
        self.board = None
        self.score = 0

        self.player = None
        self.ghosts = []
        self.bomber_ghosts = []
        self.bombs = []
        self.fire = []
        self.power_ups = [Powerups.LIFE, Powerups.LIFE, Powerups.SIZE_PLUS,
                          Powerups.SIZE_PLUS, Powerups.BOMB_PLUS, Powerups.LIFE]

        self.board = np.empty((self.high, self.width), dtype=Block)


        for col in range(self.width):
            for row in range(self.high):
                self.board[col][row] = NoneBlock(False)

        self._make_border()
        self._obsidian_grid()
        self._add_blocks(17, 17, 33)
        self._add_player()
        self._add_ghosts(9, 1)

    def _obsidian_grid(self):
        self.board[2:self.high - 1:2, 2:self.width - 1:2] = ObsidianBlock()

    def _make_border(self):
        self.board[0:self.high, 0:1] = ObsidianBlock()
        self.board[0:self.high, self.width - 1:self.width] = ObsidianBlock()
        self.board[0:1, 0:self.width] = ObsidianBlock()
        self.board[self.high - 1:self.high, 0:self.width] = ObsidianBlock()

    def _add_blocks(self, hard: int, midd: int, weak: int):
        while hard:
            x, y = randint(1, self.width - 2), randint(1, self.high - 2)
            if type(self.board[y][x]) is NoneBlock:
                self.board[y][x] = HardBlock()
                hard -= 1

            while midd:
                x, y = randint(1, self.width - 2), randint(1, self.high - 2)
                if type(self.board[y][x]) is NoneBlock:
                    self.board[y][x] = MiddleBlock()
                    midd -= 1

            while weak:
                x, y = randint(1, self.width - 2), randint(1, self.high - 2)
                if type(self.board[y][x]) is NoneBlock:
                    self.board[y][x] = WeakBlock()
                    weak -= 1

    def _add_player(self):

        while True:
            x, y = randint(1, self.width - 2), randint(1, self.high - 2)
            if type(self.board[y][x]) == NoneBlock:
                self.player = MainPlayer(x, y)
                return

    def _add_ghosts(self, ghost_cnt: int, bomb_ghost_cnt: int):
        while ghost_cnt:
            x, y = randint(1, self.width - 2), randint(1, self.high - 2)
            if type(self.board[y][x]) == NoneBlock:
                self.ghosts.append(Ghost(x, y))
                ghost_cnt -= 1
        while bomb_ghost_cnt:
            x, y = randint(1, self.width - 2), randint(1, self.high - 2)
            if type(self.board[y][x]) == NoneBlock:
                self.bomber_ghosts.append(BomberGhost(x, y))
                bomb_ghost_cnt -= 1

    def _possible_position(self, agent: Agent):
        possibilities = []

        if type(self.board[agent.y - 1][agent.x]) == NoneBlock:
            possibilities.append(Agent.UP)
        if type(self.board[agent.y][agent.x - 1]) == NoneBlock:
            possibilities.append(Agent.LEFT)
        if type(self.board[agent.y + 1][agent.x]) == NoneBlock:
            possibilities.append(Agent.DOWN)
        if type(self.board[agent.y][agent.x + 1]) == NoneBlock:
            possibilities.append(Agent.RIGHT)

        return possibilities

    def _is_player_under_attack(self):
        for ghost in self.ghosts:
            if self.player.get_position() == ghost.get_position():
                return True

        for b_ghost in self.bomber_ghosts:
            if self.player.get_position() == b_ghost.get_position():
                return True

        for fire in self.fire:
            for x, y in fire.area:
                if self.player.get_position() == (x, y):
                    return True

        return False

    def _print(self):
        os.system("cls")

        print(f"\nLIFES: {self.player.lifes}")
        print(f"SCORE: {self.score} \n")

        for ghost in self.ghosts:
            self.board[ghost.y][ghost.x].change_representation \
                (ghost.get_representation(), ghost.get_color())

        for b_ghost in self.bomber_ghosts:
            self.board[b_ghost.y][b_ghost.x].change_representation \
                (b_ghost.get_representation(), b_ghost.get_color())

        for bomb in self.bombs:
            self.board[bomb.y][bomb.x].change_representation \
                (bomb.get_representation(), bomb.get_color())

        self.board[self.player.y][self.player.x].change_representation \
            (self.player.get_representation(), self.player.get_color())

        for fire in self.fire:
            for x, y in fire.area:
                self.board[y][x].change_representation \
                    (fire.get_representation(), fire.get_color())
            self.fire.remove(fire)

        for col in range(self.width):
            print(*self.board[col])

    def _new_bomb(self, agent:Agent):
        bomb = agent.put_bomb()
        if bomb:
            self.bombs.append(bomb)

    def _player_move(self):
        dec = str(input("Input: "))

        player_acceptable_moves = self._possible_position(self.player)
        if Agent.UP in player_acceptable_moves and dec == "w":
            self.player.move(MainPlayer.UP)
        elif Agent.LEFT in player_acceptable_moves and dec == "a":
            self.player.move(MainPlayer.LEFT)
        elif Agent.DOWN in player_acceptable_moves and dec == "s":
            self.player.move(MainPlayer.DOWN)
        elif Agent.RIGHT in player_acceptable_moves and dec == "d":
            self.player.move(MainPlayer.RIGHT)
        elif dec == "b":
            self._new_bomb(self.player)

        place = self.board[self.player.y][self.player.x]
        if place.is_powerup:
            place.is_powerup = False
            self.player.get_powerup(place.powerup)
            place.powerup = False

    def _clean_up(self):
        for col in range(self.width):
            for row in range(self.high):
                self.board[col][row].original_representation()

    def _ghost_under_attack(self):
        for fire in self.fire:
            for x, y in fire.area:

                for ghost in self.ghosts:
                    if ghost.get_position() == (x, y):
                        self.ghosts.remove(ghost)
                        self.score += 7

                for b_ghost in self.bomber_ghosts:
                    if b_ghost.get_position() == (x, y):
                        self.bomber_ghosts.remove(b_ghost)
                        self.score += 9

    def _ghost_moves(self):
        for ghost in self.ghosts:
            accept_moves = self._possible_position(ghost)
            ghost.random_move(accept_moves)

        for b_ghost in self.bomber_ghosts:
            accept_moves = self._possible_position(b_ghost)
            if randint(0, 20) == 5:
                self._new_bomb(b_ghost)
            else:
                b_ghost.random_move(accept_moves)

    def _create_fire(self, bomb):
        x, y = bomb.get_position()
        fire_places = [(x, y)]
        # UP
        for i in range(1, bomb.size+1):
            if type(self.board[y - i][x]) != ObsidianBlock:
                fire_places.append((x, y - i))
            if type(self.board[y - i][x]) != NoneBlock:
                break
        #LEFT
        for i in range(1, bomb.size+1):
            if type(self.board[y][x - i]) != ObsidianBlock:
                fire_places.append((x - i, y))
            if type(self.board[y][x - i]) != NoneBlock:
                break

        #RIGHT
        for i in range(1, bomb.size+1):
            if type(self.board[y][x + i]) != ObsidianBlock:
                fire_places.append((x + i, y))
            if type(self.board[y][x + i]) != NoneBlock:
                break

        #DOWN
        for i in range(1, bomb.size+1):
            if type(self.board[y + i][x]) != ObsidianBlock:
                fire_places.append((x, y + i))
            if type(self.board[y + i][x]) != NoneBlock:
                break
        print(fire_places)
        self.fire.append(Fire(fire_places))

    def _fire_step(self):
        for fire in self.fire:
            for x,y in fire.area:
                if type(self.board[y][x]) != NoneBlock:
                    self.board[y][x].life -= 1
                    if self.board[y][x].life == 0:
                        self.score += self.board[y][x].get_point()
                        if randint(1, 15) < 5 and self.power_ups:
                            self.board[y][x] = NoneBlock(True)
                            power = choice(self.power_ups)
                            self.power_ups.remove(power)
                            self.board[y][x].powerup = power

                        else:
                            self.board[y][x] = NoneBlock(False)

    def _bombs_move(self):

        for bomb in self.bombs:
            if bomb.tick():
                bomb.owner.bombs += 1
                self._create_fire(bomb)
                self.bombs.remove(bomb)

    def play(self):
        self._init_board()
        while True:

            self._print()
            self._clean_up()

            self._ghost_moves()
            self._player_move()
            self._bombs_move()
            self._fire_step()
            self._ghost_under_attack()

            if self._is_player_under_attack():
                self.player.lifes -= 1
                if self.player.lifes <= 0:
                    os.system("cls")
                    return self.score
