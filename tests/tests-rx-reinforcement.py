import pytest
import numpy as np
import rustworkx as rx

from ecmeasure.rxreinforcement import is_opinion_getting_closer_rx, get_sccs, is_belief_getting_closer_rx
from ecmeasure.homogeneity import max_opinion_distance, max_belief_distance
from common import *

# For long iterations, it is recommended to load the file firstly and 
# build RustworkX network from it. 
# This can be achieved by:
#   np.genfromtxt('path/to/file.csv', delimiter=',', dtype=int)
# for example.
def get_network_stable_rx(time: int):
    sources = np.array([0, 1, 2, 3, 4])
    edges = np.array([
        [1, 2, 1, 4, 3]
        for _ in range(4)
    ])
    G = rx.PyDiGraph()
    G.add_nodes_from(range(5))
    G.add_edges_from_no_data(zip(sources, edges[time]))
    return G

def get_network_time_change_rx(time: int):
    sources = np.array([0, 1, 2, 3, 4])
    edges = np.array([
        [1, 2, 1, 4, 3] if t > 0 else [1, 2, 3, 4, 0]
        for t in range(4)
    ])
    G = rx.PyDiGraph()
    G.add_nodes_from(range(5))
    G.add_edges_from_no_data(zip(sources, edges[time]))
    return G

def test_is_opinion_getting_closer_rx():
    assert is_opinion_getting_closer_rx(
        {0}, 3, 
        get_opinions_at_t=lambda x: OPHISTS[x],
        get_network_at_t=get_network_stable_rx,
        get_communities=get_sccs,
        mo=max_opinion_distance,
    )
    assert is_opinion_getting_closer_rx(
        {1, 2}, 3, 
        get_opinions_at_t=lambda x: OPHISTS[x],
        get_network_at_t=get_network_stable_rx,
        get_communities=get_sccs,
        mo=max_opinion_distance,
    )
    # As between t=0 and t=1, opinions are not reinforced
    assert not is_opinion_getting_closer_rx(
        {3, 4}, 3, 
        get_opinions_at_t=lambda x: OPHISTS[x],
        get_network_at_t=get_network_stable_rx,
        get_communities=get_sccs,
        mo=max_opinion_distance,
    )

    assert is_opinion_getting_closer_rx(
        {0}, 3, 
        get_opinions_at_t=lambda x: OPHISTS[x],
        get_network_at_t=get_network_time_change_rx,
        get_communities=get_sccs,
        mo=max_opinion_distance,
    )
    assert is_opinion_getting_closer_rx(
        {1, 2}, 3, 
        get_opinions_at_t=lambda x: OPHISTS[x],
        get_network_at_t=get_network_time_change_rx,
        get_communities=get_sccs,
        mo=max_opinion_distance,
    )
    # As between t=0 and t=1, opinions are not reinforced
    assert is_opinion_getting_closer_rx(
        {3, 4}, 3, 
        get_opinions_at_t=lambda x: OPHISTS[x],
        get_network_at_t=get_network_time_change_rx,
        get_communities=get_sccs,
        mo=max_opinion_distance,
    )

def test_is_belief_getting_closer_rx():
    assert is_belief_getting_closer_rx(
        {0}, 3, 
        get_beliefs_at_t=lambda x: BELHISTS[x],
        get_network_at_t=get_network_stable_rx,
        get_communities=get_sccs, 
        mb=max_belief_distance,
    )
    assert is_belief_getting_closer_rx(
        {1, 2}, 3, 
        get_beliefs_at_t=lambda x: BELHISTS[x],
        get_network_at_t=get_network_stable_rx,
        get_communities=get_sccs, 
        mb=max_belief_distance,
    )
    # As between t=0 and t=1, beliefs are not reinforced
    assert not is_belief_getting_closer_rx(
        {3, 4}, 3, 
        get_beliefs_at_t=lambda x: BELHISTS[x],
        get_network_at_t=get_network_stable_rx,
        get_communities=get_sccs,
        mb=max_belief_distance,
    )

    assert is_belief_getting_closer_rx(
        {0}, 3, 
        get_beliefs_at_t=lambda x: BELHISTS[x],
        get_network_at_t=get_network_time_change_rx,
        get_communities=get_sccs,
        mb=max_belief_distance,
    )
    assert is_belief_getting_closer_rx(
        {1, 2}, 3, 
        get_beliefs_at_t=lambda x: BELHISTS[x],
        get_network_at_t=get_network_time_change_rx,
        get_communities=get_sccs,
        mb=max_belief_distance,
    )
    assert is_belief_getting_closer_rx(
        {3, 4}, 3, 
        get_beliefs_at_t=lambda x: BELHISTS[x],
        get_network_at_t=get_network_time_change_rx,
        get_communities=get_sccs,
        mb=max_belief_distance,
    )