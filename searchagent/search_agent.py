import random
import chess
from data.openings import openings


class SearchAgent(object):

    def __init__(self, time_limit=5):
        """Setup the Search Agent"""
        self.time_limit = time_limit
        self.name = "Chess Engine"
        self.author = "Groep2"

        self.moves = -1
        self.openings = openings
        self.openingNumber = random.randint(0, len(self.openings)-1)

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

    def minmax(self, board: chess.Board, depth=5, player=1):
        moves = list(board.legal_moves)
        # Kopie van het bord zodat moves niet "echt" uitgevoerd worden
        workBoard = board
        bestMove = [None]

        # Moves vergelijken met de slechts mogelijke waarde
        minValue = float("-inf")
        maxValue = float("inf")

        if depth == 0 or len(moves) == 0:
            return utility(board), bestMove

        # Eigen speler => utility proberen maximaliseren
        if player:
            for move in moves:
                # Voer de huidige move uit op de kopie van het bord
                workBoard.push(move)

                util = self.minmax(workBoard, depth-1, not player)[0]
                # Indien de move een betere utility geeft
                if minValue < util:
                    bestMove = [move]
                    minValue = util
                # Indien de move dezelfde utility heeft
                elif minValue == util:
                    bestMove.append(move)
                # Undo de move
                workBoard.pop()

                return minValue, bestMove

        # Tegenstander => proberen de utitlity te minimaliseren
        else:
            for move in moves:
                workBoard.push(move)

                util = self.minmax(workBoard, depth - 1, not player)[0]

                if maxValue > util:
                    bestMove = [move]
                    maxValue = util
                elif maxValue == util:
                    bestMove.append(move)

                workBoard.pop()

                return maxValue, bestMove

    def minimax_alfa_beta(self, board: chess.Board, alfa=float('-inf'), beta=float('inf'), depth=5, player=1, root=True):
        moves = list(board.legal_moves)

        # Kopie van het bord zodat moves niet "echt" uitgevoerd worden
        workBoard = board
        bestMove = [None]

        # Moves vergelijken met de slechts mogelijke waarde
        minValue = float("-inf")
        maxValue = float("inf")

        # Bekende openings gebruiken als eerste moves
        if self.moves < len(self.openings[self.openingNumber])-1 and board.turn:
            self.moves = self.moves + 1
            return 0, chess.Move.from_uci(self.openings[self.openingNumber][self.moves])

        # Bereken utility als we een bepaalde diepte hebben bereikt of als er geen moves te maken vallen
        if depth == 0 or len(moves) == 0:
            return utility(workBoard), bestMove

        # Eigen speler => utility proberen maximaliseren
        if player:
            for move in moves:
                # Voer de huidige move uit op de kopie van het bord
                workBoard.push(move)

                # Bereken utility van de move
                util = self.minimax_alfa_beta(workBoard, alfa, beta, depth - 1, not player, root)[0]

                # Undo de move
                workBoard.pop()

                # Indien de move een betere utility geeft
                if minValue < util:
                    bestMove = [move]
                    minValue = util
                # Indien de move dezelfde utility heeft
                elif minValue == util:
                    bestMove.append(move)

                alfa = max([alfa, util])
                if alfa >= beta:
                    break

            return minValue, random.choice(bestMove)

        # Tegenstander => proberen de utitlity te minimaliseren
        else:
            for move in moves:

                workBoard.push(move)

                util = self.minimax_alfa_beta(workBoard, alfa, beta, depth - 1, not player, root)[0]

                if maxValue > util:
                    bestMove = [move]
                    maxValue = util
                elif maxValue == util:
                    bestMove.append(move)

                workBoard.pop()

                beta = min([beta, util])
                if alfa <= beta:
                    break

            return maxValue, random.choice(bestMove)


def utility(board: chess.Board):
    # https://www.chessprogramming.org/Evaluation

    if board.is_checkmate():
        if board.turn:
            return float('inf')
        else:
            return float('-inf')

    if board.is_stalemate():
        return 0

    return materialScore(board)

    # MS = materialScore(board)
    #
    # PS = pawnStructure(board)
    #
    # BC = boardControl(board)
    #
    # return MS - 0.5 * PS + 0.5 * BC


# Functions for utility
def boardControl(board: chess.Board):
    allPieces = [chess.PAWN, chess.ROOK, chess.QUEEN, chess.KING, chess.BISHOP, chess.KNIGHT]

    M = 0
    Macc = 0

    for x in allPieces:
        temp = list(board.pieces(x, True))
        for y in temp:
            if y > 15:
                M = M + 1

        temp = list(board.pieces(x, False))
        for y in temp:
            if y < 48:
                Macc = Macc + 1

    return M - Macc


def pawnStructure(board: chess.Board):
    playerPawn = list(board.pieces(chess.PAWN, True))
    enemyPawn = list(board.pieces(chess.PAWN, False))
    allPieces = [chess.PAWN, chess.ROOK, chess.QUEEN, chess.KING, chess.BISHOP, chess.KNIGHT]
    l_side = [8, 16, 24, 32, 40, 48]
    r_side = [15, 23, 31, 39, 47, 55]

    # Doubled
    D = 0
    Dacc = 0
    for x in playerPawn:
        if (x + 8 in playerPawn) or (x + 16 in playerPawn) or (x + 24 in playerPawn) or \
                (x + 32 in playerPawn) or (x + 40 in playerPawn):
            D = D + 1
    for x in enemyPawn:
        if (x + 8 in enemyPawn) or (x + 16 in enemyPawn) or (x + 24 in enemyPawn) or \
                (x + 32 in enemyPawn) or (x + 40 in enemyPawn):
            Dacc = Dacc + 1

    # Isolated
    I = 0
    Iacc = 0
    for x in playerPawn:
        isolated = True
        for y in allPieces:
            temp = list(board.pieces(y, True))
            if x in l_side:
                if (x + 8 in temp) or (x + 9 in temp) or (x + 1 in temp) or (x - 8 in temp) or (x - 7 in temp):
                    isolated = False
                    break
            elif x in r_side:
                if (x + 8 in temp) or (x + 7 in temp) or (x - 1 in temp) or (x - 8 in temp) or (x - 9 in temp):
                    isolated = False
                    break
            else:
                if (x - 9 in temp) or (x - 8 in temp) or (x - 7 in temp) or (x - 1 in temp) or (x + 1 in temp) or \
                        (x + 7 in temp) or (x + 8 in temp) or (x + 9 in temp):
                    isolated = False
                    break
        if isolated:
            I = I + 1

    for x in enemyPawn:
        isolated = True
        for y in allPieces:
            temp = list(board.pieces(y, False))
            if x in l_side:
                if (x + 8 in temp) or (x + 9 in temp) or (x + 1 in temp) or (x - 8 in temp) or (x - 7 in temp):
                    isolated = False
                    break
            elif x in r_side:
                if (x + 8 in temp) or (x + 7 in temp) or (x - 1 in temp) or (x - 8 in temp) or (x - 9 in temp):
                    isolated = False
                    break
            else:
                if (x - 9 in temp) or (x - 8 in temp) or (x - 7 in temp) or (x - 1 in temp) or (x + 1 in temp) or \
                        (x + 7 in temp) or (x + 8 in temp) or (x + 9 in temp):
                    isolated = False
                    break
        if isolated:
            Iacc = Iacc + 1

    # Blocked
    B = 0
    Bacc = 0

    for x in playerPawn:
        for y in allPieces:
            temp = list(board.pieces(y, False))
            if x + 8 in temp:
                B = B + 1
                break

    for x in enemyPawn:
        for y in allPieces:
            temp = list(board.pieces(y, True))
            if x - 8 in temp:
                Bacc = Bacc + 1
                break

    # Further pawns
    F = 0
    Facc = 0

    for x in playerPawn:
        F = F + x % 8

    for x in enemyPawn:
        Facc = Facc + x % 8

    return D - Dacc + I - Iacc + B - Bacc + 0.2 * (F - Facc)


def materialScore(board: chess.Board):
    # Number of pieces
    n = 200 * (len(board.pieces(chess.KING, True)) - len(board.pieces(chess.KING, False))) + \
        9 * (len(board.pieces(chess.QUEEN, True)) - len(board.pieces(chess.QUEEN, False))) + \
        5 * (len(board.pieces(chess.ROOK, True)) - len(board.pieces(chess.ROOK, False))) + \
        3 * (len(board.pieces(chess.BISHOP, True)) - len(board.pieces(chess.BISHOP, False)) +
             len(board.pieces(chess.KNIGHT, True)) - len(board.pieces(chess.KNIGHT, False))) + \
        (len(board.pieces(chess.PAWN, True)) - len(board.pieces(chess.PAWN, False)))

    return n
