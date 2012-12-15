"""Rudimentary word lookup in python. Simply dumps the system word list into
memory and looks through it."""

WORDS_FILE = '/usr/share/dict/words'
with file(WORDS_FILE) as f:
    words = [word.strip().lower() for word in f.readlines()]
