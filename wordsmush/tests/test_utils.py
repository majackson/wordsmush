from itertools import imap, cycle
from collections import Iterator

from wordsmush.game import WordsmushGame, WordsmushTile
from wordsmush.player import WordsmushPlayer

def get_alpha_board():
    """Test utility. Creates a 5x5 game populated with the letters a-z"""
    def _letter():
        for letter in imap(chr, cycle(xrange(ord('a'), ord('z')))):
            yield letter
    letters = _letter()

    return get_board(letters)
    

def get_board(letters):
    """Creates a board from a list of letters"""

    if not isinstance(letters, Iterator):
        letters = iter(letters)

    player1 = WordsmushPlayer() 
    player2 = WordsmushPlayer()
    game = WordsmushGame(player1, player2, board_width=5,
                board_height=5)

    board = ([[WordsmushTile(game, x, y, next(letters)) 
        for x in range(game.board_width)] for y in range(game.board_height)])

    game.board = board
    return game

