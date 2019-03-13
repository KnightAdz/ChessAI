import pygame
import random

from src.config import Config


class Player:
    def __init__(self, is_white_team, is_AI):
        self.score = 0
        self.white_team = is_white_team
        self.AI = is_AI


    def take_turn(self, all_pieces):

        # build a list of possible moves this player can make
        legal_moves = []
        for p in all_pieces:
            if p.white_team == self.white_team and p.is_live:
                p_valid_moves = p.get_valid_moves(all_pieces)
                if p_valid_moves:
                    legal_moves.append( [p, p_valid_moves] )

        # if no legal moves, we have lost
        if legal_moves == []:
            return 0

        # if king is in check, only moves allowed are ones that get us out of check
        if self.king_in_check(all_pieces):
            x=0
            # need to evaluate which moves help to get out of check

            # movements by the king that don't also end up in check

            # movements by other pieces to block check

            # movements by other pieces to capture checking opponents

        # random piece
        idx = int(random.random()*len(legal_moves))
        # random move
        idx2 = int(random.random())*len(legal_moves[idx][1])
        # Make the move
        legal_moves[idx][0].move(all_pieces, legal_moves[idx][1][idx2][0], legal_moves[idx][1][idx2][1])

        return 1


    def king_in_check(self, all_pieces):
        for p in all_pieces:
            if p.is_live:
                # For pieces on the current team
                if p.white_team == self.white_team:
                    # Check whether they have opposing King in check
                    threatened = p.get_threatened_pieces(all_pieces)
                    if threatened is not None:
                        for t in threatened:
                            if t.name == 'King':
                                return True
        return False