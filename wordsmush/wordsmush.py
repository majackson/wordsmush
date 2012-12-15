from random import randint
from operator import add

from colorama import Fore, Back, Style

from wordsmush.word_lookup import words


# tile statuses
UNTAKEN = 0
TAKEN_PLAYER1 = 1
TAKEN_PLAYER2 = 2
PROTECTED_PLAYER1 = 3
PROTECTED_PLAYER2 = 4

class WordsmushGame(object):

    def __init__(self, player1, player2, board_width=5, board_height=5):

        self.player1 = player1
        self.player2 = player2

        random_letter = lambda: chr(randint(ord('a'), ord('z')))
        self.board = [[ (random_letter(), UNTAKEN) for n in range(board_width) ] 
                            for m in range(board_height) ] 
        self.letters = [letter for letter, status in reduce(add, self.board)]

    def __repr__(self):
        return self.format_pretty()

    def format_pretty(self):
        COLOR_MAPPING = {
            UNTAKEN: Fore.BLACK + Back.WHITE + Style.NORMAL,
            TAKEN_PLAYER1: Fore.CYAN + Back.BLUE + Style.DIM, 
            TAKEN_PLAYER2: Fore.RED + Back.YELLOW + Style.DIM,
            PROTECTED_PLAYER1: Fore.BLUE + Back.BLUE + Style.BRIGHT,
            PROTECTED_PLAYER2: Fore.RED + Back.RED + Style.BRIGHT,
        }

        format_string = ''
        for tile_row in self.board:
            for tile, status in tile_row:
                format_string += COLOR_MAPPING[status] + (' %s ' % tile.upper())
            format_string += Fore.RESET + Back.RESET + Style.RESET_ALL + '\n'

        return format_string

    def play(self, player, word):

        taken_status = {self.player1: TAKEN_PLAYER1,
                        self.player2: TAKEN_PLAYER2}

        protected_status = {self.player1: PROTECTED_PLAYER1,
                            self.player2: PROTECTED_PLAYER2}

        if self.is_a_word(word): 

            # give possession of each new letter to player, 
            # if the tiles are unprotected
            for tile_x, tile_y, letter in word.tiles:
                letter, status = self.board[tile_y][tile_x]
                if status not in (PROTECTED_PLAYER1, PROTECTED_PLAYER2):
                    self.board[tile_y][tile_x] = (letter, taken_status[player]) 


            # now recalculate protected status of all tiles
            # TODO
                

    def is_a_word(self, word):
        return word.word in words

class WordsmushWord(object):
    
    def __init__(self, game, tiles=[]):
        self.game = game
        self.tiles = tiles

    def add_tile(self, tile, position=None):
        """Add a tile to the word, optionally with a specific position.
        This method may also be move a tile already in play. """

        if tile in self.tiles:
            self.tiles.remove(tile)

        if not position:
            self.tiles.append((tile))
        else:
            self.tiles.insert(position, tile)

    @property
    def word(self):
        return ''.join(letter for x, y, letter in self.tiles)
        

class WordsmushPlayer(object):
    
    def __init__(self):
        self.score = 0

