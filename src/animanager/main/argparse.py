import argparse
import logging

from animanager import configlib
from animanager.anime import argparse as anime


def make_parser():

    """Make an ArgumentParser."""

    # Set up main parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=configlib.load_config,
                        default=configlib.default_config())
    parser.add_argument('--debug', action='store_true')

    # Set up subparsers
    subparsers = parser.add_subparsers(title='Managers')

    # Set up anime subsubparser
    subparser = subparsers.add_parser('anime')
    subsubparsers = subparser.add_subparsers(title='Commands')
    anime.add_parsers(subsubparsers)

    return parser
