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
