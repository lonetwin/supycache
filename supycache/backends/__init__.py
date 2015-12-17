#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings
from .dict_cache import DictCache
from .dict_cache import ExpiringDictCache

try:
    from .memcached import MemcachedCache
except ImportError:
    warnings.warn('missing optional dependency: pylibmc, '
                  'MemcachedCache backend will not be available')
