#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from collections import defaultdict
from .base import BaseCache


class DictCache(BaseCache):

    def __init__(self, config=None):
        super(DictCache, self).__init__(config)
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = defaultdict(lambda: ('', 0)) \
                if self.config.get('max_age') else defaultdict(str)
        return self._data

    def get(self, key):
        if self.config.get('max_age'):
            value, expiry_time = self.data[key]
            if time.time() > expiry_time:
                self.delete(key)
                raise KeyError(key)
        else:
            value = self.data[key]
        return value

    def set(self, key, value):
        max_age = self.config.get('max_age')
        if max_age:
            _, expiry_time = self.data[key]
            if expiry_time == 0:
                # ie: if we got the default value
                expiry_time = time.time() + max_age
            self.data[key] = (value, expiry_time)
        else:
            self.data[key] = value

    def delete(self, key):
        del(self.data[key])

    def clear(self):
        return self.data.clear()
