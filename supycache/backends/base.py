#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BaseCache(object):  # pragma: no cover

    def __init__(self, config=None):
        self.config = config if config else {}

    def get(self):
        raise NotImplementedError()

    def set(self, key, value):
        raise NotImplementedError()

    def delete(self, key):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()
