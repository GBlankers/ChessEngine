import random
import chess
from . import util


class SearchAgent(object):

    def __init__(self, time_limit=5):
        """Setup the Search Agent"""
        self.time_limit = time_limit
        self.name = "Chess Engine"

    def random_move(self, board: chess.Board):
        return random.sample(list(board.legal_moves), 1)[0]

    def random_with_first_level_search(self, board: chess.Board):
        moves = list(board.legal_moves)

        best_move = random.sample(moves, 1)[0]
        best_move_value = 0

        for move in moves:
            board.push(move)
            if board.is_checkmate():
                move_value = 100
                if move_value > best_move_value:
                    best_move = move
            board.pop()

            if board.is_into_check(move):
                move_value = 90
                if move_value > best_move_value:
                    best_move = move

            if board.is_capture(move):
                move_value = 80
                if move_value > best_move_value:
                    best_move = move

            if board.is_castling(move):
                move_value = 70
                if move_value > best_move_value:
                    best_move = move

        return best_move

    def minmax(self, board: chess.Board, depth=2):
        moves = list(board.legal_moves)
        moveUtility = util.Counter()

        for move in moves:
            moveUtility[move] = minmize(board, depth-1)
        return moveUtility.argMax()


def minmize(board: chess.Board, depth):

    # Indien we op max diepte zitten, returnen we de utility waarde van deze board state
    if depth == 0:
        return utility(board)

    moveUtility = util.Counter()
    for Nmove in board.legal_moves:
        workBoard = board
        workBoard.push(Nmove)
        moveUtility[Nmove] = maximize(workBoard, depth-1)
        workBoard.pop()

    return moveUtility[moveUtility.argMin()]


def maximize(board: chess.Board, depth):
    # Indien we op max diepte zitten, returnen we de utility waarde van deze board state
    if depth == 0:
        return utility(board)

    moveUtility = util.Counter()
    for Nmove in board.legal_moves:
        workBoard = board
        workBoard.push(Nmove)
        moveUtility[Nmove] = maximize(workBoard, depth - 1)
        workBoard.pop()

    return moveUtility[moveUtility.argMax()]


def utility(board: chess.Board):
    # https://www.chessprogramming.org/Evaluation

    f = 200 * (len(board.pieces(chess.KING, True)) - len(board.pieces(chess.KING, False))) +\
        9 * (len(board.pieces(chess.QUEEN, True)) - len(board.pieces(chess.QUEEN, False))) +\
        5 * (len(board.pieces(chess.ROOK, True)) - len(board.pieces(chess.ROOK, False))) +\
        3 * (len(board.pieces(chess.BISHOP, True)) - len(board.pieces(chess.BISHOP, False)) +
             len(board.pieces(chess.KNIGHT, True)) - len(board.pieces(chess.KNIGHT, False))) +\
        (len(board.pieces(chess.PAWN, True)) - len(board.pieces(chess.PAWN, False)))

    return f
