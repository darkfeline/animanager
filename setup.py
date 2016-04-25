#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name='animanager',
    version='0.10.2',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=['apsw', 'tabulate'],
    entry_points={
        'console_scripts': [
            'animanager = animanager.__main__:main',
        ],
    },

    author='Allen Li',
    author_email='darkfeline@felesatra.moe',
    description='Command line program for advanced anime watching management',
    license='GPLv3',
    url='https://www.felesatra.moe/animanager/',
)
