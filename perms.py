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


def multislice(seq: Sequence[T], cuts: Sequence[int]) -> List[List[T]]:
    n = len(seq) + 1
    # keep only valid, unique, sorted cuts
    cut_points = sorted({c for c in cuts if 0 <= c < n})
    # build boundary list: 0, (cut+1)..., n
    boundaries = [0] + [c + 1 for c in cut_points] + [n]
    # zip into (start,end) pairs
    result = [list(seq[a:b]) for a, b in zip(boundaries, boundaries[1:])]
    return [x for x in result if x]  # kludge!!!!


def foo(seq: Sequence[T]) -> List[List[List[T]]]:
    # generate all cut-position lists by slicing the indices
    idxs = list(range(len(seq)))
    start_time = perf_counter()
    bar = contiguous_segments(idxs)
    elapsed_ms = (perf_counter() - start_time) * 1000
    # print(f"contiguous_segments executed in {elapsed_ms:.2f} ms")

    # print(bar)
    return [multislice(seq, cuts) for cuts in bar]


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
