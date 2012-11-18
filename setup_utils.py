import os.path
import re


def get_resources(dir):
    l = []
    _rget_resources(dir, l)
    return l


def _make_listing(dir):
    return (dir, [os.path.join(dir, x) for x in os.listdir(dir) if
            os.path.isfile(os.path.join(dir, x))])


def _rget_resources(dir, l):
    l.append(_make_listing(dir))
    for d in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, d)):
            _rget_resources(os.path.join(dir, d), l)


def get_modules(dir):
    return [_p_py.match(x).group(1) for x in os.listdir(dir) if _p_py.match(x)]
_p_py = re.compile(r'(.+)\.py')


def get_packages(dir):
    l = []
    _rget_packages(dir, '', l)
    return l


def _rget_packages(start, dir, l):
    ls = os.listdir(os.path.join(start, dir))
    if '__init__.py' in ls:
        l.append(dir.replace('/', '.'))
    for x in [x for x in ls if os.path.isdir(os.path.join(start, dir, x))]:
        _rget_packages(start, os.path.join(dir, x), l)


def get_scripts(dir):
    l = []
    _rget_scripts(dir, l)
    return l


def _rget_scripts(dir, l):
    for f in os.listdir(dir):
        f = os.path.join(dir, f)
        if os.path.isfile(f):
            l.append(f)
        elif os.path.sidir(f):
            _rget_scripts(f, l)
