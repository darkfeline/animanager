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
def bump(config, *args):
    logger.debug('bump(%r)', args)
    parser = argparse.ArgumentParser(prog="anime bump", add_help=False)
    parser.add_argument('name', nargs="?")
    args = parser.parse_args(args)
    from animanager import bump
    bump.main(config, args.name)


@_public
@_command
def add(config, *args):
    logger.debug('add(%r)', args)
    parser = argparse.ArgumentParser(prog="anime add", add_help=False)
    parser.add_argument('name', nargs="?")
    args = parser.parse_args(args)
    from animanager import add
    add.main(config, args.name)


@_public
@_command
def hold(config, *args):
    logger.debug('hold(%r)', args)
    parser = argparse.ArgumentParser(prog="anime hold", add_help=False)
    parser.add_argument('name', nargs="?")
    args = parser.parse_args(args)
    from animanager import hold
    hold.main(config, args.name)


@_public
@_command
def drop(config, *args):
    logger.debug('drop(%r)', args)
    parser = argparse.ArgumentParser(prog="anime drop", add_help=False)
    parser.add_argument('name', nargs="?")
    args = parser.parse_args(args)
    from animanager import drop
    drop.main(config, args.name)


@_public
@_command
def update(config, *args):
    logger.debug('update(%r)', args)
    parser = argparse.ArgumentParser(prog="anime update", add_help=False)
    args = parser.parse_args(args)
    from animanager import update
    update.main(config)


@_public
@_command
def stats(config, *args):
    logger.debug('stats(%r)', args)
    parser = argparse.ArgumentParser(prog="anime stats", add_help=False)
    args = parser.parse_args(args)
    from animanager import stats
    stats.main(config)
