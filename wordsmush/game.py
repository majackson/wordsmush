from random import randint
from operator import add

from colorama import Fore, Back, Style

from wordsmush.word_lookup import words


class WordsmushGame(object):

    def __init__(self, player1, player2, board_width=5, board_height=5):
        """Instantiates a new WordsmushGame.
        :param player1: a WordsmushPlayer instance representing player 1 of the new game
        :param player2: a WordsmushPlayer instance representing player 2 of the new game
        :param board_width: The width of the play board (optional, default is 5) 
        :param board_height: the height of the play board (optional, default is 5)
        """
        self.board_width = 5
        self.board_height = 5

        self.player1 = player1
        self.player2 = player2

        random_letter = lambda: chr(randint(ord('a'), ord('z')))
        self.board = [[ WordsmushTile(self, n, m, random_letter())
                            for n in range(board_width)] for m in range(board_height)]
        self.words_played = []

    @property
    def tiles(self):
        """Iterator for all tiles on the board"""
        for tile in reduce(add, self.board):
            yield tile

    def __repr__(self):
        return self.format_pretty()

    def format_pretty(self):
        """Returns a colourised representation of the play state of the board"""
        COLOR_MAPPING = {
            (WordsmushTile.UNTAKEN, None): Fore.BLACK + Back.WHITE + Style.NORMAL,
            (WordsmushTile.TAKEN, self.player1): Fore.CYAN + Back.BLUE + Style.DIM, 
            (WordsmushTile.TAKEN, self.player2): Fore.RED + Back.YELLOW + Style.DIM,
            (WordsmushTile.PROTECTED, self.player1): Fore.BLUE + Back.BLUE + Style.BRIGHT,
            (WordsmushTile.PROTECTED, self.player2): Fore.RED + Back.RED + Style.BRIGHT,
        }

        format_string = ''
        for tile_row in self.board:
            for tile in tile_row:
                format_string += COLOR_MAPPING[tile.status, tile.owner] + (' %s ' % tile.letter.upper())
            format_string += Fore.RESET + Back.RESET + Style.RESET_ALL + '\n'

        return format_string

    def get_tile(self, x, y):
        """Get tile at the specified index
        :param x: zero-based index of the x value of the requested tile
        :param y: zero-based index of the y value of the requested tile"""

        return self.board[y][x]

    def is_playable(self, word):
        """Returns whether a word is playable, based on if it is a dict word
        and if it has not been played before"""
        return self.is_a_word(word) and self.is_playable_word(word)

    def play(self, player, word):
        """Play a single turn.
        :param player: the player playing the turn.
        :param word: the instance of WordsmushWord representing the turn."""

        if self.is_a_word(word) and self.is_playable_word(word): 

            # give possession of each new letter to player, 
            # if the tiles are unprotected
            for tile in word.tiles:
                if tile.status != WordsmushTile.PROTECTED:
                    tile.status = WordsmushTile.TAKEN
                    tile.owner = player

            self.calculate_protected()
            self.words_played.append(word.word)
        else:
            raise ValueError("Word is not playable")

    def get_points(self, player):
        return sum(1 for tile in self.tiles if tile.owner == player)

    def is_game_over(self):
        return all(tile.owner for tile in self.tiles)

    def calculate_protected(self):
        """Calculates the protected status of all tiles on the board"""

        has_tile = lambda f: f() is not None
        tile_owned = lambda t, p: t.status in (WordsmushTile.TAKEN, WordsmushTile.PROTECTED) and t.owner == p
        def tile_surrounded(tile):
            if ((not has_tile(tile.tile_above) or tile_owned(tile.tile_above(), tile.owner)) and
               (not has_tile(tile.tile_below) or tile_owned(tile.tile_below(), tile.owner)) and
               (not has_tile(tile.tile_left) or tile_owned(tile.tile_left(), tile.owner)) and
               (not has_tile(tile.tile_right) or tile_owned(tile.tile_right(), tile.owner))):
                    return True

        for tile in self.tiles:
            if tile.status in (WordsmushTile.TAKEN, WordsmushTile.PROTECTED):
                if tile_surrounded(tile):
                    tile.status = WordsmushTile.PROTECTED
                else:
                    tile.status = WordsmushTile.TAKEN
        

    def is_a_word(self, word):
        """Returns whether or not the word is a valid dictionary word"""
        return word.word in words

    def is_playable_word(self, word):
        """Returns whether or not the word is playable.
        This is simply if the word or a superstring of word has been played before."""
        return not any(played_word.startswith(word.word) for played_word in self.words_played)

class WordsmushTile(object):

    # tile statuses
    UNTAKEN = 0
    TAKEN = 1
    PROTECTED = 2

    def __init__(self, game, x, y, letter):
        self.game = game
        self.x = x
        self.y = y
        self.letter = letter
        self.status = self.UNTAKEN
        self.owner = None

    def tile_above(self):
        """Return the tile above this tile on the board.
        Returns None if the tile is on the top row of the board."""
        if self.y == 0:
            return None
        else:
            return self.game.get_tile(self.x, self.y-1) 

    def tile_below(self):
        """Return the tile below this tile on the board.
        Returns None if the tile is on the bottom row of the board."""
        if self.y+1 == self.game.board_height:
            return None
        else:
            return self.game.get_tile(self.x, self.y+1) 

    def tile_left(self):
        """Return the tile left of this tile on the board.
        Returns None if the tile is on the left-most column of the board."""
        if self.x == 0:
            return None
        else:
            return self.game.get_tile(self.x-1, self.y)

    def tile_right(self):
        """Return the tile right of this tile on the board.
        Returns None if the tile is on the right-most column of the board."""
        if self.x+1 == self.game.board_width:
            return None
        else:
            return self.game.get_tile(self.x+1, self.y)


class WordsmushWord(object):
    
    def __init__(self, game, tiles=None):
        self.game = game
        self.tiles = tiles or []

    def add_tile(self, tile, position=None):
        """Add a tile to the word, optionally with a specific position.
        This method may also be move a tile already in play. 
        :param tile: a WordsmushTile instance representing the tile to be added.
        :param position: Optional argument to add the tile at a specific position.
        When no position is specified, the tile is added to the end of the word"""

        if tile in self.tiles:
            self.tiles.remove(tile)

        if position is None:
            self.tiles.append((tile))
        else:
            self.tiles.insert(position, tile)

    def remove_tile(self, tile):
        self.tiles.remove(tile)

    def remove_tile_at_position(self, position):
        del self.tiles[position]

    def clear_tiles(self):
        self.tiles = []

    @property
    def word(self):
        return ''.join(tile.letter for tile in self.tiles)
        
