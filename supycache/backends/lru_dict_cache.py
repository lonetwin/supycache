#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict

from .base import BaseCache


class LRUCache(BaseCache):
    """A LRU cache implementation for use with supycache

    Recognizes config parameter `max_items`
    """

    def __init__(self, config=None):
        super(DictCache, self).__init__(config)
        self.data = OrderedDict()

    def get(self, key):
        # - reorder if key in self._data, let KeyError bubble up if not
        value = self.data.pop(key)
        self.data[key] = value
        return value

    def set(self, key, value):
        try:
            self.data.pop(key)
        except KeyError:
            if len(self.data) >= self.config.get('max_items', 32):
                self.data.popitem(last=False)

        self.data[key] = value

    def delete(self, key):
        del(self.data[key])

    def clear(self):
        return self.data.clear()
