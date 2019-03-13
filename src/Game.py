import pygame
import pandas as pd
import numpy as np
from src.Board import Board
from src.Pieces import Chesspiece
from src.Pieces import Pawn
from src.Pieces import King
from src.Pieces import Queen
from src.Pieces import Rook
from src.Pieces import Knight
from src.Pieces import Bishop
from src.config import Config
from src.Player import Player

class Game:
    def __init__(self, display):
        self.display = display
        self.in_play_piece = None

    def loop(self):
        clock = pygame.time.Clock()

        # Initial set up
        self.set_up_new_game()

        # Game loop
        while True:
            # Alternate control between the players
            self.active_player = self.players[divmod(self.turn_counter,2)[1]]

            # Check for the win condition: the king not having any valid moves and being threatened by one enemy piece
            king_no_moves, king_in_check = self.check_win_condition()

            # Calculate safe squares for the new player
#            occupied_squares = self.board.get_occupied_squares(self.pieces)

            if self.active_player.AI == False:
                # Check input events
                self.handle_input()
            else:
                # Compute move
                self.active_player.take_turn(self.pieces)
                self.turn_counter += 1

            # if both players are AI
            if self.players[0].AI and self.players[1].AI:
                # Be able to quit
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()


            # Refill whole screen with green
            self.display.fill(Config['colors']['green'])
            if king_no_moves or king_in_check:
                self.display.fill(Config['colors']['red'])
            # Draw the board
            self.board.draw()
            # Draw pieces on the board
            for p in self.pieces:
                p.draw(self.board)

            # update the display and increase the tick
            pygame.display.update()
            clock.tick(Config['game']['fps'])


    # Set up a new game
    def set_up_new_game(self):
        self.board = Board(self.display)
        self.pieces = []
        self.players = []

        # For two teams, white and black
        for t in [True,False]:
            # Create a lay out the pieces
            self.pieces.append(King(self.display, t))
            self.pieces.append(Queen(self.display, t))
            for p in range(8):
                self.pieces.append(Pawn(self.display, t, p))
                if p < 2:
                    self.pieces.append(Bishop(self.display,t,p))
                    self.pieces.append(Knight(self.display, t, p))
                    self.pieces.append(Rook(self.display, t, p))

            # Also create a player for the team
            self.players.append(Player(t,t))
            #self.players.append(Player(t, True))

        self.turn_counter = 0

    def handle_input(self):
        for event in pygame.event.get():
            # Be able to quit
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons = pygame.mouse.get_pressed()
                x, y = pygame.mouse.get_pos()

                # convert to the board square that was clicked
                x_square = int( (x - self.board.xpos)/self.board.squarewidth )
                y_square = int( (y - self.board.ypos)/self.board.squareheight )

                # if right mouse button then cancel move#
                if buttons[2] == 1:
                    print('Piece cancelled')
                    self.in_play_piece = None
                # if left mouse button then pick up the piece or put it down
                if buttons[0] == 1:
                    # if we don't have an in play piece
                    if self.in_play_piece is None:
                        # find piece on this square
                        for p in self.pieces:
                            dist = abs(p.xpos - x_square) + abs(p.ypos - y_square)
                            if dist < 1 and p.is_live and p.white_team == self.active_player.white_team:
                                self.in_play_piece = p
                                break
                    # Else try to move to this square
                    else:
                        res = self.in_play_piece.move(self.pieces, x_square, y_square)
                        if res == "Successful move":
                            self.turn_counter += 1
                        self.in_play_piece = None

            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                x = 0


    def check_win_condition(self):
        king_no_moves = False
        king_in_check = False

        active_team = self.active_player.white_team
        for p in self.pieces:
            if p.is_live:
                if p.white_team != active_team:
                    # If this is the opposing king
                    if p.name == 'King':
                        # check for moves
                        moves = p.get_valid_moves(self.pieces)
                        if moves is None:
                            king_no_moves = True

        king_in_check = self.active_player.king_in_check(self.pieces)

        return king_no_moves, king_in_check

