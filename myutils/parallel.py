# from multiprocess import Pool
# from typing import Iterable, Callable
#
# from myutils import chained
#
#
#
# def map_parallel(*functions : Callable) -> Callable[[Iterable], Iterable]:
#     def _chain(source):
#         return chained(source, *functions)
#     def _inner(input : Iterable):
#         with Pool() as p:
#             return p.map(_chain, input)
#     return _inner