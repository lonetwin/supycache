#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .dict_cache import DictCache

try:
    __import__('MemcachedCache', fromlist=['.memcached'], level=1)
except ImportError:
    pass
