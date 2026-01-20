from typing import Callable
from utils import hamming

def max_opinion_distance(
    community: set[int], 
    opinions: list[float],
) -> float:
    ## Return the maximal distance between opinions within `community`.
    opinion_within_community = [opinions[a] for a in community]
    return max(opinion_within_community) - min(opinion_within_community)

def max_belief_distance(
    community: set[int], 
    beliefs: list[str],
    *,
    distance: Callable[[str, str], int]=hamming,
) -> int:
    ## Return the maximal distance between beliefs within `community`.
    ## The distance between two beliefs can be changed by the optional arument `distance`.
    max_distance = 0
    for a in community:
        for b in community:
            max_distance = max(max_distance, distance(beliefs[a], beliefs[b]))
    return max_distance

