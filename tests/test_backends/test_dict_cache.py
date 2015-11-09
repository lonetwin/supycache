#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import supycache

class TestDictCache(unittest.TestCase):
    """ Test the DictCache backend
    """

    def setUp(self):
        from supycache.backends import DictCache
        self.cache = DictCache()
        supycache.set_default_backend(self.cache)

    def tearDown(self):
        self.cache.clear()

    def test_init(self):
        """Testing DictCache constructor"""
        self.assertTrue(hasattr(self.cache, 'set'))
        self.assertTrue(hasattr(self.cache, 'get'))
        self.assertTrue(hasattr(self.cache, 'clear'))

    def test_methods(self):
        """Testing DictCache methods"""
        self.cache.set('key', 'value')
        self.assertTrue(self.cache.get('key') == 'value')
        self.assertTrue(bool(self.cache.get('non-existent')) == False)
        self.assertTrue(self.cache.clear() == None)
        self.assertTrue(len(self.cache._data) == 0)

