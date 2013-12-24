import json
import os


def load_config(f):
    """Load config from file

    Args:
        f: file path

    """
    with open(f) as f:
        config = json.load(f)
    return config


def default_config():
    """Return default user config"""
    return os.path.join(os.path.expanduser("~"), '.anime.cfg')
