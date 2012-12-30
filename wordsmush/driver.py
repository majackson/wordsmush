from itertools import cycle

from wordsmush.game import WordsmushGame
from wordsmush.player import CommandLineWordsmushPlayer
from wordsmush.ai import WordsmushAIPlayer
from wordsmush.cli import loop_input


class WordsmushGameDriver(object):

    def __init__(self):
        self.player1, self.player2 = self.get_players()

        self.game = WordsmushGame(self.player1, self.player2)
        turn_player = cycle([self.player1, self.player2])

        while not self.game.is_game_over():
            player = next(turn_player)
            self.get_turn(player)

        if self.game.scores[self.player1] == self.game.scores[self.player2]:
            self.game_draw()
        else:
            (winner, winner_score), (loser, loser_score) = \
                sorted(self.game.scores.items(), key=lambda i: -i[1])

            self.game_over(winner, loser)

    def get_turn(self, player):
        player.take_turn(self.game)


class CommandLineWordsmushGameDriver(WordsmushGameDriver):

    def get_players(self):
        player1_name = loop_input("Enter name for Player 1, or 'ai' for computer opponent")
        player2_name = loop_input("Enter name for Player 2, or 'ai' for computer opponent")

        player1 = (CommandLineWordsmushPlayer(player1_name) 
            if player1_name != 'ai' else WordsmushAIPlayer())

        player2 = (CommandLineWordsmushPlayer(player2_name) 
            if player2_name != 'ai' else WordsmushAIPlayer())

        return player1, player2

    def __init__(self):
        print("Starting new Wordsmush game...")
        super(CommandLineWordsmushGameDriver, self).__init__()

    def game_draw(self):
        print(self.game)
        print("Both players have %d points. The game is a draw!" % 
            self.game.scores[self.player1])

    def game_over(self, winner, loser):
        print(self.game)
        print("%s wins by %d-%d!" % 
            (winner.name, self.game.scores[winner], self.game.scores[loser]))

    def get_turn(self, player):
        print("%s's turn" % player.name)
        word = player.take_turn(self.game)

        print("%s played %s" % (player.name, word.word.upper()))
        print("Scores:\n%s - %d\n%s - %d" % (self.player1.name, self.game.scores[self.player1],
                                           self.player2.name, self.game.scores[self.player2])) 

def command_line():
    """Entry point to start a new command line game"""
    CommandLineWordsmushGameDriver()

