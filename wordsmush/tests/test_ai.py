import unittest

from wordsmush import game_utils
from wordsmush.ai import WordsmushAIPlayer

class TestAI(unittest.TestCase):

    def setUp(self):
        self.ai = WordsmushAIPlayer() 
    
    def test_solve_board(self):
        game = game_utils.get_board(
            'espro'
            'lishm'
            'tabdi'
            'entsi'
            'xfgmn')

        solved_game = self.ai.solve_board(game)
        words = ['establish', 'sadism', 'establishment', 'disestablishment',
                 'stab', 'stand', 'spasm', 'stream', 'espresso']

        for word in words:
            self.assertTrue(word in solved_game) 
