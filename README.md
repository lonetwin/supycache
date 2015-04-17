# supycache
Simple yet capable caching decorator for python

## what is supycache ?
supycache is a decorator that automates the caching of the return values of expensive functions, either in memory or on a cache server such as [`memcached`] or [`redis`].

Additionally, it provides a way to ensure that the return values are cached either _independently_, _partially dependent_ or _completely dependent_ on the arguments/keyword arguments passed to the function. This is different from other similar caching decorators, for instance, [`functools.lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache) which is *wholly* dependent on all the arguments passed to the function and require that the arguments are hashable.

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

@supycache(cache_key='result')   # Cache the sum of x and y *independent* the values of x and y
def cached_sum(x, y):
    return x + y

print cached_sum(1, 1)    # prints ...ehe, lets see ...umm, 2 ?
2
print cached_sum(1, 2)    # prints 2 again ! something's not right
2
print supycache.default_backend.get('result')  # prints 2
2
```

So then you do:

```python

@supycache(cache_key='{0} and {1}')   # build the cache key dependent on the positional args
def cached_sum(x, y):
    return x + y
```

If that format specification for the `cache_key` looks familiar, you've discovered the _*secret*_ of supycache !

```python

@supycache(backend=memcached_backend, cache_key='{0}_{kw[foo]}_{obj.x}')
def custom_key_built_from_args(positional, kw=None, obj=None):
    # now, supycache will build the `cache_key` from the arguments passed and
    # use the memcached_backend instance to `set` the key with the return value
    # of this function
    return 'cached'
```

The _*secret*_ of supycache is quite simple -- it calls `.format()` on the `cache_key/expire_key` with the passed `args` and `kwargs` to build the actual key. Additionaly the `backend` interface is abstarcted out neatly so that backends can be swapped out without too much hassle ...and yeah, the decorator accepts more than just `cache_key`.

Right now though, this project has only the code and tests, no docs (or even docstrings !). I'll be adding them soon. If interested take a look at the tests to see the typical usage and try it out. Feedback, bug reports and pull requests would be great !

[`memcached`]: http://memcached.org/
[`redis`]: http://redis.io/
