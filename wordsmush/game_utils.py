from itertools import imap, cycle
from collections import Iterator
from random import randint, choice

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

random_letter = lambda: chr(randint(ord('a'), ord('z')))

def random_letter_freq():
    """Gets a random letter, with the random choice weighted by frequency of
    use in the english language. Weights from http://en.wikipedia.org/wiki/Letter_frequency"""
    return choice(['a']*8 +
                  ['b']*1 +
                  ['c']*3 +
                  ['d']*4 +
                  ['e']*12 +
                  ['f']*2 +
                  ['g']*2 +
                  ['h']*6 +
                  ['i']*7 +
                  ['j']*1 +
                  ['k']*1 +
                  ['l']*4 +
                  ['m']*2 +
                  ['n']*7 +
                  ['o']*8 +
                  ['p']*2 +
                  ['q']*1 +
                  ['r']*6 +
                  ['s']*6 +
                  ['t']*9 +
                  ['u']*3 +
                  ['v']*1 +
                  ['w']*2 +
                  ['x']*1 +
                  ['y']*2 +
                  ['z']*1 ) 
