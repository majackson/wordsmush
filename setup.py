#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='Wordsmush',
    version=0.1,
    description='Wordsmush, a python-based clone of Letterpress.',
    author='Matt Jackson',
    author_email='me@mattjackson.eu',
    packages=find_packages(),
    install_requires=['colorama'],
    entry_points={},
)
