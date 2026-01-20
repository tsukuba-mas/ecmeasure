def hamming(b1: str, b2: str) -> int:
    ## Return the Hamming distance between two beliefs `b1` and `b2`.
    return sum([x1 != x2 for (x1, x2) in zip(b1, b2)])