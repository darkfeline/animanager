import argparse
import logging


def _make_appender(obj):
    def f(x):
        obj.append(x.__name__)
        return x
    return f

__all__ = ['t_command']
logger = logging.getLogger(__name__)
t_command = []

_public = _make_appender(__all__)
_command = _make_appender(t_command)


@_public
@_command
def imp(config, *args):
    """import"""
    logger.debug('import(%r)', args)
    parser = argparse.ArgumentParser(prog="manga imp", add_help=False)
    parser.add_argument('file')
    args = parser.parse_args(args)
    from animanager.manga import imp
    imp.main(config, args.file)


@_public
@_command
def bump(config, *args):
    logger.debug('bump(%r)', args)
    parser = argparse.ArgumentParser(prog="manga bump", add_help=False)
    parser.add_argument('name', nargs="?")
    args = parser.parse_args(args)
    from animanager.manga import bump
    bump.main(config, args.name)


@_public
@_command
def add(config, *args):
    logger.debug('add(%r)', args)
    parser = argparse.ArgumentParser(prog="manga add", add_help=False)
    parser.add_argument('name', nargs="?")
    args = parser.parse_args(args)
    from animanager.manga import add
    add.main(config, args.name)


@_public
@_command
def hold(config, *args):
    logger.debug('hold(%r)', args)
    parser = argparse.ArgumentParser(prog="manga hold", add_help=False)
    parser.add_argument('name', nargs="?")
    args = parser.parse_args(args)
    from animanager.manga import hold
    hold.main(config, args.name)


@_public
@_command
def drop(config, *args):
    logger.debug('drop(%r)', args)
    parser = argparse.ArgumentParser(prog="manga drop", add_help=False)
    parser.add_argument('name', nargs="?")
    args = parser.parse_args(args)
    from animanager.manga import drop
    drop.main(config, args.name)


@_public
@_command
def update(config, *args):
    logger.debug('update(%r)', args)
    parser = argparse.ArgumentParser(prog="manga update", add_help=False)
    args = parser.parse_args(args)
    from animanager.manga import update
    update.main(config)


@_public
@_command
def stats(config, *args):
    logger.debug('stats(%r)', args)
    parser = argparse.ArgumentParser(prog="manga stats", add_help=False)
    args = parser.parse_args(args)
    from animanager.manga import stats
    stats.main(config)
