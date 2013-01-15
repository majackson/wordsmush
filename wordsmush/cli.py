from itertools import groupby
import argparse

def loop_input(message):
    """Repeats input until user inputs valid data"""
    user_input = ''
    while not user_input.strip():
        user_input = raw_input('%s: ' % message)

    return user_input

def solve_from_letters(letters):
    from wordsmush import game_utils
    from wordsmush.ai import WordsmushAIPlayer

    ai = WordsmushAIPlayer()
    board = game_utils.get_board(letters)
    words = ai.solve_board(board)
    words_by_len = groupby(words, key=len)
    for length, words in words_by_len:
        if length > 2:
            print "%d letter words: " % length
            print ", ".join(words)

def solve_from_letters_entry_point():
    p = argparse.ArgumentParser()
    p.add_argument('letters', help='The letters on the board you would like to solve.')
    args = p.parse_args()
    solve_from_letters(args.letters)
