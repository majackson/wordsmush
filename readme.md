# Wordsmush

Wordsmush is a Python clone of the excellent Letterpress by [Loren Brichter](http://twitter.com/lorenb).

If you like Wordsmush (or even if you don't) and you own an iOS device, you should definitely [go download Letterpress now](https://itunes.apple.com/gb/app/letterpress-word-game/id526619424?mt=8).

## Installation

Install using the standard `python setup.py install`

## Use

Currently the only way to play is two-player, locally, via the command line. I might add more in the future.

### Command Line

Start a new game with `wordsmush-cli`

For each turn, type one of the following:

* To add a tile to the end of word, type the co-ordinates of the tile separated by a comma - e.g. '3,2'.
* To add a tile to a specific position in a word, type the co-ordinates followed by a position - e.g. '3,2 2'.
* To remove a tile from a specific position, type 'rem' followed by the tiles position - e.g. 'rem 2'.
* To remove all tiles from the current word, type 'clear'.
* To play the currently selected tiles, type 'play'.
* To pass the current turn, type 'pass'.
* To resign the game, type 'resign'.
* To view this help text, type 'help'.
