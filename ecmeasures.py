from ecmeasure.homogeneity import max_opinion_distance, max_belief_distance
from ecmeasure.segregation import ratio_edges_to_outside
from ecmeasure.reinforcement import is_opinion_getting_closer, is_belief_getting_closer, nx_scc_wrapper
import networkx as nx
import pandas as pd
from typing import Callable, NamedTuple

import mentsuyu

# To make the type annotation shorter
CallableReinforcing = Callable[
    [
        set[int], 
        int, 
        Callable[int, list[float]], 
        Callable[int, nx.DiGraph], 
        Callable[[set[int], list[float]], float], 
        Callable[nx.DiGraph, list[set[int]]]
    ],
    bool
]

class VerboseECInfo(NamedTuple):
    ec: list[set[int]]
    homogeneity: list[set[int]]
    segregation: list[set[int]]
    reinforcement: list[set[int]]

def eo_raw(
    time: int,
    *,
    is_homogeneous: Callable[float, bool],
    is_segregated: Callable[float, bool],
    is_reinforcing: CallableReinforcing,
    get_opinions_at_t: Callable[int, list[float]],
    get_network_at_t: Callable[int, nx.DiGraph],
    mo: Callable[[set[int], list[float]], float],
    segregation: Callable[[nx.DiGraph, set[int]], float],
    get_communities: Callable[nx.DiGraph, list[set[int]]],
    verbose: bool=False,
) -> int | VerboseECInfo:
    ## Opinion echo chamber measures (customizable version).
    ## If `verbose` is `False`, only #ec is returned.
    ## Otherwise, other information can be obtained (see `VerboseECInfo`).
    G = get_network_at_t(time)
    opinions = get_opinions_at_t(time)
    info = VerboseECInfo([], [], [], [])
    for community in get_communities(G):
        is_ec = True

        # Homogeneity
        if is_homogeneous(mo(community, opinions)):
            info.homogeneity.append(community)
        else:
            is_ec = False

        # Segregation
        if is_segregated(segregation(G, community)):
            info.segregation.append(community)
        else:
            is_ec = False

        # Reinforcement
        if is_reinforcing(
            community, 
            time,
            get_opinions_at_t=get_opinions_at_t,
            get_network_at_t=get_network_at_t,
            mo=mo,
            get_communities=get_communities,
        ):
            info.reinforcement.append(community)
        else:
            is_ec = False

        # If `community` is an echo chamber, incement `ecs`
        if is_ec:
            info.ec.append(community)
    
    if verbose:
        return info
    else:
        return len(info.ec)

def eb_raw(
    time: int,
    *,
    is_homogeneous: Callable[int, bool],
    is_segregated: Callable[float, bool],
    is_reinforcing: CallableReinforcing,
    get_belief_at_t: Callable[int, list[str]],
    get_network_at_t: Callable[int, nx.DiGraph],
    mb: Callable[[set[str], list[float]], int],
    segregation: Callable[[nx.DiGraph, set[int]], float],
    get_communities: Callable[nx.DiGraph, list[set[int]]],
    verbose: bool=False,
) -> int | VerboseECInfo:
    ## Belief echo chamber measures (customizable version).
    G = get_network_at_t(time)
    beliefs = get_belief_at_t(time)
    info = VerboseECInfo([], [], [], [])
    for community in get_communities(G):
        is_ec = True

        # Homogeneity
        if is_homogeneous(mb(community, beliefs)):
            info.homogeneity.append(community)
        else:
            is_ec = False          

        # Segregation
        if is_segregated(segregation(G, community)):
            info.segregation.append(community)
        else:
            is_ec = False            

        # Reinforcement
        if is_reinforcing(
            community, 
            time,
            get_beliefs_at_t=get_belief_at_t,
            get_network_at_t=get_network_at_t,
            mb=mb,
            get_communities=get_communities,
        ):
            info.reinforcement.append(community)
        else:
            is_ec = False

        # If `community` is an echo chamber, incement `ecs`
        if is_ec:
            info.ec.append(community)

    if verbose:
        return info
    else:
        return len(info.ec)

def eo(
    time: int, 
    exp: str,
    *,
    allowed_opinion_difference: float = 1e-3,
    allowed_outgoing_edge_ratio: float = 0.5,
    opid: int = 0,
    verbose: bool = False,
) -> int | VerboseECInfo:
    ## Opinion echo chamber measure.
    ## This is equivalent to the initially proposed measure.
    ## Note that this measure depends on `mentsuyu` (submodule).
    return eo_raw(
        time=time,
        is_homogeneous=lambda mdo: mdo <= allowed_opinion_difference,
        is_segregated=lambda rat: rat <= allowed_outgoing_edge_ratio,
        is_reinforcing=is_opinion_getting_closer,
        get_opinions_at_t=lambda t: list(mentsuyu.reader.readop(exp=exp, opid=opid).loc[t]),
        get_network_at_t=lambda t: mentsuyu.reader.readgr_nx(tick=t, exp=exp),
        segregation=ratio_edges_to_outside,
        mo=max_opinion_distance,
        get_communities=nx_scc_wrapper,
        verbose=verbose,
    )

def eb(
    time: int, 
    exp: str,
    *,
    allowed_belief_difference: int = 0,
    allowed_outgoing_edge_ratio: float = 0.5,
    verbose: bool = False,
) -> int | VerboseECInfo:
    ## Belief echo chamber measure.
    ## This is equivalent to the initially proposed measure.
    ## Note that this measure depends on `mentsuyu` (submodule).
    return eb_raw(
        time=time,
        is_homogeneous=lambda mdo: mdb <= allowed_belief_difference,
        is_segregated=lambda rat: rat <= allowed_outgoing_edge_ratio,
        is_reinforcing=is_belief_getting_closer,
        get_belief_at_t=lambda t: list(mentsuyu.reader.readbel(exp=exp).loc[t]),
        get_network_at_t=lambda t: mentsuyu.reader.readgr_nx(tick=t, exp=exp),
        segregation=ratio_edges_to_outside,
        mb=max_belief_distance,
        get_communities=nx_scc_wrapper,
        verbose=verbose,
    )
