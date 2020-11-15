#!/usr/bin/python3
import chess
import chess.engine
from searchagent.search_agent import SearchAgent
from searchagent.search_agent import utility


def main():
    board = chess.Board()
    white_player = SearchAgent(time_limit=5)
    black_player = chess.engine.SimpleEngine.popen_uci("stockfish")
    limit = chess.engine.Limit(time=5.0)

    running = True
    turn_white_player = True

    while running:
        move = None

        if turn_white_player:
            move = white_player.minimax_alfa_beta(board=board, alfa=float('-inf'), beta=float('inf'))[1]
            print(move)
            turn_white_player = False
            print("Engine")
        else:
            move = black_player.play(board, limit).move
            turn_white_player = True
            print("Stockfish")

        board.push(move)
        print("Utility: " + str(utility(board)))
        print(board)
        print("###########################")

        if board.is_checkmate():
            running = False

            if turn_white_player:
                print("Stockfish wins!")
            else:
                print("{} wins!".format(white_player.name))

        if board.is_stalemate():
            running = False
            print("Stalemate")

    black_player.quit()


if __name__ == "__main__":
    main()
