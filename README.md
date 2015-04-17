# supycache
Simple yet capable caching using decorators for python code

```python

from supycache import supycache

# This will cache the return value of the `cache_this` function in memory
# using the `supycache.DictCache` backend

@supycache(cache_key='simple_cache')
def cache_this(x, y):
    return x + y
    
# ie: now if you call
print cache_this(1, 1)
# you will always get 2 ...but then ...supycache is *NOT* memoization
# because after the first call, you'll also get 2 for
print cache_this(1, 2)

# So, yeah, supycache provides caching not memoization, so what ? 
# well, supycache is much more than simple caching decorators out there because ...

@supycache(backend=memcached_backend, cache_key='{0}_{kw[foo]}_{obj.x}')
def custom_key_built_from_args(positional, kw=None, obj=None):
    # now, supycache will build the `cache_key` from the arguments passed and
    # use the memcached_backend instance to `set` the key with the return value
    # of this function
    return 'cached'
```

The `magic` of supycache is quite simple -- it calls `.format()` on the `cache_key/expire_key` with the passed `args` and `kwargs` to build the actual key. Additionaly the `backend` interface is abstarcted out neatly so that backends can be swapped out without too much hassle.

Right now, this project has only the code and tests, no docs (or even docstrings !). I'll be adding them soon. If interested take a look at the tests to see the typical usage and try it out. Feedback, bug reports and pull requests would be great !

