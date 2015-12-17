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


def test_get_set_default_backend():
    """Testing get/set default_backend"""
    reload(supycache) # - re-init
    from supycache.backends import DictCache
    assert(supycache.default_backend == None)
    assert(isinstance(supycache.get_default_backend(), DictCache))
    assert(isinstance(supycache.default_backend, DictCache))
    new_backend = DictCache()
    supycache.set_default_backend(new_backend)
    assert(supycache.get_default_backend() is new_backend)
    assert(supycache.default_backend is new_backend)

class TestCacheDecorators(unittest.TestCase):
    """ Test the CacheDecorators
    """

    def setUp(self):
        from supycache.backends import DictCache
        self.backend = DictCache()
        supycache.default_backend = self.backend

    def tearDown(self):
        self.backend.clear()

    def test_missing_options(self):
        """ missing option
        """
        with self.assertRaises(KeyError) as context:
            @supycache.supycache()
            def simple_function():
                return 'dummy'

        self.assertTrue('expecting one of' in context.exception.message)


    def test_do_not_ignore_errors(self):
        """ do not ignore errors
        """
        from supycache.backends import DictCache

        class TestException(Exception):
            pass

        class DummyBackend:
            config = {}

            def raise_exc(self, *args):
                """dummy function to raise exception, used later"""
                raise TestException()

        backend = DummyBackend()
        supycache.set_default_backend(backend) # override setUp()

        @supycache.supycache(cache_key='simple_key', ignore_errors=False)
        def simple_function():
            return 'simple_value'

        # - test exception in get() with ignore_errors=False
        with self.assertRaises(TestException) as context:
            backend.get = backend.raise_exc
            simple_function()

        # - test exception in set() with ignore_errors=False
        with self.assertRaises(TestException) as context:
            backend.get = lambda key: None
            backend.set = backend.raise_exc
            simple_function()

        # - test exception in delete() with ignore_errors=False
        with self.assertRaises(TestException) as context:
            backend.delete = backend.raise_exc
            simple_function()


    def test_decorator_for_cache_key_cache_miss(self):
        """ caching a simple key on a cache miss
        """
        @supycache.supycache(cache_key='simple_key')
        def simple_function():
            return 'simple_value'

        simple_function()
        self.assertTrue(self.backend.get('simple_key') == 'simple_value')

    def test_decorator_for_cache_key_cached(self):
        """ caching a simple key and return from cache
        """

        @supycache.supycache(cache_key='simple_key')
        def simple_function(call_count):
            return '%d:cached_value' % call_count

        simple_function(1)
        self.assertTrue(self.backend.get('simple_key') == '1:cached_value')

        simple_function(2)
        self.assertTrue(self.backend.get('simple_key') == '1:cached_value')

        simple_function(3)
        self.assertTrue(self.backend.get('simple_key') == '1:cached_value')


    def test_decorator_for_cache_key_positional_args(self):
        """ caching a key built from positional arguments and returning from cache
        """

        @supycache.supycache(cache_key='{0}')
        def simple_function(x, y):
            return '%d:cached_value' % y

        simple_function('key', 1)
        self.assertTrue(self.backend.get('key') == '1:cached_value')

        simple_function('key', 2)
        self.assertTrue(self.backend.get('key') == '1:cached_value')

        simple_function('new_key', 3)
        self.assertTrue(self.backend.get('new_key') == '3:cached_value')


    def test_decorator_for_cache_key_keyword_args(self):
        """ caching a key built from keyword arguments and returning from cache
        """

        @supycache.supycache(cache_key='{somearg}')
        def simple_function(call_count, somearg):
            return '%d:cached_value' % call_count

        simple_function(1, somearg='key')
        self.assertTrue(self.backend.get('key') == '1:cached_value')

        simple_function(2, somearg='key')
        self.assertTrue(self.backend.get('key') == '1:cached_value')

        simple_function(3, somearg='new_key')
        self.assertTrue(self.backend.get('new_key') == '3:cached_value')


    def test_decorator_for_cache_key_multi_args_simple(self):
        """ caching a key built from both positional and keyword arguments and returning from cache
        """

        @supycache.supycache(cache_key='{0}_{keyword}')
        def simple_function(positional, call_count, keyword=''):
            return '%d:cached_value' % call_count

        simple_function('some', 1, keyword='key')
        self.assertTrue(self.backend.get('some_key') == '1:cached_value')

        simple_function('some', 2, keyword='key')
        self.assertTrue(self.backend.get('some_key') == '1:cached_value')

        simple_function('some_other', 1, keyword='new_key')
        self.assertTrue(self.backend.get('some_other_new_key') == '1:cached_value')


    def test_decorator_for_cache_key_multi_args_complex_list(self):
        """ caching a key built from elements of a list passed as an argument
        """

        @supycache.supycache(cache_key='{0}_{arglist[0]}')
        def simple_function(positional, call_count, arglist=None):
            return '%d:cached_value' % call_count

        simple_function('some', 1, arglist=['key', 'dummy'])
        self.assertTrue(self.backend.get('some_key') == '1:cached_value')

        simple_function('some', 2, arglist=['key', 'changed'])
        self.assertTrue(self.backend.get('some_key') == '1:cached_value')

        simple_function('some_other', 1, arglist=['new_key', 'dummy'])
        self.assertTrue(self.backend.get('some_other_new_key') == '1:cached_value')

        simple_function('yet_another', 1, arglist=['new_key', 'dummy'])
        self.assertTrue(self.backend.get('yet_another_new_key') == '1:cached_value')


    def test_decorator_for_cache_key_multi_args_complex_dict(self):
        """ caching a key built from elements of a dict passed as an argument
        """

        @supycache.supycache(cache_key='{0}_{argdict[lookup]}')
        def simple_function(positional, call_count, argdict=None):
            return '%d:cached_value' % call_count

        simple_function('some', 1, argdict={'lookup' : 'key'})
        self.assertTrue(self.backend.get('some_key') == '1:cached_value')

        simple_function('some', 2, argdict={'lookup' : 'key'})
        self.assertTrue(self.backend.get('some_key') == '1:cached_value')

        simple_function('some_other', 1, argdict={'lookup' : 'new_key'})
        self.assertTrue(self.backend.get('some_other_new_key') == '1:cached_value')


    def test_decorator_for_cache_key_multi_args_complex_object(self):
        """ caching a key built from attributes of an object passed as an argument
        """

        @supycache.supycache(cache_key='{0}_{arg.name}')
        def simple_function(positional, call_count, arg):
            return '%d:cached_value' % call_count

        class DummyArg:
            def __init__(self, value):
                self.name = value

        simple_function('some', 1, arg=DummyArg('key'))
        self.assertTrue(self.backend.get('some_key') == '1:cached_value')

        simple_function('some', 2, arg=DummyArg('key'))
        self.assertTrue(self.backend.get('some_key') == '1:cached_value')

        simple_function('some_other', 1, arg=DummyArg('new_key'))
        self.assertTrue(self.backend.get('some_other_new_key') == '1:cached_value')


    def test_decorator_for_expire_key_with_cached_key(self):
        """ expire a simple key which exists in cache
        """
        @supycache.supycache(cache_key='simple_key')
        def simple_function():
            return 'simple_value'

        @supycache.supycache(expire_key='simple_key')
        def simple_expiry():
            return 'ignored_value'

        simple_function()
        self.assertTrue(self.backend.get('simple_key') == 'simple_value')

        simple_expiry()
        self.assertFalse(bool(self.backend.get('simple_key')))


    def test_decorator_for_expire_key_with_non_cached_key(self):
        """ expire a simple key with does not exist in cache
        """

        @supycache.supycache(cache_key='simple_key')
        def simple_function():
            return 'simple_value'

        @supycache.supycache(expire_key='simple_key')
        def simple_expiry():
            return 'ignored_value'

        simple_function()
        self.assertTrue(self.backend.get('simple_key') == 'simple_value')

        simple_expiry()
        self.assertFalse(bool(self.backend.get('simple_key')))
        self.assertFalse(bool(self.backend.get('simple_key')))


    def test_decorator_for_expire_key_positional_args(self):
        """ expire a key built from positional arguments
        """

        @supycache.supycache(cache_key='{0}')
        def simple_function(x, y):
            return 'cached_value'

        @supycache.supycache(expire_key='{0}')
        def simple_expiry(x, y):
            return 'ignored_value'

        simple_function('simple_key', 1)
        self.assertTrue(self.backend.get('simple_key') == 'cached_value')

        simple_expiry('simple_key', 'dummy')
        self.assertFalse(bool(self.backend.get('simple_key')))
