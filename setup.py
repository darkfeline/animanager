#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name='animanager',
    version='0.10.2',
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
        'Programming Language :: Python :: 3.5',
    ],

    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=['apsw', 'tabulate'],
    entry_points={
        'console_scripts': [
            'animanager = animanager.__main__:main',
        ],
    },
)
