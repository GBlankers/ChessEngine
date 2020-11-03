import random
import chess


class SearchAgent(object):

    def __init__(self, time_limit=5):
        """Setup the Search Agent"""
        self.time_limit = time_limit
        self.name = "Chess Engine"
        self.author = "S. Vanneste"

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
