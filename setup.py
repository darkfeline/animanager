#!/usr/bin/env python3

from setuptools import setup

setup(
    name='animanager',
    version='0.9.0',
    packages=['animanager'],
    install_requires=['tabulate'],
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
