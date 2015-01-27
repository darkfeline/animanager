#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='animanager',
    version='0.1',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    requires=['mysql.connector'],
    entry_points={
        'console_scripts': [
            'animanager = animanager.main:main',
        ],
    },

    author='Allen Li',
    author_email='darkfeline@felesatra.moe',
    description='Anime manager MySQL frontend application',
    license='GPLv3',
    url='',
)
