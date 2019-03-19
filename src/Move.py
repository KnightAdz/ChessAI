import pygame
import random

from src.config import Config

# Class for holding stats about a move, for scoring
class Move:
    def __init__(self):
        self.valid = False
        self.take_piece = None
        self.score = 0


    def score(self):
        return 0