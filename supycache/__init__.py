#!/usr/bin/env python
# -*- coding: utf-8 -*-

default_backend = None

def get_default_backend():
    return DictCache if default_backend is None else default_backend

from .backends import DictCache
from .cdf import CacheDecoratorFactory

def supycache(**options):
    def prepare_inner(function):
        recognized_options = {'cache_key',
                              'expire_key',
                              'key_creator',
                              }

        if recognized_options.isdisjoint(options):
            raise KeyError('expecting one of %s as an argument' % \
                ','.join(recognized_options))

        cdf = CacheDecoratorFactory(default_backend, **options)
        return cdf(function)
    return prepare_inner
