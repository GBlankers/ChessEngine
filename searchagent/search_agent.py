import random
import chess


class SearchAgent(object):

    def __init__(self, time_limit=5):
        """Setup the Search Agent"""
        self.time_limit = time_limit
        self.name = "Chess Engine"
        self.author = "GB"
        self.depth = 4

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

    def minmax(self, board: chess.Board, depth=4, player=1):
        moves = list(board.legal_moves)
        workBoard = board

        if depth == 0 or len(moves) == 0:
            return utility(board, player)

        if player:
            minValue = float("-inf")

            for move in moves:
                workBoard.push(move)
                temp = self.minmax(workBoard, depth-1, not player)
                if minValue < temp:
                    minValue = temp
                    bestMove = move
                workBoard.pop()
        else:
            maxValue = float("inf")

            for move in moves:
                workBoard.push(move)
                temp = self.minmax(workBoard, depth - 1, not player)
                if maxValue > temp:
                    maxValue = temp
                    bestMove = move
                workBoard.pop()

        if depth == self.depth:
            return bestMove

        if player:
            return minValue
        else:
            return maxValue


def utility(board: chess.Board, player):
    # https://www.chessprogramming.org/Evaluation

    if board.is_checkmate():
        if player:
            return 99999
        else:
            return -99999

    f = 200 * (len(board.pieces(chess.KING, True)) - len(board.pieces(chess.KING, False))) +\
        9 * (len(board.pieces(chess.QUEEN, True)) - len(board.pieces(chess.QUEEN, False))) +\
        5 * (len(board.pieces(chess.ROOK, True)) - len(board.pieces(chess.ROOK, False))) +\
        3 * (len(board.pieces(chess.BISHOP, True)) - len(board.pieces(chess.BISHOP, False)) +
             len(board.pieces(chess.KNIGHT, True)) - len(board.pieces(chess.KNIGHT, False))) +\
        (len(board.pieces(chess.PAWN, True)) - len(board.pieces(chess.PAWN, False)))

    return f
