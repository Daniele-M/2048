import pygame as pg
import numpy as np
import random
from os import path

from settings import *


class Board:
    def __init__(self, game):
        self.game = game
        self.game_square = 4
        self.cellsize = int(WIDTH / self.game_square)
        self.game_over = False
        self.b = np.zeros((self.game_square, self.game_square))
        self.previus_move = np.zeros((self.game_square, self.game_square))
        self.score = 0
        self.rect_width = WIDTH/2 - 70
        self.score_rect = pg.Rect(20, 100, self.rect_width, 50)
        self.record_rect = pg.Rect(WIDTH/2 + 70 - 20, 100, self.rect_width, 50)

    def draw_UI(self):
        self.display("Score", 35, 20 + self.rect_width/2, 60)
        self.display("Record", 35, WIDTH/2 + 70 - 20 + self.rect_width/2, 60)
        pg.draw.rect(self.game.screen, UI_COLOR, self.score_rect, border_radius=15)
        pg.draw.rect(self.game.screen, UI_COLOR, self.record_rect, border_radius=15)
        self.display(str(self.score), 25,  self.score_rect.centerx, self.score_rect.centery)
        self.display(str(self.game.record), 25, self.record_rect.centerx, self.record_rect.centery)


    def draw_lines(self):
        n = self.game_square
        pg.draw.line(self.game.screen, LINE_COLOR, (0, MARGIN), (WIDTH, MARGIN), 5)
        #Orizzontal lines
        for i in range(1, n):
            pg.draw.line(self.game.screen, LINE_COLOR, (0, MARGIN + i * WIDTH/n), (WIDTH, MARGIN + i * WIDTH/n), 5)
        #Vertical lines
        for i in range(1, n):
            pg.draw.line(self.game.screen, LINE_COLOR, (i * WIDTH/n, MARGIN), (i * WIDTH/n, MARGIN + HEIGHT), 5)

    def display(self, text, font_size, x, y):
        # x,y of the center
        font = pg.font.SysFont('arial', max(15, font_size))
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(x, y))
        self.game.screen.blit(text_surface, text_rect)

    def draw_nums(self):
        for row in range(self.game_square):
            for col in range(self.game_square):
                if self.b[row][col] != 0:
                    value = int(self.b[row][col])
                    text = str(value)
                    position = (col * self.cellsize + 3, MARGIN + row * self.cellsize + 3)
                    rect = pg.Rect(position, (self.cellsize - 5, self.cellsize - 5))
                    pg.draw.rect(self.game.screen, COLORS[value], rect)
                    self.display(text, self.cellsize//5, rect.centerx, rect.centery)

    def move_cells(self, direction, board, original_board=True):
        temp = np.copy(board)
        moved = False
        skip = False

        for i in range(self.game_square):
            if direction in "leftright":
                vec = board[i, :]
                if direction == "right":
                    vec = vec[::-1]
            else:
                vec = board[:, i]
                if direction == "down":
                    vec = vec[::-1]
            for j in range(self.game_square):
                if vec[j] != 0:
                    temp_j = j
                    while temp_j > 0 and vec[temp_j-1] == 0:
                        temp_j -= 1
                        moved = True
                    if j != temp_j:
                        vec[temp_j] = vec[j]
                        vec[j] = 0

                    if not skip:
                        if temp_j > 0 and vec[temp_j-1] == vec[temp_j]:
                            vec[temp_j-1] *= 2
                            vec[temp_j] = 0
                            skip = True
                            moved = True
                            if original_board:
                                self.update_score(int(vec[temp_j-1]))
                    else:
                        skip = False

        if moved and original_board:
            self.previus_move = temp
            self.spawn_cells()
            moved = False
            self.check_game_over()

    def spawn_cells(self, num=1):
        free_cells = self.get_available_cells()
        if free_cells == []:
            self.game_over = True
        else:
            spawn_points = random.sample(free_cells, num)
            for cell in spawn_points:
                if random.uniform(0, 1) > 0.1:
            	    self.b[cell] = 2
                else:
                    self.b[cell] = 4


    def get_available_cells(self):
        index = []
        for row in range(self.game_square):
            for col in range(self.game_square):
                if self.b[row][col] == 0:
                    index.append((row, col))
        return index


    def move_back(self):
        self.b = self.previus_move

    def update_score(self, score):
        self.score += score

    def check_game_over(self):
        directions = ["left", "right", "up", "down"]
        copy = self.b.copy()
        for dir in directions:
            self.move_cells(dir, copy, original_board=False)
            v = copy != self.b
            if v.any():
                return
        self.game_over = True
