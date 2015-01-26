"""
This package provides an easy framework for implementing commands.
"""

import logging

from . import argparse


def main():
    """Entry function."""
    # Set up logging.
    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    root_logger.addHandler(handler)
    # Parse arguments.
    parser = argparse.make_parser()
    args = parser.parse_args()
    if args.debug:
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s @%(name)s %(message)s'))
        # handler default is pass all
        root_logger.setLevel('DEBUG')
    else:
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        handler.setLevel('WARNING')
        # root logger default is WARNING
    # Run command.
    try:
        func = args.func
    except AttributeError:
        parser.print_help()
    else:
        func(args)

if __name__ == '__main__':
    main()
