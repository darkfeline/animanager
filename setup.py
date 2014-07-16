#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='animanager',
    version='0.1',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    requires=['mysql.connector'],
    scripts=['src/bin/animanager'],

    author='Allen Li',
    author_email='darkfeline@abagofapples.com',
    description='Anime manager MySQL frontend application',
    license='',
    url='',
)
