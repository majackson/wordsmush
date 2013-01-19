from itertools import imap, izip
from collections import Counter

from wordsmush.player import WordsmushPlayer
from wordsmush.game import WordsmushTurn
from wordsmush import word_list


class WordsmushAIPlayer(WordsmushPlayer):

    def __init__(self):
        self.name = "Wordbot"
        self.playable_words = {}

    def solve_board(self, game):
        """Compute list of all playable words for this board
        :param game: WordsmushGame instance representing the board"""

        counted_letters = Counter(tile.letter for tile in game.tiles)
        words_by_letter_count = izip(word_list.words, imap(Counter, word_list.words))
         
        def is_match(word):
            # Takes word as Counter('something')
            for letter in word:
                if not (word[letter] <= counted_letters[letter]):
                    return False
            return True

        return sorted((word for word, letter_count in words_by_letter_count 
                            if is_match(letter_count)), key=len, reverse=True)

    def get_best_word(self, game):
        turn = WordsmushTurn(game)

        try:
            word_str = next(word for word in self.playable_words[game] 
                            if game.is_playable_word(word) and len(word) > 2)
            self.playable_words[game].remove(word_str)

            tiles_by_letter = game.tiles_by_letter()
            for word_char in word_str:
                turn.add_tile(next(tile for tile in tiles_by_letter[word_char]
                                        if tile not in turn.tiles))
        except StopIteration:  # no more words left to play!
            turn.resign = True

        return turn

    def take_turn(self, game):
        if not self.playable_words.get(game):
            self.playable_words[game] = self.solve_board(game) 
                               
        word = self.get_best_word(game)
        game.play(self, word)

        return word
