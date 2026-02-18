from copy import deepcopy
import pygame
from checkers.constants import BLACK, RED, WHITE
from checkers.board import Board

def minimax(position, depth, alpha, beta, max_player, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax(move, depth-1, alpha, beta, False, game)[0]
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if maxEval == evaluation:
                best_move = move
            if beta <= alpha: # Tämä on se taika: katkaistaan turha laskenta
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, alpha, beta, True, game)[0]
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if minEval == evaluation:
                best_move = move
            if beta <= alpha: # Tämä on se taika: katkaistaan turha laskenta
                break
        return minEval, best_move

def simulate_move(piece, move, board, skip):
    """Suorittaa siirron ja poistaa syödyt nappulat"""
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

def get_all_moves(board, color, game):
    moves = []
    all_valid_moves = {}
    
   # 1. Kerätään ensin KAIKKI mahdolliset siirrot kaikille nappuloille
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        if valid_moves:
            all_valid_moves[piece] = valid_moves

    # 2. Tarkistetaan, onko millään nappulalla syöntimahdollisuutta (skipped > 0)
    has_any_jump = False
    for piece, moves_dict in all_valid_moves.items():
        if any(len(skipped) > 0 for skipped in moves_dict.values()):
            has_any_jump = True
            break

    # 3. Luodaan uudet laudat
    for piece, moves_dict in all_valid_moves.items():
        for move, skip in moves_dict.items():
            # Jos jollain on hyppy, jätetään tavalliset siirrot (len(skip) == 0) huomiotta
            if has_any_jump and len(skip) == 0:
                continue
                
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)
    
    return moves