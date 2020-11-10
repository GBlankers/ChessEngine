import random
import chess


class SearchAgent(object):

    def __init__(self, time_limit=5):
        """Setup the Search Agent"""
        self.time_limit = time_limit
        self.name = "Chess Engine"
        self.author = "GB"
        self.depth = 5

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

    # Depth ook bij self.depth aanpassen voor juiste werking
    # TODO ALFA_BETA pruning
    def minmax(self, board: chess.Board, depth=5, player=1):
        moves = list(board.legal_moves)
        # Kopie van het bord zodat moves niet "echt" uitgevoerd worden
        workBoard = board
        bestMove = None

        # Moves vergelijken met de slechts mogelijke waarde
        minValue = float("-inf")
        maxValue = float("inf")

        if depth == 0 or len(moves) == 0:
            return utility(board, player)

        # Eigen speler => utility proberen maximaliseren
        if player:
            for move in moves:
                # Voer de huidige move uit op de kopie van het bord
                workBoard.push(move)
                util = self.minmax(workBoard, depth-1, not player)
                # Indien de move een betere utility geeft
                if minValue < util:
                    bestMove = [move]
                    minValue = util
                # Indien de move dezelfde utility heeft
                elif minValue == util:
                    bestMove.append(move)
                # Undo de move
                workBoard.pop()
        # Tegenstander => proberen de utitlity te minimaliseren
        else:
            for move in moves:
                workBoard.push(move)
                util = self.minmax(workBoard, depth - 1, not player)
                if maxValue > util:
                    bestMove = [move]
                    maxValue = util
                elif maxValue == util:
                    bestMove.append(move)
                workBoard.pop()

        # Return de beste move indien we in root zitten
        # Indien er meer mogelijke moves zijn dan zal er random 1 gekozen worden
        if depth == self.depth:
            return random.choice(bestMove)

        # Return de Utility indien we niet in root zitten
        if player:
            return minValue
        else:
            return maxValue

    def minimax_alfa_beta(self, board: chess.Board, alfa, beta, depth=5, player=1):
        moves = list(board.legal_moves)
        # Kopie van het bord zodat moves niet "echt" uitgevoerd worden
        workBoard = board
        bestMove = None

        # Moves vergelijken met de slechts mogelijke waarde
        minValue = float("-inf")
        maxValue = float("inf")

        if depth == 0 or len(moves) == 0:
            return utility(workBoard, player)

            # Eigen speler => utility proberen maximaliseren
        if player:
            for move in moves:
                # Voer de huidige move uit op de kopie van het bord
                workBoard.push(move)

                # Bereken utility van de move
                util = self.minimax_alfa_beta(workBoard, alfa, beta, depth - 1, not player)

                # Indien de move een betere utility geeft
                if minValue < util:
                    bestMove = [move]
                    minValue = util
                # Indien de move dezelfde utility heeft
                elif minValue == util:
                    bestMove.append(move)

                # Undo de move
                workBoard.pop()

                alfa = max([alfa, util])
                if alfa >= beta:
                    break

        # Tegenstander => proberen de utitlity te minimaliseren
        else:
            for move in moves:

                workBoard.push(move)

                util = self.minimax_alfa_beta(workBoard, alfa, beta, depth - 1, not player)

                if maxValue > util:
                    bestMove = [move]
                    maxValue = util
                elif maxValue == util:
                    bestMove.append(move)

                workBoard.pop()

                beta = min([beta, util])
                if alfa <= beta:
                    break

        # Return de beste move indien we in root zitten
        # Indien er meer mogelijke moves zijn dan zal er random 1 gekozen worden
        if depth == self.depth:
            return random.choice(bestMove)

        # Return de Utility indien we niet in root zitten
        if player:
            return minValue
        else:
            return maxValue



# TODO Implement mobility + blocked/isolated/doubled pawns
def utility(board: chess.Board, player):
    # https://www.chessprogramming.org/Evaluation

    if board.is_checkmate():
        if player:
            return 9999999
        else:
            return -9999999

    # Number of pieces
    n = 200 * (len(board.pieces(chess.KING, True)) - len(board.pieces(chess.KING, False))) +\
        9 * (len(board.pieces(chess.QUEEN, True)) - len(board.pieces(chess.QUEEN, False))) +\
        5 * (len(board.pieces(chess.ROOK, True)) - len(board.pieces(chess.ROOK, False))) +\
        3 * (len(board.pieces(chess.BISHOP, True)) - len(board.pieces(chess.BISHOP, False)) +
             len(board.pieces(chess.KNIGHT, True)) - len(board.pieces(chess.KNIGHT, False))) +\
        (len(board.pieces(chess.PAWN, True)) - len(board.pieces(chess.PAWN, False)))

    return n
