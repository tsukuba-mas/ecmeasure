import networkx as nx
import pandas as pd
from typing import Callable
from homogeneity import max_opinion_distance, max_belief_distance
from functools import cache

@cache
def nx_scc_wrapper(G: nx.DiGraph) -> list[set[int]]:
    ## Wrapper of `nx.strongly_connected_components`.
    ## This function is memoized.
    return list(nx.strongly_connected_components(G))

def is_decreasing(xs: list[float]) -> bool:
    ## Returns `True` if xs[0] >= xs[1] >= ... >= xs[-1]; returns `False` otherwise.
    for i in range(1, len(xs)):
        if xs[i-1] < xs[i]:
            return False
    return True

def is_opinion_getting_closer(
    community: set[int], 
    time: int, 
    *,
    get_opinions_at_t: Callable[int, list[float]],
    get_network_at_t: Callable[int, nx.DiGraph],
    mo: Callable[[set[int], list[float]], float],
    get_communities: Callable[nx.DiGraph, list[set[int]]],
) -> bool:
    ## Returns `True` if opinions within `community` are getting closer.
    ## This is tested by for the maximal time window whose upper bound is `time` and
    ## `community` exists, the maximal distance between opinions decreases.
    G = get_network_at_t(time)
    now = time - 1
    mos = [mo(community, get_opinions_at_t(time))]
    while 0 <= now:
        G = get_network_at_t(now)
        past_comp = get_communities(get_network_at_t(now))
        if community not in past_comp:
            break
        past_ops = get_opinions_at_t(now)
        mos.append(mo(community, past_ops))
        now = now - 1
    # Reverse `mos` as mos[0] is at `time`, mos[1] is at `time-1`, etc.
    return is_decreasing(mos[::-1])

def is_belief_getting_closer(
    community: set[int], 
    time: int, 
    *,
    get_beliefs_at_t: Callable[int, list[str]],
    get_network_at_t: Callable[int, nx.DiGraph],
    mb: Callable[[set[int], list[str]], int],
    get_communities: Callable[nx.DiGraph, list[set[int]]],
) -> bool:
    ## Returns `True` if opinions within `community` are getting closer.
    ## This is tested by for the maximal time window whose upper bound is `time` and
    ## `community` exists, the maximal distance between opinions decreases.
    G = get_network_at_t(time)
    now = time - 1
    mbs = [mb(community, get_beliefs_at_t(time))]
    while 0 <= now:
        G = get_network_at_t(now)
        past_comp = get_communities(get_network_at_t(now))
        if community not in past_comp:
            break
        past_ops = get_beliefs_at_t(now)
        mbs.append(mb(community, past_ops))
        now = now - 1
    return is_decreasing(mbs[::-1])
