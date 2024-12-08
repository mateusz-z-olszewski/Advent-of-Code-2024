from itertools import groupby
from types import NoneType
from typing import Callable, Iterable, TypeVar, Iterator, MutableSequence, Generic, Sequence, Collection
from _operator import sub
from collections import deque


T = TypeVar('T')
KT = TypeVar('KT')
VT = TypeVar('VT')
KTX = TypeVar('KTX')
VTX = TypeVar('VTX')
F = TypeVar('F')


def merge_dicts(
        *dicts : dict[KT, VT],
        merger : Callable[[VT | NoneType], F] = sum,
        optional: bool = False
) -> dict[KT, F]:
    assert len(dicts) > 0
    return {
        k: merger(*[d.get(k) for d in dicts])
        for k in dicts[0].keys()
        if optional or all(k in d for d in dicts[1:])
    }


def transpose(*iterables : Iterable):
    return list(zip(iterables))


def identity(t: T) -> T:
    return t


def dictchange(
        k: Callable[[KT], KTX]=identity,
        v: Callable[[VT], VTX]=identity
) -> Callable[[dict[KT, VT]], dict[KTX, VTX]]:

    return lambda d : {k(key) : v(value) for key, value in d.items()}



def dictmap(f : Callable[[KT, VT], F]) -> Callable[[dict[KT, VT]], Iterable[F]]:
    return lambda d: (f(k, v) for k, v in d.items())


def groupby_to_dict(iterable):
    return {k : tuple(v) for k, v in groupby(iterable)}


def count_bool(iterable: Iterable[bool]) -> int:
    return sum(map(int, iterable))


def diff(l : list[int], diff_function=sub, gap=1):
    return map(lambda i: diff_function(l[i], l[i - gap]), range(gap, len(l)))


def safe_line_split(input: str) -> list[str]:
    return input.strip().split("\n")


def consume(iterable: Iterator) -> None:
    deque(iterable, maxlen=0)


CollT = type[MutableSequence, Generic]
def split_multiple(input : str, *patterns : str | None, collections:Sequence[CollT]=(list,), continue_collections:CollT=tuple, atom_f=None):
    """
    Note: degree (depth) of a plural split is the number of patterns. The result will be a collection of collections
    of ... of items, for a total of `depth` levels of nesting. Types of the most outer collections are lists. If
    the list of collections is exhausted, it will be continued using the other keyword argument.
    :param input: Input string to be split
    :param patterns: Simple strings that are going to split the input
    :param collections: list of iterable types
    :param continue_collections: iterable type
    :param atom_f: function to be applied to every atom - each item at largest depth. If is None, atoms are unchanged.
    """
    if len(patterns) == 0: raise Exception("Cannot split on no patterns.")
    if len(patterns) == 1:
        t = collections[0] if collections else continue_collections
        if atom_f is None:
            out = input.split(patterns[0])
            return out if t == list else t(*out)
        else:
            return t(atom_f(atom) for atom in input.split(patterns[0]))
    pattern, *remaining = patterns
    if collections:
        t, *collections = collections
    else:
        t = continue_collections
    return t(split_multiple(
        s,
        *remaining,
        collections=collections,
        continue_collections=continue_collections,
        atom_f=atom_f
    ) for s in input.split(pattern))



def cartesian_power(input : Collection, n: int, start: list = None):
    """
    Very fast cartesian power implementation. Warning: it returns *the same list every single time*. This means it
    cannot be converted to a list (or other collection) directly. It should be iterated over instead
    :param input:
    :param n:
    :param start:
    :return:
    """

    if start is None: start = []
    if n > 1:
        for i in input:
            start.append(i)
            yield from cartesian_power(input, n - 1, start=start)
            start.pop()
    elif n == 1:
        for i in input:
            start.append(i)
            yield start
            start.pop()
    else:
        raise Exception(f"{n} is not a valid power!")
    return

#if __name__ == '__main__':
    #consume(map(print, cartesian_power(('*', '+', '||'), 5)))