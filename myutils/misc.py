from itertools import groupby
from types import NoneType
from typing import Callable, Iterable, TypeVar
from _operator import sub


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


def count(iterable: Iterable[bool]) -> int:
    return sum(map(int, iterable))


def diff(l : list[int], diff_function=sub, gap=1):
    return map(lambda i: diff_function(l[i], l[i - gap]), range(gap, len(l)))


def safe_line_split(input: str) -> list[str]:
    return input.strip().split("\n")