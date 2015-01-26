from . import commands


def add_parsers(subparsers):

    parser = subparsers.add_parser('bump')
    parser.add_argument('name', nargs='?')
    parser.set_defaults(func=commands.bump)

    parser = subparsers.add_parser('add')
    parser.add_argument('name', nargs='?')
    parser.set_defaults(func=commands.add)

    parser = subparsers.add_parser('update')
    parser.set_defaults(func=commands.update)

    parser = subparsers.add_parser('stats')
    parser.set_defaults(func=commands.stats)
