import argparse
import os

from . import configlib
from .anime import argparse as anime
from .manga import argparse as manga

parser = argparse.ArgumentParser()
parser.add_argument('--config', type=configlib.load_config,
                    default=configlib.default_config())
parser.add_argument('--log', metavar='LOGFILE')

subparsers = parser.add_subparsers(title='Managers')
anime.add_parsers(subparsers)
manga.add_parsers(subparsers)
