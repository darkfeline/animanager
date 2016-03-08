"""Search against AniDB titles dump.

"""

import argparse
import xml.etree.ElementTree as ET
import pickle
import os
import re

RAW_FILE = 'anime-titles.xml'
CACHE_FILE = 'anime-titles.pickle'


def load_tree():
    """Load anime titles XML tree."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as file:
            tree = pickle.load(file)
    else:
        tree = ET.parse(RAW_FILE)
        with open(CACHE_FILE, 'wb') as file:
            pickle.dump(tree, file)
    return tree


def print_results(list):
    """Pretty print list of anime trees."""
    for anime in list:
        print(anime.attrib['aid'])
        for title in anime:
            print(title.text)
        print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    tree = load_tree()
    root = tree.getroot()
    query = re.compile('.*'.join(args.query), re.I)
    found = set()
    for anime in root:
        for title in anime:
            if query.search(title.text):
                found.add(anime)
                break
    print_results(sorted(found, key=lambda anime: anime.attrib['aid']))

if __name__ == '__main__':
    main()
