import time, types, itertools, inspect
from functools import wraps, partial

from decorator_tools import decorate_classes, decorate_everything

def filter(func, predicate):
    @wraps(func)
    def wrapper(*args, **kargs):
        for result in func(*args, **kwargs):
            if predicate(result):
                yield result
    return wrapper

@filter(partial(isinstance, string))
def test_funct():
    return (3, 4, 'fdsf', 5, 4.9)


