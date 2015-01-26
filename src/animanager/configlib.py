import json
import os


def load_config(path):
    """Load config from file."""
    with open(path) as file:
        config = json.load(file)
    return config


def default_config():
    """Return default user config path."""
    return os.path.join(os.path.expanduser("~"), '.anime.cfg')
