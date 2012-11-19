#!/usr/bin/env python3

from distutils.core import setup

from setup_utils import get_modules
from setup_utils import get_packages
from setup_utils import get_scripts

setup(
    name='Animanager',
    version='0.3',
    description='Anime Manager MySQL frontend application',
    author='Allen Li',
    author_email='darkfeline@abagofapples.com',
    package_dir={'': 'src'},
    py_modules=get_modules('src'),
    packages=get_packages('src'),
    scripts=get_scripts('src/bin')
)
