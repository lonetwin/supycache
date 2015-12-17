#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from collections import defaultdict
from .base import BaseCache


class DictCache(BaseCache):

    def __init__(self, config=None):
        super(DictCache, self).__init__(config)
        self._data = defaultdict(str)

    def get(self, key):
        return self._data[key]

    def set(self, key, value):
        self._data[key] = value

    def delete(self, key):
        del(self._data[key])

    def clear(self):
        return self._data.clear()


class ExpiringDictCache(DictCache):

    def __init__(self, config=None):
        super(ExpiringDictCache, self).__init__(config)
        self._data = defaultdict(lambda: ('', 0))

    def get(self, key):
        value, expiry_time = self._data[key]
        if time.time() > expiry_time:
            self.delete(key)
            raise KeyError(key)
        return value

    def set(self, key, value):
        max_age = self.config.get('max_age')
        existing_value, expiry = self._data[key]
        if expiry == 0:
            # ie: if we got the default value
            expiry = time.time() + max_age
        self._data[key] = (value, expiry)
