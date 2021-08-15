import pygame as pg
import sys
from os import path

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
        self.load_HS()

    def load_HS(self):
        file = path.join(path.dirname(__file__), 'highscore.txt')
        if not path.exists(file):
            with open(file, 'w') as f:
                f.writelines(["0\n" for _ in range(15)])
        with open(file, "r+") as f:
            self.highscores = f.readlines()


    def new(self):
        if self.running:
            self.board.score = 0
            self.board.game_over = False
            self.board.cellsize = int(WIDTH / self.board.game_square)
            self.board.b = np.zeros((self.board.game_square, self.board.game_square))
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
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.direction = "left"
                if event.key == pg.K_RIGHT:
                    self.direction = "right"
                if event.key == pg.K_UP:
                    self.direction = "up"
                if event.key == pg.K_DOWN:
                    self.direction = "down"
                if DEBUGGING:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_q:
                            self.board.move_back()

    def update(self):
        if self.board.game_over:
            self.playing = False
        if self.direction != "":
            self.board.move_cells(self.direction, self.board.b)
        self.direction  = ""

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.board.draw_lines()
        self.board.draw_nums()
        self.board.draw_UI()

        pg.display.flip()

    def game_over_screen(self):
        if not self.running:
            return
        self.screen.fill(BG_COLOR)
        self.board.display("GAME OVER!", 50, WIDTH/2, HEIGHT/4)
        if self.board.score > self.record:
            self.record = self.board.score
            self.highscores[self.board.game_square-2] = f"{self.board.score}\n"
            self.board.display("NEW RECORD: " + str(self.board.score), 40, WIDTH/2, HEIGHT*3/4)
            with open(path.join(path.dirname(__file__), "highscore.txt"), 'w') as f:
                f.writelines(self.highscores)
        else:
            self.board.display("SCORE: " + str(self.board.score), 40, WIDTH/2, HEIGHT*3/4)

        self.board.display("HIGHSCORE: " + str(self.record), 40, WIDTH/2, HEIGHT*3/4 + 50)
        self.board.display("PRESS ENTER TO CONTINUE", 30, WIDTH/2, HEIGHT/2)

        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_RETURN:
                        waiting = False

    def options_screen(self):
        selected = False
        while not selected:
            self.screen.fill(BG_COLOR)
            self.board.display("CHOOSE THE BOARD DIMENSIONS", 25, WIDTH/2, HEIGHT/4)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    selected = True
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT and self.board.game_square > 2:
                        self.board.game_square -= 1
                    elif event.key == pg.K_RIGHT and self.board.game_square < 16:
                        self.board.game_square += 1
                    elif event.key == pg.K_RETURN:
                        selected = True
            self.record = int((self.highscores[self.board.game_square-2]).strip("\n"))
            self.board.display("RECORD: " + str(self.record), 30, WIDTH/2, HEIGHT/2)
            self.board.display(f"{str(self.board.game_square)}X{str(self.board.game_square)}", 25, WIDTH/2, HEIGHT*3/4)
            pg.display.flip()

g = Game()
while g.running:
    g.options_screen()
    g.new()
    g.game_over_screen()

sys.exit()
