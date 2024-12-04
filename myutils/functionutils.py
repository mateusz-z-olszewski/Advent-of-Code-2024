import itertools
import functools
import builtins

from typing import *


def map(f: Callable, *iterables: Iterable) -> Union[map, Callable[..., map]]:
    if len(iterables) == 0:
        return lambda *_iterables: builtins.map(f, *_iterables)
    else:
        return builtins.map(f, *iterables)


def filter(f: Callable, iterable: Iterable = None) -> Union[filter, Callable[..., filter]]:
    if iterable is None:
        return lambda _iterable: builtins.filter(f, _iterable)
    else:
        return builtins.filter(f, iterable)


_missing = object()
def reduce(f: Callable, iterable: Iterable = None, initial=_missing) -> Union[filter, Callable[..., filter]]:
    if iterable is None:
        if initial is _missing:
            return lambda _iterable: functools.reduce(f, _iterable)
        else:
            return lambda _iterable: functools.reduce(f, _iterable, initial)
    else:
        if initial is _missing:
            return functools.reduce(f, iterable)
        else:
            return functools.reduce(f, iterable, initial)


def chained(source: Iterable, f1: Callable, *fs: Callable) -> ...:
    out = f1(source)
    for f in fs:
        out = f(out)
    return out

def partial(function: Callable, *bound: Any) -> Any:
    return lambda *args: function(*bound + args)