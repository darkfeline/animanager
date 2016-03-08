"""Helper functions for the pickle standard module."""

import pickle


def dump(obj, file):
    try:
        with open(file, 'wb') as file:
            pickle.dump(obj, file)
    except Exception as e:
        print(e)


def load(file):
    with open(file, 'rb') as file:
        return pickle.load(file)
