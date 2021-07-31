import pygame as pg
import sys

from settings import *
from logic import *


class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.board = Board(self)
        self.direction = ""
        self.clock = pg.time.Clock()
        self.running = True


    def new(self):
        self.score = 0

        self.board.spawn_cells(2)

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    self.direction = "left"
                if event.key == pg.K_RIGHT:
                    self.direction = "right"
                if event.key == pg.K_UP:
                    self.direction = "up"
                if event.key == pg.K_DOWN:
                    self.direction = "down"
                if DEBUGGING:
                    if event.type == pg.KEYUP:
                        if event.key == pg.K_RETURN:
                            self.board.move_back()

    def update(self):
        if self.board.game_over:
            self.playing = False
            self.running = False
        if self.direction != "":
            self.board.move_cells(self.direction)
        self.direction  = ""

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.board.draw_lines()
        self.board.draw_nums()

        pg.display.flip()



g = Game()
while g.running:
    g.new()

sys.exit()
