from itertools import cycle
import re

from wordsmush.game import WordsmushGame, WordsmushWord
from wordsmush.player import WordsmushPlayer


class WordsmushGameDriver(object):

    def __init__(self):
        player1_name, player2_name = self.get_player_names()
        self.player1 = WordsmushPlayer(name=player1_name)
        self.player2 = WordsmushPlayer(name=player2_name)

        self.game = WordsmushGame(self.player1, self.player2)
        turn_player = cycle([self.player1, self.player2])

        while not self.game.is_game_over():
            player = next(turn_player)
            self.get_turn(player)

        if self.player1.score == self.player2.score:
            self.game_draw()
        else:
            winner, loser = (self.player1, self.player2 
                            if self.player1.score > self.player2.score 
                            else self.player2, self.player1)
            self.game_over(winner, loser)


class CommandLineWordsmushGameDriver(WordsmushGameDriver):

    def __init__(self):
        print("Starting new Wordsmush game...")
        super(CommandLineWordsmushGameDriver, self).__init__()

    def game_draw(self):
        print(self.game)
        print("Both players have %d points. The game is a draw!" % self.player1.score)

    def game_over(self, winner, loser):
        print(self.game)
        print("%s wins by %d-%d!" % (winner.name, winner.score, loser.score))

    def get_turn(self, player):
        print("%s's turn" % player.name)
        word = WordsmushWord(self.game)

        move_complete = False
        move_rx = re.compile('^(help|play|rem|clear|\d,\d)', re.IGNORECASE)
        tile_rx = re.compile('^(?P<x>\d),(?P<y>\d)( (?P<pos>\d))?', re.IGNORECASE)

        while not move_complete:
            move_text = ''
            print(self.game)
            print(word.word.upper())

            while not move_rx.match(move_text):
                move_text = self.loop_input("Enter move or 'help'")
            
            if move_text == 'play':
                if self.game.is_playable(word):
                    self.game.play(player, word)
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
            else:
                tile_move = tile_rx.match(move_text)
                if tile_move:
                    tile_move_dict = tile_move.groupdict()
                    tile_x = int(tile_move_dict.get('x'))
                    tile_y = int(tile_move_dict.get('y'))
                    tile_pos = tile_move_dict.get('pos')
                    tile_pos = int(tile_pos)-1 if tile_pos else None
                    game_tile = self.game.get_tile(tile_x-1, tile_y-1)

                    word.add_tile(game_tile, tile_pos)

        print("%s played %s" % (player.name, word.word.upper()))

        self.player1.score = self.game.get_points(self.player1)
        self.player2.score = self.game.get_points(self.player2)
        print("Scores:\n%s - %d\n%s - %d" % (self.player1.name, self.player1.score,
                                           self.player2.name, self.player2.score)) 

    def print_help(self):
        print("""
        Wordsmush Playing Help:
        To add a tile to the end of word, type the co-ordinates of the tile separated by a comma - e.g. '3,2'.
        To add a tile to a specific position in a word, type the co-ordinates followed by a position - e.g. '3,2 2'.
        To remove a tile from a specific position, type 'rem' followed by the tiles position - e.g. 'rem 2'.
        To remove all tiles from the current word, type 'clear'.
        To play the currently selected tiles, type 'play'.
        To view this help text, type 'help'.
        """)

    def get_player_names(self):
        player1_name = self.loop_input('Enter name for Player 1')
        player2_name = self.loop_input('Enter name for Player 2')
        return player1_name, player2_name
    
    @staticmethod
    def loop_input(message):
        """Repeats input until user inputs valid data"""
        user_input = ''
        while not user_input.strip():
            user_input = raw_input('%s: ' % message)

        return user_input

def command_line():
    """Entry point to start a new command line game"""
    CommandLineWordsmushGameDriver()
