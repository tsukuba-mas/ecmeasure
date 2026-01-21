import rustworkx as rx
import networkx as nx
from functools import cache
from typing import Callable

from ecmeasure.utils import is_decreasing

# RustworkX provides more faster functions than NetworkX.
# In this file, faster reinforcement detection functions are defined.

@cache
def get_sccs(G: rx.PyDiGraph | nx.DiGraph) -> list[set[int]]:
    if type(G) == rx.PyDiGraph:
        return list(rx.strongly_connected_components(G))
    else:
        return list(nx.strongly_connected_components(G))

def is_opinion_getting_closer_rx(
    community: set[int], 
    time: int, 
    *,
    get_opinions_at_t: Callable[int, list[float]],
    get_network_at_t: Callable[int, nx.DiGraph],
    mo: Callable[[set[int], list[float]], float],
    get_communities,
) -> bool:
    ## Returns `True` if opinions within `community` are getting closer.
    ## This is tested by for the maximal time window whose upper bound is `time` and
    ## `community` exists, the maximal distance between opinions decreases.
    now = time - 1
    mos = [mo(community, get_opinions_at_t(time))]
    G = get_network_at_t(time)
    while 0 <= now:
        now_G = get_network_at_t(now)
        if rx.is_isomorphic_node_match(G, now_G, lambda x, y: x == y):
            # if the network is the same as before, sccs should be the same,
            # hence just compute mo and push
            mos.append(mo(community, get_opinions_at_t(now)))
        else:
            # otherwise, since #node is constant,
            # reuse `G` itself
            G = now_G
            past_comp = get_communities(G)
            if community not in past_comp:
                break
            past_ops = get_opinions_at_t(now)
            mos.append(mo(community, past_ops))
        now = now - 1
    # Reverse `mos` as mos[0] is at `time`, mos[1] is at `time-1`, etc.
    return is_decreasing(mos[::-1])

def is_belief_getting_closer_rx(
    community: set[int], 
    time: int, 
    *,
    get_beliefs_at_t: Callable[int, list[str]],
    get_network_at_t: Callable[int, nx.DiGraph],
    mb: Callable[[set[int], list[float]], int],
    get_communities,
) -> bool:
    ## Returns `True` if beliefs within `community` are getting closer.
    ## This is tested by for the maximal time window whose upper bound is `time` and
    ## `community` exists, the maximal distance between beliefs decreases.
    now = time - 1
    mbs = [mb(community, get_beliefs_at_t(time))]
    G = get_network_at_t(time)
    while 0 <= now:
        now_G = get_network_at_t(now)
        if rx.is_isomorphic_node_match(G, now_G, lambda x, y: x == y):
            # if the network is the same as before, sccs should be the same,
            # hence just compute mb and push
            mbs.append(mb(community, get_beliefs_at_t(now)))
        else:
            # otherwise, since #node is constant,
            # reuse `G` itself
            G = now_G
            past_comp = get_communities(G)
            if community not in past_comp:
                break
            past_ops = get_beliefs_at_t(now)
            mbs.append(mb(community, past_ops))
        now = now - 1
    # Reverse `mbs` as mbs[0] is at `time`, mbs[1] is at `time-1`, etc.
    return is_decreasing(mbs[::-1])