#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict


class BaseCache(object):
    def __init__(self, config=None):
        self.config = config

    def connect(self):
        raise NotImplementedError()

    def get(self):
        raise NotImplementedError()

    def set(self, key, value):
        raise NotImplementedError()

    def delete(self, key):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()


class DictCache(BaseCache):

    def __init__(self, config=None):
        super(DictCache, self).__init__(config)
        self._data = defaultdict(str)
        self.get = self._data.__getitem__
        self.set = self._data.__setitem__
        self.delete = self._data.__delitem__
        self.clear = self._data.clear
        self.conn = None

    def connect(self, **options):
        self.conn = self._data
