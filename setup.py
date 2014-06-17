#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='animanager',
    version='0.1',
    description='Anime Manager MySQL frontend application',
    author='Allen Li',
    author_email='darkfeline@abagofapples.com',
    package_dir={'': 'src'},
    packages=['animanager', 'animanager.anime',  'animanager.manga'],
    requires=['mysql.connector'],
    scripts=['src/bin/animanager']
)
