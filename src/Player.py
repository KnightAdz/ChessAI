import pygame
import random

from src.config import Config
from src.Pieces import Chesspiece
import pandas as pd

class Player:
    def __init__(self, is_white_team, is_AI):
        self.score = 0
        self.white_team = is_white_team
        self.AI = is_AI


    def take_turn(self, all_pieces):

        # build a list of possible moves this player can make
        move_data = pd.DataFrame(columns=['Move_piece', 'NewX', 'NewY', 'Take_piece'])

        for p in all_pieces:
            if p.white_team == self.white_team and p.is_live:
                p_valid_moves = p.get_valid_moves(all_pieces)
                if p_valid_moves:
                    for m in p_valid_moves:
                        take_piece = ""
                        if isinstance(m[2], Chesspiece):
                            take_piece = m[2].name
                        move_data = move_data.append( {'Move_piece': p,
                                                       'NewX': m[0],
                                                       'NewY': m[1],
                                                       'Take_piece': take_piece
                                                       }, ignore_index=True )

        # if no legal moves, we have lost
        num_moves = move_data.shape[0]
        if num_moves == 0:
            return 1

        # Calculate scoring for the moves
        move_data['Score'] = move_data.apply( lambda x: Config['piece_values'][x['Take_piece']], axis=1 )
        #Config['piece_values'][

        # randomise the moves
        move_data = move_data.sample(frac=1).reset_index(drop=True)

        if self.white_team == False:
            # But if there are non-zero scores
            if move_data['Score'].sum() > 0:
                # Sort by them and pick the highest
                move_data.sort_values(by='Score', inplace=True, ascending=False)
                move_data.reset_index(inplace=True)

        # Try to execute the move, and if it fails, move down the list until finding one that works, or return 1
        idx = 0
        while move_data.loc[idx, 'Move_piece'].move(all_pieces, move_data.loc[idx, 'NewX'], move_data.loc[idx, 'NewY']) != 'Successful move':
            idx += 1
            if idx >= move_data.shape[0]:
                return 1

        return 0


    def king_in_check(self, all_pieces):
        for p in all_pieces:
            if p.is_live and p.white_team == self.white_team:
                    # Check if King in check
                    if p.name == 'King':
                         return p.is_in_check(all_pieces)
        return False


    def score_move(self):
        return 0