import unittest
from itertools import cycle

from mock import Mock

from wordsmush.game import (WordsmushGame, WordsmushTile, WordsmushWord)
from wordsmush.player import WordsmushPlayer

from wordsmush.tests import test_utils

class TestWordsmushGame(unittest.TestCase):
    
    def setUp(self):
        self.game = test_utils.get_alpha_board() 

    def test_get_tile(self):
        a_tile = self.game.get_tile(0,0)
        self.assertEqual(a_tile.letter, 'a')
        self.assertEqual(a_tile.owner, None)
        self.assertEqual(a_tile.status, WordsmushTile.UNTAKEN)

        a_tile = self.game.get_tile(3,3)
        self.assertEqual(a_tile.letter, 's')
        self.assertEqual(a_tile.owner, None)
        self.assertEqual(a_tile.status, WordsmushTile.UNTAKEN)
        
    def test_is_playable(self):
        # test a valid word
        self.assertTrue(self.game.is_playable(Mock(word='planting')))
        self.game.words_played.append('planting')

        # test a non-dict word
        self.assertFalse(self.game.is_playable(Mock(word='xxdjfhskfh')))

        # test a word previously played
        self.assertFalse(self.game.is_playable(Mock(word='planting')))

        # test a word which is a substring of a word previously played
        self.assertFalse(self.game.is_playable(Mock(word='plan')))

    def test_play(self):
        pass

    def test_calculate_protected(self):
        self.game = test_utils.get_board(['f', 'r', 'a', 'b', 'c',
                                          'n', 'a', 'h', 'i', 'j',
                                          't', 'i', 'm', 'n', 'o',
                                          'c', 's', 'g', 'x', 'q',
                                          'u', 'v', 'w', 'y', 'z'])
        word = WordsmushWord(self.game)
        word.add_tile(self.game.get_tile(0,0))
        word.add_tile(self.game.get_tile(1,0))
        word.add_tile(self.game.get_tile(1,1))
        word.add_tile(self.game.get_tile(0,1))
        word.add_tile(self.game.get_tile(0,2))
        word.add_tile(self.game.get_tile(1,2))
        word.add_tile(self.game.get_tile(0,3))

        self.assertTrue([tile.letter for tile in word.tiles] == list('frantic'))

        self.game.play(self.game.player1, word)

        self.assertTrue(all(tile.owner == self.game.player1 for tile in word.tiles))

        protected_tile1 = self.game.get_tile(0,0)
        protected_tile2 = self.game.get_tile(0,1)
        self.assertTrue(protected_tile1.status == WordsmushTile.PROTECTED)
        self.assertTrue(protected_tile2.status == WordsmushTile.PROTECTED)

        # now test that a second play will not capture a protected tile
        word2 = WordsmushWord(self.game)
        word2.add_tile(self.game.get_tile(0,0))
        word2.add_tile(self.game.get_tile(1,1))
        word2.add_tile(self.game.get_tile(0,1))
        word2.add_tile(self.game.get_tile(2,0))
        word2.add_tile(self.game.get_tile(0,2))
        word2.add_tile(self.game.get_tile(1,2))
        word2.add_tile(self.game.get_tile(0,3))

        self.assertTrue([tile.letter for tile in word2.tiles] == list('fanatic'))

        self.game.play(self.game.player2, word2)

        self.assertTrue(protected_tile1.owner == self.game.player1)
        self.assertTrue(protected_tile2.owner == self.game.player1)


    def test_is_a_word(self):
        # Tested by is_playable method
        pass

    def test_is_playable_word(self):
        # Tested by is_playable method
        pass

    def test_is_game_over(self):

        # test all tiles taken
        owner = cycle([self.game.player1, self.game.player2])
        for tile in self.game.tiles:
            tile.status = WordsmushTile.TAKEN
            tile.owner = next(owner)

        self.assertTrue(self.game.is_game_over())

        # test only some tiles taken
        tile1 = self.game.get_tile(2,2)
        tile2 = self.game.get_tile(3,3)
        tile1.owner = None
        tile1.status = WordsmushTile.UNTAKEN
        tile2.owner = None
        tile2.status = WordsmushTile.UNTAKEN

        self.assertFalse(self.game.is_game_over())

        # test no tiles taken
        self.game = test_utils.get_alpha_board()
        self.assertFalse(self.game.is_game_over())
        

    def test_get_points(self):
        word_cat = WordsmushWord(self.game)
        word_cat.add_tile(self.game.get_tile(2,0))
        word_cat.add_tile(self.game.get_tile(0,0))
        word_cat.add_tile(self.game.get_tile(4,3))
        self.game.play(self.game.player1, word_cat)

        self.assertTrue(self.game.get_points(self.game.player1) == 3)
        self.assertTrue(self.game.get_points(self.game.player2) == 0)

        word_bat = WordsmushWord(self.game)
        word_bat.add_tile(self.game.get_tile(1,0))
        word_bat.add_tile(self.game.get_tile(0,0))
        word_bat.add_tile(self.game.get_tile(4,3))
        self.game.play(self.game.player2, word_bat)

        self.assertTrue(self.game.get_points(self.game.player1) == 1)
        self.assertTrue(self.game.get_points(self.game.player2) == 3)

        word_fabric = WordsmushWord(self.game)
        word_fabric.add_tile(self.game.get_tile(0,1))
        word_fabric.add_tile(self.game.get_tile(0,0))
        word_fabric.add_tile(self.game.get_tile(1,0))
        word_fabric.add_tile(self.game.get_tile(2,3))
        word_fabric.add_tile(self.game.get_tile(3,1))
        word_fabric.add_tile(self.game.get_tile(2,0))
        self.game.play(self.game.player1, word_fabric)  # tile in 0,0 (a) is now protected

        self.assertTrue(self.game.get_points(self.game.player1) == 6)
        self.assertTrue(self.game.get_points(self.game.player2) == 1)

        word_cab = WordsmushWord(self.game)
        word_cab.add_tile(self.game.get_tile(2,0))
        word_cab.add_tile(self.game.get_tile(0,0))
        word_cab.add_tile(self.game.get_tile(1,0))
        self.game.play(self.game.player2, word_cab)

        self.assertTrue(self.game.get_points(self.game.player1) == 4)
        self.assertTrue(self.game.get_points(self.game.player2) == 3)


class TestWordsmushTile(unittest.TestCase):

    def setUp(self):
        self.game = test_utils.get_alpha_board() 

    def test_tile_above(self):
        a_tile = self.game.get_tile(0,0)   # a
        self.assertEqual(a_tile.tile_above(), None)

        g_tile = self.game.get_tile(1,1)  # g
        self.assertEqual(g_tile.tile_above(), self.game.get_tile(1,0))

        y_tile = self.game.get_tile(4,4)  # y
        self.assertEqual(y_tile.tile_above(), self.game.get_tile(4,3))

    def test_tile_below(self):
        a_tile = self.game.get_tile(0,0)  # a
        self.assertEqual(a_tile.tile_below(), self.game.get_tile(0,1))

        g_tile = self.game.get_tile(1,1)  # g
        self.assertEqual(g_tile.tile_below(), self.game.get_tile(1,2))

        y_tile = self.game.get_tile(4,4)  # y
        self.assertEqual(y_tile.tile_below(), None)

    def test_tile_right(self):
        a_tile = self.game.get_tile(0,0)  # a
        self.assertEqual(a_tile.tile_right(), self.game.get_tile(1,0))

        g_tile = self.game.get_tile(1,1)  # g
        self.assertEqual(g_tile.tile_right(), self.game.get_tile(2,1))

        y_tile = self.game.get_tile(4,4)  # y
        self.assertEqual(y_tile.tile_right(), None)

    def test_tile_left(self):
        a_tile = self.game.get_tile(0,0)  # a
        self.assertEqual(a_tile.tile_left(), None)

        g_tile = self.game.get_tile(1,1)  # g
        self.assertEqual(g_tile.tile_left(), self.game.get_tile(0,1))

        y_tile = self.game.get_tile(4,4)  # y
        self.assertEqual(y_tile.tile_left(), self.game.get_tile(3,4))


class TestWordsmushWord(unittest.TestCase):

    def setUp(self):
        self.game = test_utils.get_alpha_board() 

    def test_add_tile(self):
        word = WordsmushWord(self.game)

        word.add_tile(self.game.get_tile(0,0))
        word.add_tile(self.game.get_tile(1,0))

        self.assertEqual(word.word, 'ab')

        word.add_tile(self.game.get_tile(2,0), position=0)

        self.assertEqual(word.word, 'cab')

        # test moving a tile from one position to another
        word.add_tile(self.game.get_tile(1,0), position=0)
        word.add_tile(self.game.get_tile(2,0), position=2)
        word.add_tile(self.game.get_tile(0,2), position=3)

        self.assertEqual(word.word, 'back')

    def test_remove_tile(self):
        word = WordsmushWord(self.game)

        word.add_tile(self.game.get_tile(2,0))
        word.add_tile(self.game.get_tile(0,0))
        word.add_tile(self.game.get_tile(2,3))
        word.add_tile(self.game.get_tile(4,3))
        word.add_tile(self.game.get_tile(4,2))
        word.add_tile(self.game.get_tile(3,2))

        self.assertEqual(word.word, 'carton')

        # remove from beginning
        word.remove_tile(self.game.get_tile(2,0))
        self.assertEqual(word.word, 'arton')

        # remove from end
        word.remove_tile(self.game.get_tile(3,2))
        self.assertEqual(word.word, 'arto')

        # remove from middle 
        word.remove_tile(self.game.get_tile(4,3))
        self.assertEqual(word.word, 'aro')

    def test_remove_tile_at_position(self):
        word = WordsmushWord(self.game)

        word.add_tile(self.game.get_tile(2,0))
        word.add_tile(self.game.get_tile(0,0))
        word.add_tile(self.game.get_tile(2,3))
        word.add_tile(self.game.get_tile(4,3))
        word.add_tile(self.game.get_tile(4,2))
        word.add_tile(self.game.get_tile(3,2))

        self.assertEqual(word.word, 'carton')

        # remove from beginning
        word.remove_tile_at_position(0)
        self.assertEqual(word.word, 'arton')

        # remove from end
        word.remove_tile_at_position(4)
        self.assertEqual(word.word, 'arto')

        # remove from middle 
        word.remove_tile_at_position(2)
        self.assertEqual(word.word, 'aro')


    def test_clear_tiles(self):
        word = WordsmushWord(self.game)

        word.clear_tiles()
        self.assertEqual(word.word, '')

        word.add_tile(self.game.get_tile(2,0))
        word.add_tile(self.game.get_tile(0,0))
        word.add_tile(self.game.get_tile(1,0))

        self.assertEqual(word.word, 'cab')

        word.clear_tiles()
        self.assertEqual(word.word, '')


