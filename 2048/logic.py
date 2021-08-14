import pygame as pg
import numpy as np
import random

from settings import *


class Board:
    def __init__(self, game):
        self.game = game
        self.game_over = False
        self.b = np.zeros((GAME_SQUARE, GAME_SQUARE))
        self.font = pg.font.SysFont('arial', CELL_SIZE//5)
        self.previus_move = np.zeros((GAME_SQUARE, GAME_SQUARE))

    def draw_lines(self):
        n = GAME_SQUARE
        pg.draw.line(self.game.screen, LINE_COLOR, (0, MARGIN), (WIDTH, MARGIN), 5)
        #Orizzontal lines
        for i in range(1, n):
            pg.draw.line(self.game.screen, LINE_COLOR, (0, MARGIN + i * WIDTH/n), (WIDTH, MARGIN + i * WIDTH/n), 5)
        #Vertical lines
        for i in range(1, n):
            pg.draw.line(self.game.screen, LINE_COLOR, (i * WIDTH/n, MARGIN), (i * WIDTH/n, MARGIN + HEIGHT), 5)

    def display(self, text, rect):

        txt = self.font.render(text, True, BLACK)
        text_rect = txt.get_rect(center=(rect.centerx,rect.centery))
        self.game.screen.blit(txt, text_rect)

    def draw_nums(self):
        for row in range(GAME_SQUARE):
            for col in range(GAME_SQUARE):
                if self.b[row][col] != 0:
                    value = int(self.b[row][col])
                    text = str(value)
                    position = (col * CELL_SIZE + 3, MARGIN + row * CELL_SIZE + 3)
                    rect = pg.Rect(position, (CELL_SIZE - 5, CELL_SIZE - 5))
                    pg.draw.rect(self.game.screen, COLORS[value], rect)
                    self.display(text, rect)

    def move_cells(self, direction):
        temp = np.copy(self.b)
        moved = False
        skip = False

        for i in range(GAME_SQUARE):
            if direction in "leftright":
                vec = self.b[i, :]
                if direction == "right":
                    vec = vec[::-1]
            else:
                vec = self.b[:, i]
                if direction == "down":
                    vec = vec[::-1]
            for j in range(GAME_SQUARE):
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
                    else:
                        skip = False



        if moved:
            self.previus_move = temp
            self.spawn_cells()
            moved = False

    def spawn_cells(self, num=1):
        free_cells = self.get_available_cells()
        if free_cells == []:
            self.end_game()
        else:
            spawn_points = random.sample(free_cells, num)
            for cell in spawn_points:
                if random.uniform(0, 1) > 0.1:
            	    self.b[cell] = 2
                else:
                    self.b[cell] = 4


    def get_available_cells(self):
        index = []
        for row in range(GAME_SQUARE):
            for col in range(GAME_SQUARE):
                if self.b[row][col] == 0:
                    index.append((row, col))
        return index

    def end_game(self):
        self.game_over = True

    def move_back(self):
        self.b = self.previus_move
