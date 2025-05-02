from time import perf_counter

from typing import Sequence, TypeVar, List
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from numpy.typing import NDArray

T = TypeVar("T")


def sliding_nonoverlapping_segments_grouped(
    seq: Sequence[T],
) -> List[List[List[T]]]:
    """
    For each k=1..len(seq), return non-overlapping contiguous chunks of length k.

    Example:
      seq = ["J","O","H","N"]
      returns [
        [["J"], ["O"], ["H"], ["N"]],        # k=1
        [["J","O"], ["H","N"]],              # k=2
        [["J","O","H"]],                     # k=3 (tail ["N"] dropped)
        [["J","O","H","N"]],                 # k=4
      ]
    """
    arr: NDArray[np.generic] = np.asarray(seq)
    n = arr.shape[0]
    result: List[List[List[T]]] = []
    for k in range(1, n + 1):
        # full sliding windows of width k, shape (n-k+1, k)
        windows: NDArray[np.generic] = sliding_window_view(arr, window_shape=k)
        # pick every k-th window to avoid overlap
        non_overlap = windows[::k]
        # convert to Python lists; any leftover window shorter than k is never in windows[::k]
        group: List[List[T]] = [w.tolist() for w in non_overlap]
        result.append(group)
    return result


# --- example usage ---
if __name__ == "__main__":
    data = ["J", "O", "H", "N"]
    for group in sliding_nonoverlapping_segments_grouped(data):
        print(group)
    # for size in [1, 2, 3, 10, 100, 200, 300, 400, 500]:
    #     print(f"Size is {size}; calculating...")
    #     start_time = perf_counter()
    #     input_seq = list(range(1, size + 1))
    #     if size < 10:
    #         print(f"\tinput is: {input_seq}")
    #     else:
    #         print("\tinput is: (omitting input because of size)")
    #     results = sliding_contiguous_segments_grouped(input_seq)

    #     print(f"\tresults ({len(results)}):")

    #     if len(results) < 10:
    #         for x in results[0:10]:
    #             print(f"\t\t{x}")
    #     else:
    #         print("\t\t(omitting results because of size)")
    #     elapsed = (perf_counter() - start_time) * 1000
    #     print(f"\ttime: {elapsed:.2f} ms")
