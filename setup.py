#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='animanager',
    version='0.8.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    requires=['tabulate'],
    entry_points={
        'console_scripts': [
            'animanager = animanager.main:main',
        ],
    },

    author='Allen Li',
    author_email='darkfeline@felesatra.moe',
    description='Anime tracking/management application',
    license='GPLv3',
    url='https://darkfeline.github.io/animanager/',
)
