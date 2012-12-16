#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='Animanager',
    version='0.3',
    description='Anime Manager MySQL frontend application',
    author='Allen Li',
    author_email='darkfeline@abagofapples.com',
    package_dir={'': 'src'},
    packages=['animanager', 'animanager.scene'],
    scripts=['src/bin/animanager']
)
