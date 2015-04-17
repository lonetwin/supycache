#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from .backends import DictCache
from .cdf import CacheDecoratorFactory

default_backend = DictCache()


def supycache(**options):
    def prepare_inner(function):
        @wraps(function)
        def inner(*args, **kwargs):
            return function(*args, **kwargs)

        backend = options.pop('backend', default_backend)
        backend.connect(**options)

        if options.get('cache_key') or options.get('expire_key'):
            cdf = CacheDecoratorFactory(backend, **options)
            wrapper = cdf(function)
        else:
            raise KeyError('supycache expects at least either '
                           '`cache_key` or `expire_key`')

        return wrapper
    return prepare_inner
