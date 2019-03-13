import pygame
import random
from src.config import Config
from src.Pieces import Chesspiece

class Board:
    def __init__(self, display, num_squares=8):
        self.xpos = Config['game']['width']*0.5 - Config['playarea']['width']*0.5
        self.ypos = Config['game']['height']*0.5 - Config['playarea']['height']*0.5
        self.squarewidth = Config['playarea']['width'] / num_squares
        self.squareheight = Config['playarea']['height'] / num_squares
        self.display = display
        self.num_squares = num_squares
        self.colours = [ Config['colors']['white'],
                         Config['colors']['black'] ]

    def draw(self):
        draw_x = self.xpos
        draw_y = self.ypos
        for j in range(self.num_squares):
            for i in range(self.num_squares):
                pygame.draw.rect(
                    self.display,
                    self.colours[divmod(i+j,2)[1]],
                    [
                        draw_x,
                        draw_y,
                        self.squarewidth,
                        self.squareheight
                    ]
                )
                draw_x += self.squarewidth
            draw_y += self.squareheight
            draw_x = self.xpos

    def get_occupied_sqaures(self, all_pieces):
        occ_squares = []
        for p in all_pieces:
            if p.is_live:
                occ_squares.append([p.xpos, p.ypos])



