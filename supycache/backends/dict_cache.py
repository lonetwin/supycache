#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict

from .base import BaseCache

class DictCache(BaseCache):

    def __init__(self, config=None):
        super(DictCache, self).__init__(config)
        self._data = defaultdict(str)
        self.get = self._data.__getitem__
        self.set = self._data.__setitem__
        self.delete = self._data.__delitem__
        self.clear = self._data.clear
