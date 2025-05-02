from itertools import combinations
from typing import Sequence, TypeVar, Iterator, List, Any
from collections import deque
import numpy as np
from time import perf_counter

T = TypeVar("T")
MAX_RESULTS_TO_PRINT = 50
VERBOSE = True
ARRAY_SIZES = [1, 2, 3, 10, 20, 50, 100, 200, 300, 400, 500]
MAX_CUTS = [0, 1, 2, 3, 4]


def zeros_to_n(n: int) -> np.ndarray[Any, np.dtype[np.int_]]:
    return np.arange(n + 1, dtype=int)


def join_nparray(arr: np.ndarray[Any, np.dtype[Any]]) -> str:
    flat = arr.ravel()
    str_arr = flat.astype(str)
    return ",".join(str_arr)


def cut_np(seq: Sequence[T], num_cuts: int) -> Iterator[List[np.ndarray]]:
    arr = np.asarray(seq)
    n = arr.shape[0]
    if num_cuts < 0 or num_cuts >= n:
        return

    # combinations still in C
    for cp in combinations(range(1, n), num_cuts):
        # np.split returns exactly num_cuts+1 sub‐arrays (views)
        yield list(np.split(arr, cp))


def cumulative_cuts(seq: Sequence[T], max_cuts: int) -> Iterator[List[Sequence[T]]]:
    """
    Generate all ways to cut `seq` into pieces with 0 up to `max_cuts` cuts.
    Yields lists of subsequences for each cut count cumulatively.
    Equivalent to chaining cut(seq, k) for k in 0..max_cuts.
    """
    n = len(seq)
    # no more cuts than possible positions
    max_k = min(max_cuts, n - 1)
    for k in range(max_k + 1):
        yield from cut_np(seq, k)


if not VERBOSE:
    print("      size  max_cuts      time (ms)")

for size in ARRAY_SIZES:
    for max_cuts in MAX_CUTS:
        start_time = perf_counter()
        # input_seq = list(range(1, size + 1))
        input_seq = zeros_to_n(size)

        # results = cumulative_cuts(input_seq, max_cuts)
        results = cut_np(input_seq, max_cuts)

        if VERBOSE:
            print(f"Size is {size}, cuts is {max_cuts}; calculating...")
            results_list = list(results)
            print(f"\tresults ({len(results_list)}):")

            if size < 50:
                for x in results_list[0:MAX_RESULTS_TO_PRINT]:
                    print("\t\t", end="")
                    for y in x:
                        print(f"{join_nparray(y)}", end="  ")
                    print()
                if len(results_list) > MAX_RESULTS_TO_PRINT:
                    print(
                        f"\t\t... and {len(results_list) - MAX_RESULTS_TO_PRINT} more results ..."
                    )
        else:
            deque(cumulative_cuts(input_seq, max_cuts), maxlen=0)

        elapsed = (perf_counter() - start_time) * 1000

        if VERBOSE:
            print(f"\ttime: {elapsed:.2f} ms")
        else:
            print(f"{size!s:>{10}}{max_cuts!s:>{10}}{elapsed:15.2f}")
