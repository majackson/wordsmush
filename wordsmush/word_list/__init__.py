"""Rudimentary word lookup in python. Simply dumps the system word list into
memory and looks through it."""

from pkg_resources import resource_stream

WORDS_FILE = 'scrabble_us'

with resource_stream(__name__, WORDS_FILE) as f:
    words = {word.strip().lower(): True for word in f.readlines()}
