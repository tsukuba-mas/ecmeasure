def hamming(b1: str, b2: str) -> int:
    ## Return the Hamming distance between two beliefs `b1` and `b2`.
    return sum([x1 != x2 for (x1, x2) in zip(b1, b2)])

def is_decreasing(xs: list[float]) -> bool:
    ## Returns `True` if xs[0] >= xs[1] >= ... >= xs[-1]; returns `False` otherwise.
    for i in range(1, len(xs)):
        if xs[i-1] < xs[i]:
            return False
    return True