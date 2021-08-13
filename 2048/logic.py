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
        if direction == "left":
            for row in range(GAME_SQUARE):
                for col in range(GAME_SQUARE):
                    if self.b[row][col] != 0:
                        temp_col = col
                        while temp_col - 1 >= 0 and self.b[row][temp_col-1] == 0:
                            self.b[row][temp_col-1] = self.b[row][temp_col]
                            self.b[row][temp_col] = 0
                            moved = True
                            temp_col -= 1
                        if temp_col != 0 and self.b[row][temp_col-1] == self.b[row][temp_col]:
                            self.b[row][temp_col-1] *= 2
                            self.b[row][temp_col] = 0
                            moved = True
        if direction == "right":
            for row in range(GAME_SQUARE):
                for col in range(GAME_SQUARE-1, -1, -1):
                    if self.b[row][col] != 0:
                        temp_col = col
                        while temp_col + 1 <= GAME_SQUARE - 1 and self.b[row][temp_col+1] == 0:
                            self.b[row][temp_col+1] = self.b[row][temp_col]
                            self.b[row][temp_col] = 0
                            moved = True
                            temp_col += 1
                        if temp_col != GAME_SQUARE - 1 and self.b[row][temp_col+1] == self.b[row][temp_col]:
                            self.b[row][temp_col+1] *= 2
                            self.b[row][temp_col] = 0
                            moved = True

        if direction == "up":
            for col in range(GAME_SQUARE):
                for row in range(GAME_SQUARE):
                    if self.b[row][col] != 0:
                        temp_row = row
                        while temp_row - 1 >= 0 and self.b[temp_row-1][col] == 0:
                            self.b[temp_row-1][col] = self.b[temp_row][col]
                            self.b[temp_row][col] = 0
                            moved = True
                            temp_row -= 1
                        if temp_row != 0 and self.b[temp_row-1][col] == self.b[temp_row][col]:
                            self.b[temp_row-1][col] *= 2
                            self.b[temp_row][col] = 0
                            moved = True
        if direction == "down":
            for col in range(GAME_SQUARE):
                for row in range(GAME_SQUARE-1, -1, -1):
                    if self.b[row][col] != 0:
                        temp_row = row
                        while temp_row + 1 <= GAME_SQUARE - 1 and self.b[temp_row+1][col] == 0:
                            self.b[temp_row+1][col] = self.b[temp_row][col]
                            self.b[temp_row][col] = 0
                            moved = True
                            temp_row += 1
                        if temp_row != GAME_SQUARE - 1 and self.b[temp_row+1][col] == self.b[temp_row][col]:
                            self.b[temp_row+1][col] *= 2
                            self.b[temp_row][col] = 0
                            moved = True

        if moved:
            self.previus_move = temp
            self.spawn_cells(1)
            moved = False

    def spawn_cells(self, num):
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
