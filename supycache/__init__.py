#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
supycache - Simple yet capable caching decorator for python.

https://github.com/lonetwin/supycache
https://supycache.readthedocs.org/en/latest/
"""

__author__ = "Steven Fernandez <steve@lonetwin.net>"
__license__ = "MIT"
__version__ = '0.1.1'

from functools import wraps

from .backends import DictCache
from .cdf import CacheDecoratorFactory

default_backend = None

def get_default_backend():
    """Returns the currently configured `default_backend`.

    The ``default_backend`` is a ``supycache.DictCache`` instance if not set.
    Use ``supycache.set_default_backend`` to change this. A ``backend`` is any
    (caching) object that has at least the `.get()``, ``.set()`` and
    ``.delete()`` methods.
    """
    global default_backend
    if not default_backend:
        default_backend = DictCache()
    return default_backend

def supycache(**options):
    """Decorates a function for caching/expiring cache depending on arguments.

    This is the primary interface to use `supycache`. This decorator accepts
    the following parameters:

    - ``cache_key`` : Either a simple string, a format string or callable used
                      to create the key used for caching the result of the
                      function being decorated.
                      This key will be resolved at run-time and would be
                      evaluated against/with the parameters passed to the
                      function being decorated.

    - ``expire_key`` : Either a simple string, a format string or callable used
                       to create the key that would be expired before the
                       decorated function is called.
                       This key will be resolved at run-time and would be
                       evaluated against/with the parameters pass to the
                       function being decorated.

    - `ignore_errors` : A boolean to indicate whether errors in getting,
                        setting or expiring cache should be ignored or
                        re-raised on being caught.
    """
    def prepare_inner(function):
        recognized_options = {'cache_key',
                              'expire_key',
                              'ignore_errors',
                             }

        if recognized_options.isdisjoint(options):
            raise KeyError('expecting one of %s as an argument' % \
                ','.join(recognized_options))

        cdf = CacheDecoratorFactory(options.get('backend', get_default_backend()), **options)
        return cdf(function)
    return prepare_inner
