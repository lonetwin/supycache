# supycache
Simple yet capable caching decorator for python

## what is supycache ?
supycache is a decorator that automates caching of return values for expensive functions, either in memory or on a cache server such as [`memcached`] or [`redis`]. The cache keys can either be _indedependent_ or dependent (completely or _partially_) of the arguments passed to the function.

This is **different** from other similar caching decorators, for instance, [`functools.lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache) which is dependent on all the arguments passed to the function and requires the arguments to be hashable.

Here's an example of how you might use `supycache`
```python
import time
import supycache

@supycache.supycache(cache_key='result')
def execute_expensive():
    time.sleep(15)
    return 42

print execute_expensive()  # This will take 15 seconds to execute ...
42
print execute_expensive()  # ...not this tho', because the value is cached ...
42
print supycache.default_backend.get('result') # ..keyed as `result`
42
```

However, you might want to be aware of the arguments that are passed to the function:

```python

@supycache(cache_key='sum_of_{0}_and_{1}')   # Cache the sum of x and y creating a
def cached_sum(x, y):                        # key based on the arguments passed
    return x + y
```

You can also create the key based on **partial arguments** or on the `attributes`/`items` within the arguments.

```python

class User:
    def __init__(self, name, session_key):
        self.name = name
        self.session_key = session_key

@supycache(cache_key='{user_obj.name}')   # build the cache key dependent on *just*
def get_username(user_obj):               # the `.name` attribute
    time.sleep(15)
    return user_obj.name

a = User(name='steve', session_key='0123456789')
b = User(name='steve', session_key='9876543210')

print get_username(user_obj=a)   # This will take 15 seconds to execute ...
steve
print get_username(user_obj=a)   # ...not this tho'...
steve
print get_username(user_obj=b)   # ...and neither will this !


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

```

If that format specification for the `cache_key` looks familiar, you've discovered the _secret_ of supycache !

```python

@supycache(backend=memcached_backend, cache_key='{0}_{kw[foo]}_{obj.x}')
def custom_key_built_from_args(positional, kw=None, obj=None):
    # now, supycache will build the `cache_key` from the arguments passed and
    # use the memcached_backend instance to `set` the key with the return value
    # of this function
    return 'cached'
```

The _secret_ of supycache is quite simple -- it calls `.format()` on the `cache_key/expire_key` with the passed `args` and `kwargs` to build the actual key. Additionaly the `backend` interface is abstarcted out neatly so that backends can be swapped out without too much hassle ...and yeah, the decorator accepts more than just `cache_key`.

Right now though, this project has only the code and tests, no docs (or even docstrings !). I'll be adding them soon. If interested take a look at the tests to see the typical usage and try it out. Feedback, bug reports and pull requests would be great !

[`memcached`]: http://memcached.org/
[`redis`]: http://redis.io/
