import numpy as np
from functionutils import chained, map


def parse_grid(input: str):
    return chained(input.split(),
        map(list),
        list,
        np.char.array
    )