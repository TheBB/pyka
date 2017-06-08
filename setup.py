#!/usr/bin/env python

from setuptools import setup

setup(
    name='PyKa',
    version='1.0.0',
    description='Python implementation of Kaleidoscope',
    maintainer='Eivind Fonn',
    maintainer_email='evfonn@gmail.com',
    packages=['pyka'],
    entry_points={
        'console_scripts': [
            'pyka=pyka.__main__:main',
        ],
    },
    install_requires=[
        'tatsu',
        'click',
    ]
)
