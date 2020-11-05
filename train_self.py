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
            move = white_player.minmax(board=board)
            turn_white_player = False
            print("white")
            print(utility(board, 1))

        else:
            # move = black_player.random_move(board=board)
            move = black_player.random_with_first_level_search(board=board)
            turn_white_player = True
            print("Black")
            print(utility(board, 0))

        board.push(move)
        print(board)
        print("###########################")
        print(board.piece_at(chess.QUEEN))
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
