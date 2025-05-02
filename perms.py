from typing import Sequence, TypeVar, List, TypeVar, ParamSpec, Callable
from datetime import datetime
from functools import wraps
from time import perf_counter


P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")


def contiguous_segments(seq: Sequence[T]) -> List[Sequence[T]]:
    # All contiguous slices of lengths 1..len(seq).
    n = len(seq)
    return [seq[i : i + k] for k in range(1, n + 1) for i in range(n - k + 1)]


# def multislice(seq: Sequence[T], cuts: Sequence[int]) -> List[List[T]]:
#     n = len(seq) + 1
#     cut_points = sorted({c for c in cuts if 0 <= c < n})
#     boundaries = [0] + [c + 1 for c in cut_points] + [n]
#     result = [list(seq[a:b]) for a, b in zip(boundaries, boundaries[1:])]
#     return [x for x in result if x]  # kludge!!!!


# This is about 20% faster than multislice()
def multislice_fast(seq: Sequence[T], cuts: Sequence[int]) -> List[List[T]]:
    n = len(seq)
    cut_set = {c for c in cuts if 0 <= c < n}
    out: List[List[T]] = []
    curr: List[T] = []

    for i, x in enumerate(seq):
        curr.append(x)
        if i in cut_set:
            out.append(curr)
            curr = []

    if curr:
        out.append(curr)

    return out


def foo(seq: Sequence[T]) -> List[List[List[T]]]:
    idxs = list(range(len(seq)))
    bar = contiguous_segments(idxs)
    return [multislice_fast(seq, cuts) for cuts in bar]


print(foo(["J", "O", "H", "N"]))


for size in [1, 2, 3, 10, 200, 300, 400, 500]:
    print(f"Size is {size}; calculating...")
    start_time = perf_counter()
    input_seq = list(range(1, size + 1))
    if size < 10:
        print(f"\tinput is: {input_seq}")
    else:
        print("\tinput is: (omitting input because of size)")
    results = foo(input_seq)

    print(f"\tresults ({len(results)}):")

    if len(results) < 10:
        for x in results[0:10]:
            print(f"\t\t{x}")
    else:
        print("\t\t(omitting results because of size)")
    elapsed = (perf_counter() - start_time) * 1000
    print(f"\ttime: {elapsed:.2f} ms")
