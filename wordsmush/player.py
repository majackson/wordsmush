import uuid
import re

from wordsmush.game import WordsmushWord
from wordsmush.cli import loop_input


class WordsmushPlayer(object):
    
    def __init__(self, name=None):
        self.name = name or uuid.uuid4() 

class CommandLineWordsmushPlayer(WordsmushPlayer):

    def take_turn(self, game):
        word = WordsmushWord(game)

        move_complete = False
        move_rx = re.compile('^(help|play|rem|clear|\d,\d)', re.IGNORECASE)
        tile_rx = re.compile('^(?P<x>\d),(?P<y>\d)( (?P<pos>\d))?', re.IGNORECASE)

        while not move_complete:
            move_text = ''
            print(game)
            print(word)

            while not move_rx.match(move_text):
                move_text = loop_input("Enter move or 'help'")
            
            if move_text == 'play':
                if game.is_playable(word):
                    game.play(self, word)
                    move_complete = True
                else:
                    print("'%s' is not a playable word." % word.word.upper())
            elif move_text == 'help':
                self.print_help()
            elif move_text == 'clear':
                word.clear_tiles()
            elif move_text.startswith('rem'):
                rem_tile = int(move_text[3:])
                word.remove_tile_at_position(rem_tile-1)
            else:  # add tile
                tile_move = tile_rx.match(move_text)
                if tile_move:
                    tile_move_dict = tile_move.groupdict()
                    tile_x = int(tile_move_dict.get('x'))
                    tile_y = int(tile_move_dict.get('y'))
                    tile_pos = tile_move_dict.get('pos')
                    tile_pos = int(tile_pos)-1 if tile_pos else None

                    try:
                        game_tile = game.get_tile(tile_x-1, tile_y-1)
                        word.add_tile(game_tile, tile_pos)
                    except IndexError:
                        print("No such tile.")

        return word

    @staticmethod
    def print_help():
        print("""
        Wordsmush Playing Help:
        To add a tile to the end of word, type the co-ordinates of the tile separated by a comma - e.g. '3,2'.
        To add a tile to a specific position in a word, type the co-ordinates followed by a position - e.g. '3,2 2'.
        To remove a tile from a specific position, type 'rem' followed by the tiles position - e.g. 'rem 2'.
        To remove all tiles from the current word, type 'clear'.
        To play the currently selected tiles, type 'play'.
        To view this help text, type 'help'.
        """)

