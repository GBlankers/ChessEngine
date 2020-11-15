#!/usr/bin/python3
import chess
from searchagent.search_agent import SearchAgent
from searchagent.search_agent import utility


def run_episode():
    board = chess.Board()
    white_player = SearchAgent(time_limit=5)
    white_player.name = "White Player"
    black_player = SearchAgent(time_limit=5)
    black_player.name = "Black Player"

    running = True
    turn_white_player = True
    counter = 0

    while running:
        counter += 1
        move = None

        if turn_white_player:
            move = white_player.minimax_alfa_beta(board=board, depth= 5, alfa=float('-inf'), beta=float('inf'))[1]
            turn_white_player = False
            print("white")
            print(utility(board))

        else:
            move = black_player.random_move(board=board)
            # move = black_player.minimax_alfa_beta(board=board, depth=4, player=0)[1]
            turn_white_player = True
            print("Black")
            print(utility(board))

        board.push(move)
        print(board)
        print("###########################")

        if board.is_checkmate():
            running = False

            if turn_white_player:
                print("{} wins!".format(black_player.name))
            else:
                print("{} wins!".format(white_player.name))

        if board.is_stalemate() or counter > 1000:
            running = False
            print("Stalemate")


def main():
    run_episode()


if __name__ == "__main__":
    main()
