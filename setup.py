#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" supycache -  Simple yet capable caching decorator for python

Source code: https://github.com/lonetwin/supycache
"""

from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'supycache',
    version = '0.3.0',
    description = 'Simple yet capable caching decorator for python',
    long_description = long_description,
    url = 'https://github.com/lonetwin/supycache',
    author = 'Steven Fernandez',
    author_email = 'steve@lonetwin.net',
    license = 'MIT',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        ],
    keywords = 'cache, caching, memcached, redis, memoize, memoization',
    packages = find_packages(exclude=['contrib', 'docs', 'tests*']),
)

