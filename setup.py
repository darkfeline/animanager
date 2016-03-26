#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages

setup(
    name='animanager',
    version='0.10.0',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=['apsw', 'tabulate'],
    entry_points={
        'console_scripts': [
            'animanager = animanager.main:main',
        ],
    },

    author='Allen Li',
    author_email='darkfeline@felesatra.moe',
    description='Anime tracking and management application',
    license='GPLv3',
    url='https://darkfeline.github.io/animanager/',
)
