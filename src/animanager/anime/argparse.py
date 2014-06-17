from . import commands


def add_parsers(subparsers):
    parser = subparsers.add_parser('anime')
    subparsers = parser.add_subparsers(title='Commands')

    # import {{{1
    tmp_parser = subparsers.add_parser('imp')
    tmp_parser.add_argument('file')
    tmp_parser.set_defaults(func=commands.imp)

    # bump {{{1
    tmp_parser = subparsers.add_parser('bump')
    tmp_parser.add_argument('name', nargs='?')
    tmp_parser.set_defaults(func=commands.bump)

    # add {{{1
    tmp_parser = subparsers.add_parser('add')
    tmp_parser.add_argument('name', nargs='?')
    tmp_parser.set_defaults(func=commands.add)

    # hold {{{1
    tmp_parser = subparsers.add_parser('hold')
    tmp_parser.add_argument('name', nargs='?')
    tmp_parser.set_defaults(func=commands.hold)

    # drop {{{1
    tmp_parser = subparsers.add_parser('drop')
    tmp_parser.add_argument('name', nargs='?')
    tmp_parser.set_defaults(func=commands.drop)

    # update {{{1
    tmp_parser = subparsers.add_parser('update')
    tmp_parser.set_defaults(func=commands.update)

    # stats {{{1
    tmp_parser = subparsers.add_parser('stats')
    tmp_parser.set_defaults(func=commands.stats)
