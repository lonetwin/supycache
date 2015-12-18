supycache
=========

Simple yet capable caching decorator for python

Source code: https://github.com/lonetwin/supycache

Install using pip: ``pip install supycache`` or download from https://pypi.python.org/pypi/supycache

What is supycache ?
-------------------

``supycache`` is a decorator that enables caching of return values for
time-consuming functions, either in memory or on a cache server such as
`memcached <http://memcached.org/>`_ or `redis <http://redis.io/>`_.

The cache keys can either be *indedependent* or dependent (completely or
*partially*) on the arguments passed to the function.

This is **different** from other similar caching decorators, for
instance,
`functools.lru_cache <https://docs.python.org/3/library/functools.html#functools.lru_cache>`_
which is dependent on all the arguments passed to the function and
requires the arguments to be hashable.

If you use the default cache backend (ie: `supycache.backends.DictCache`), you
can also provide an age for the cached values

Here's an example of how you might use ``supycache``

.. code:: python

    import time
    import supycache

    @supycache.supycache(cache_key='result', max_age=5)
    def execute_expensive():
        print 'original function called'
        time.sleep(15)
        return 42

    print execute_expensive()  # This will take 15 seconds to execute ...
    original function called
    42
    print execute_expensive()  # ...not this tho', because the value is cached ...
    42
    print supycache.default_backend.get('result') # ..keyed as `result`
    42
    time.sleep(5)              # wait for the cache to expire...
    execute_expensive()        # This will again take 15 seconds to execute ...
    original function called
    42
    print execute_expensive()  # ...not this tho', because the value is re-cached ...
    42


Sometimes you might want to be aware of the arguments that are passed to
the function:

.. code:: python


    @supycache(cache_key='sum_of_{0}_and_{1}')   # Cache the sum of x and y creating a
    def cached_sum(x, y):                        # key based on the arguments passed
        return x + y

    print cached_sum(28, 14)
    42
    print supycache.default_backend.get('sum_of_28_and_14')
    42

You can also create the key based on **partial arguments** or on the
``attributes``/``items`` within the arguments.

.. code:: python


    class User:
        def __init__(self, name, session_key):
            self.name = name
            self.session_key = session_key

    @supycache(cache_key='{user_obj.name}')   # build the cache key dependent on *just*
    def get_username(user_obj):               # the `.name` attribute
        time.sleep(15)
        return user_obj.name

    a = User(name='steve', session_key='0123456789')
    b = User(name='steve', session_key='9876543210') # same name, different session

    print get_username(user_obj=a)   # This will take 15 seconds to execute ...
    steve
    print get_username(user_obj=a)   # ...not this tho'...
    steve
    print get_username(user_obj=b)   # ...and neither will this !
    steve


    @supycache(cache_key='{choices[0]}_{menu[lunch]}')         # build the cache
    def supersized_lunch(ignored, choices=None, menu=None):    # key dependent on
        time.sleep(15)                                         # partial arguments
        return 'You get a %s %s' % (choices[-1], menu['lunch'])

    menu = {'breakfast' : 'eggs',
            'lunch'     : 'pizza',
            'dinner'    : 'steak'}

    sizes = ['small', 'medium', 'large', 'supersize']

    print supersized_lunch('ignored', choices=sizes, menu=menu)
    You get a supersize pizza       # This will take 15 seconds to execute ...

    print supersized_lunch('changed', choices=sizes, menu=menu)
    You get a supersize pizza       # ...not this tho'...

If that format specification for the ``cache_key`` looks familiar,
you've discovered the *secret* of supycache !

.. code:: python


    @supycache(backend=memcached_backend, cache_key='{0}_{kw[foo]}_{obj.x}')
    def custom_key_built_from_args(positional, kw=None, obj=None):
        # now, supycache will build the `cache_key` from the arguments passed and
        # use the memcached_backend instance to `set` the key with the return value
        # of this function
        return 'cached'

The *secret* of supycache is quite simple -- it calls ``.format()`` on
the ``cache_key/expire_key`` with the passed ``args`` and ``kwargs`` to
build the actual key.

However, if you'd like to have more control on the way the
``cache_key/expire_key`` are created, simply pass in a callable !

.. code:: python

    def extract_path(url=None, *args, **kwags):
        return urlparse.urlparse(url).path

    @supycache(cache_key=extract_path, ignore_errors=False)
    def do_something_with(url):
        # will call `extract_path` at runtime passing `url` as parameter and
        # will use the returned value as the cache key. Also, don't ignore any
        # errors in the entire process if something fails (the default is to
        # ignore any caching errors and just return the result as tho' this
        # function was undecorated.
        return 'cached'

    do_something_with('http://www.example.com/foo/bar')
    'cached'
    supycache.default_backend.get('/foo/bar')
    'cached'


The ``backend`` interface is abstarcted out neatly so that backends can be
swapped out without too much hassle. As long as the passed in object has a
``get()``, ``set()`` and ``delete()`` methods, it can be passed to
``supycache`` as a backend or can be set as the ``default_backend``.


Right now though, this project has only the code and tests, no docs
(barring some docstrings !). I'll be adding them soon. If interested take a
look at the tests to see the typical usage and try it out. Feedback, bug
reports and pull requests would be great !

Help required
-------------

I would really appreciate any help you could offer, not just in implementation
but also in validating the packaging and distribution of this module via pypi
since I've not distributed any packages before.

Besides that I plan on adding a few more things:

    * Ability to specify a ``max_age`` for all backends.
    * I'm not sure whether I am doing the right thing for the not the packaging
      of the memcached dependency. I'd like to automatically include the
      support for ``memcached`` or ``redis`` backends if the python memcached
      or redis modules are installed.
    * logging support

