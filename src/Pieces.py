import pygame
import random

from src.config import Config


class Chesspiece:
    def __init__(self, display):
        self.xpos = 0
        self.ypos = 0
        self.score = 0
        self.name = 'Piece'
        self.white_team = True
        self.is_live = True
        self.has_moved = False
        self.grabbed = False
        self.grab_offset_x = 0
        self.grab_offset_y = 0
        self.movement_vectors = [[1,1]]
        self.range = 1

        self.display = display
        self.font = pygame.font.SysFont(Config['game']['font'], Config['game']['fontsize'])
        self.image = pygame.image.load("D:\Coding\Chess AI\src\pieces.png")
        self.image = pygame.transform.scale(self.image,
                                            (
                                                int(Config['playarea']['width']/Config['playarea']['squares']*6),
                                                int(Config['playarea']['height']/Config['playarea']['squares']*2)
                                            ) )
        self.area = pygame.Rect(0,0,63,63)


    def draw(self, board):
        if self.is_live:
            drawx = board.xpos + self.xpos*board.squarewidth
            drawy = board.ypos + self.ypos*board.squareheight
        else:
            drawx = self.xpos
            drawy = self.ypos

        #textsurface = self.font.render(self.name, False, Config['colors']['red'])
        #self.display.blit(textsurface, (drawx, drawy))

        self.display.blit(self.image, (drawx, drawy), area=self.area)



    def move(self, all_pieces, xpos_new, ypos_new):

        x_change = self.xpos - xpos_new
        y_change = self.ypos - ypos_new

        # check if valid move for the piece
        if self.is_valid_move(all_pieces, xpos_new, ypos_new):

            # check if the new space is occupied
            for p in all_pieces:
                if p.xpos == xpos_new and p.ypos == ypos_new:
                    if p.white_team != self.white_team:
                        p.get_taken()

            # complete the move
            print("{} from ({},{}) to ({},{})".format(self.name, self.xpos, self.ypos, xpos_new, ypos_new))
            self.xpos = xpos_new
            self.ypos = ypos_new
            self.has_moved = True

            return 'Successful move'


    def get_taken(self):
        self.is_live = False
        self.y_pos = 10
        if self.white_team == True:
            self.x_pos = 10
        else:
            self.x_pos = 700


    def is_valid_move(self, all_pieces, xpos_new, ypos_new):

        x_change = xpos_new - self.xpos
        y_change = ypos_new - self.ypos

        # Can't not move
        if x_change == 0 and y_change == 0:
            return False

        # check if the new space is on the board
        if xpos_new < 0 or xpos_new >= Config['playarea']['squares']:
            return False
        if ypos_new < 0 or ypos_new >= Config['playarea']['squares']:
            return False

        # check if the new space is occupied
        for p in all_pieces:
            if p.is_live:
                if p.xpos == xpos_new and p.ypos == ypos_new:
                    # If same team then we can't do this
                    if p.white_team == self.white_team:
                        return False
                    # If the king then we can't do this
                    elif p.name == 'King':
                        return False

        # check if space en route to the destination is occupied (except for Knight)
        if self.name != 'Knight':
            if abs(x_change) > 1 or abs(y_change) > 1:
                # traverse in the direction until we find another piece
                x_unit = 0
                y_unit = 0

                if x_change > 0:
                    x_unit = 1
                elif x_change < 0:
                    x_unit = -1

                if y_change > 0:
                    y_unit = 1
                elif y_change < 0:
                    y_unit = -1

                # check intermediate positions up to the max range
                max_dist = max(abs(x_change), abs(y_change))
                occ_x = -1
                occ_y = -1
                for i in range(1, max_dist):
                    for p in all_pieces:
                        if p.is_live and p.xpos == self.xpos+i*x_unit and p.ypos == self.ypos+i*y_unit:
                            occ_x = p.xpos
                            occ_y = p.ypos
                            break

                if occ_x != -1:
                    if abs(occ_x - self.xpos) < abs(x_change):
                        return False
                    if abs(occ_y - self.ypos) < abs(y_change):
                        return False

        # can't move and leave the king in check

        return True


    # List out the moves that this piece could make
    def get_valid_moves(self, all_pieces):
        valid_moves = []
        for i in range(Config['playarea']['squares']):
            for j in range(Config['playarea']['squares']):
                if self.is_valid_move(all_pieces, i, j):
                    valid_moves.append([i,j])

        if valid_moves == []:
            return

        return valid_moves

    # list out any pieces from the opposing team that this piece is threatening
    def get_threatened_pieces(self, all_pieces):
        threatened_pieces = []
        moves = self.get_valid_moves(all_pieces)
        if moves is None:
            return None

        for m in moves:
            for p in all_pieces:
                if p.is_live and p.white_team != p.white_team:
                    if p.xpos == m[0] and p.ypos == m[1]:
                        threatened_pieces.append(p)
        if threatened_pieces == []:
            return None
        return threatened_pieces

        return valid_moves


    # list out any squares that this piece could threaten from current position
    def get_threatened_squares(self):
        squares = []
        for r in range(self.range):
            for v in self.movement_vectors:
                new_pos = [self.xpos + (r+1)*v[0], self.ypos + (r+1)*v[1]]
                if new_pos[0] >= 0 and new_pos[0] < 8 and new_pos[1] >= 0 and new_pos[1] < 8:
                    squares.append(new_pos)

        if squares == []:
            return None

        return squares


class King(Chesspiece):
    def __init__(self, display, white_team, copy=0):
        Chesspiece.__init__(self, display)
        self.name = 'King'
        self.white_team = white_team
        self.movement_vectors = [ [1,1], #Up-right
                                  [1,0], #Right
                                  [1,-1],#Down-right
                                  [0,1],#Up
                                  [-1,0],#Left
                                  [-1,-1],#Down-Left
                                  [0,-1],#Down
                                  [-1,1] #Up-left
                                  ]

        # Set space on board
        self.xpos = 4
        if white_team == True:
            # Put at bottom of board
            self.ypos = 7
            # Set area of image file to use
            self.area = pygame.Rect(63*5,0,63,63)
        else:
            # Put at top of board
            self.ypos = 0
            # Set area of image file to use
            self.area = pygame.Rect(0,63,63,126)


    def is_valid_move(self, all_pieces, xpos_new, ypos_new):
        x_change = xpos_new - self.xpos
        y_change = ypos_new - self.ypos

        change = [x_change, y_change]
        if change not in self.movement_vectors:
            return False

        # king can't move self into check
        for p in all_pieces:
            if p.is_live and p.white_team != self.white_team:
                squares = p.get_threatened_squares()
                if squares is not None:
                    for m in squares:
                        if xpos_new == m[0] and ypos_new == m[1]:
                            return False

        return super().is_valid_move(all_pieces, xpos_new, ypos_new)



class Queen(Chesspiece):
    def __init__(self, display, white_team, copy=0):
        Chesspiece.__init__(self, display)
        self.name = 'Queen'
        self.white_team = white_team
        self.xpos = 3
        self.range = 8
        self.movement_vectors = [ [1,1], #Up-right
                                  [1,0], #Right
                                  [1,-1],#Down-right
                                  [0,1],#Up
                                  [-1,0],#Left
                                  [-1,-1],#Down-Left
                                  [0,-1],#Down
                                  [-1,1]#Up-left
                                  ]
        if white_team == True:
            self.ypos = 7
            # Set area of image file to use
            self.area = pygame.Rect(63*4,0,63,63)
        else:
            self.ypos = 0
            # Set area of image file to use
            self.area = pygame.Rect(63,63,63,63)


    def is_valid_move(self, all_pieces, xpos_new, ypos_new):
        x_change = self.xpos - xpos_new
        y_change = self.ypos - ypos_new
        # if we're not moving horizontal or vertical
        if x_change != 0 and y_change != 0:
            # and if we're not moving diagonal
            if abs(x_change) != abs(y_change):
                return False

        return super().is_valid_move(all_pieces, xpos_new, ypos_new)


class Bishop(Chesspiece):
    def __init__(self, display, white_team, copy=0):
        Chesspiece.__init__(self, display)
        self.name = 'Bishop'
        self.white_team = white_team
        self.xpos = 2
        self.range = 8
        self.movement_vectors = [ [1,1], #Up-right
                                  [1,-1],#Down-right
                                  [-1,-1],#Down-Left
                                  [-1,1] #Up-left
                                  ]
        if white_team == True:
            self.ypos = 7
            # Set area of image file to use
            self.area = pygame.Rect(63*3,0,63,63)
        else:
            self.ypos = 0
            # Set area of image file to use
            self.area = pygame.Rect(63*2,63,63,63)
        if copy == 1:
            self.xpos = 5

    def is_valid_move(self, all_pieces, xpos_new, ypos_new):
        x_change = self.xpos - xpos_new
        y_change = self.ypos - ypos_new
        # if we're not moving diagonal
        if abs(x_change) != abs(y_change):
            return False

        return super().is_valid_move(all_pieces, xpos_new, ypos_new)


class Knight(Chesspiece):
    def __init__(self, display, white_team, copy=0):
        Chesspiece.__init__(self, display)
        self.name = 'Knight'
        self.white_team = white_team
        self.xpos = 1
        self.movement_vectors = [[2, -1],
                                 [2, 1],
                                 [-2, -1],
                                 [-2, 1],
                                 [1, 2],
                                 [1, -2],
                                 [-1, 2],
                                 [-1, -2]
                                 ]
        if white_team == True:
            self.ypos = 7
            # Set area of image file to use
            self.area = pygame.Rect(63*2,0,63,63)
        else:
            self.ypos = 0
            # Set area of image file to use
            self.area = pygame.Rect(63*3,63,63,63)
        if copy == 1:
            self.xpos = 6


    def is_valid_move(self, all_pieces, xpos_new, ypos_new):

        if super().is_valid_move(all_pieces, xpos_new, ypos_new) != True:
            return False

        # need to move in an L shape
        change = [xpos_new - self.xpos, ypos_new - self.ypos]
        if change not in self.movement_vectors:
            return False

class Rook(Chesspiece):
    def __init__(self, display, white_team, copy=0):
        Chesspiece.__init__(self, display)
        self.name = 'Rook'
        self.white_team = white_team
        self.xpos = 0
        self.range = 8
        self.movement_vectors = [ [1,0], #Right
                                  [0,1],#Up
                                  [-1,0],#Left
                                  [0,-1]#Down
                                  ]
        if white_team == True:
            self.ypos = 7
            # Set area of image file to use
            self.area = pygame.Rect(63,0,63,63)
        else:
            self.ypos = 0
            # Set area of image file to use
            self.area = pygame.Rect(63*4,63,63,63)
        if copy == 1:
            self.xpos = 7


    def is_valid_move(self, all_pieces, xpos_new, ypos_new):
        x_change = self.xpos - xpos_new
        y_change = self.ypos - ypos_new
        # if we're not moving horizontal or vertical
        if abs(x_change) > 0  and abs(y_change) > 0:
            return False

        return super().is_valid_move(all_pieces, xpos_new, ypos_new)


class Pawn(Chesspiece):
    def __init__(self, display, white_team, copy=0):
        Chesspiece.__init__(self, display)
        self.name = 'Pawn'
        self.white_team = white_team
        self.xpos = copy
        self.range = 2

        if white_team == True:
            self.movement_vectors = [[1, -1],  # Down-right
                                     [-1, -1],  # Down-Left
                                     [0, -1]  # Down
                                     ]
            self.ypos = 6
            # Set area of image file to use
            self.area = pygame.Rect(0,0,63,63)
        else:
            self.movement_vectors = [[1, 1],  # Up-right
                                     [-1, 1],  # Up-Left
                                     [0, 1]  # Up
                                     ]
            self.ypos = 1
            # Set area of image file to use
            self.area = pygame.Rect(63*5,63,63,63)


    def is_valid_move(self, all_pieces, xpos_new, ypos_new):
        x_change = xpos_new - self.xpos
        y_change = ypos_new - self.ypos

        if super().is_valid_move(all_pieces, xpos_new, ypos_new) == False:
            return False

        # See if the new spot is occupied as pawns work a little differently
        occupied = False
        for p in all_pieces:
            if p.xpos == xpos_new and p.ypos == ypos_new:
                occupied = True

        if occupied == False:
            # if first go, can move 2 spaces
            if self.has_moved == False and abs(y_change) == 2 and x_change == 0:
                return True

            if self.white_team and x_change == 0 and y_change == -1:
                return True

            if self.white_team == False and x_change == 0 and y_change == 1:
                return True
        else:
            # can only move diagonal if capturing a piece
            if abs(x_change) == 1:
                if self.white_team and y_change == -1:
                    return True
                elif self.white_team == False and y_change == 1:
                    return True

        return False