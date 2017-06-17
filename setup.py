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

from setuptools import find_packages, setup

setup(
    name='animanager',
    version='0.10.3',
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
        'apsw',
        'tabulate',
        'wcwidth',
        'mir.anidb==1.0.1',
        'mir.cp==1.0.0',
        'mir.sqlqs==0.4.0',
        'SQLAlchemy==1.1.10',
    ],
    entry_points={
        'console_scripts': [
            'animanager = animanager.__main__:main',
        ],
    },
)
