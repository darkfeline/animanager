# Copyright (C) 2015-2016 Allen Li
#
# This file is part of Animanager.
#
# Animanager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Animanager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Animanager.  If not, see <http://www.gnu.org/licenses/>.

import re
from setuptools import setup, find_packages


def find_version(path):
    with open(path) as f:
        text = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              text, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='animanager',
    version=find_version('animanager/__init__.py'),
    description='Command line program for advanced anime watching management',
    long_description='',
    keywords='',
    url='https://www.felesatra.moe/animanager/',
    author='Allen Li',
    author_email='darkfeline@felesatra.moe',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'apsw~=3.9',
        'tabulate==0.8.1',
        'wcwidth==0.1.7',
        'mir.anidb~=1.0',
        'mir.cp~=1.0',
        'mir.sqlite3m~=1.0',
        'SQLAlchemy~=1.1',
    ],
    entry_points={
        'console_scripts': [
            'animanager = animanager.__main__:main',
        ],
    },
)
