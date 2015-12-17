#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps


class CacheDecoratorFactory:

    def __init__(self, backend, cache_key='', expire_key='', **other_kwargs):
        self._backend = backend
        self._backend.config.update(other_kwargs)

        if cache_key:
            self.key = cache_key
            self._wrapped = self._caching_wrapper

        if expire_key:
            self.key = expire_key
            self._wrapped = self._expiry_wrapper

        self.ignore_errors = other_kwargs.get('ignore_errors', True)

    def __call__(self, func):
        return self._wrapped(func)

    def _expiry_wrapper(self, func):
        @wraps(func)
        def cache_deleter(*args, **kwargs):
            key = self.key(*args, **kwargs) if callable(self.key) \
                else self.key.format(*args, **kwargs)
            try:
                self._backend.delete(key)
            except:
                if not self.ignore_errors:
                    raise

            return func(*args, **kwargs)
        return cache_deleter

    def _caching_wrapper(self, func):
        @wraps(func)
        def cache_setter(*args, **kwargs):
            result = None
            key = self.key(*args, **kwargs) if callable(self.key) \
                else self.key.format(*args, **kwargs)
            try:
                result = self._backend.get(key)
            except:
                if not self.ignore_errors:
                    raise

            if not result:
                result = func(*args, **kwargs)
                try:
                    self._backend.set(key, result)
                except:
                    if not self.ignore_errors:
                        raise

            return result
        return cache_setter
