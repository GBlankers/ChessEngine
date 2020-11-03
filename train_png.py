#!/usr/bin/python3
import chess.pgn

def main():
    # get from https://raw.githubusercontent.com/niklasf/python-chess/master/data/pgn/kasparov-deep-blue-1997.pgn
    pgn = open("data/kasparov-deep-blue-1997.pgn")
    running = True

    while running:
        pgn_game = chess.pgn.read_game(pgn)
        
        if pgn_game:
            board = pgn_game.board()

            for move in pgn_game.mainline_moves():
                print(board)
                print("###################")
                board.push(move)
        else:
            running = False


if __name__ == "__main__":
    main()
