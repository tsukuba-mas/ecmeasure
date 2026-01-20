import pytest

from reinforcement import is_opinion_getting_closer, is_belief_getting_closer, nx_scc_wrapper
from homogeneity import max_opinion_distance, max_belief_distance
from common import *

def test_is_opinion_getting_closer():
    assert is_opinion_getting_closer(
        {0}, 3, 
        get_opinions_at_t=lambda x: OPHISTS[x],
        get_network_at_t=get_network_stable,
        get_communities=nx_scc_wrapper,
        mo=max_opinion_distance,
    )
    assert is_opinion_getting_closer(
        {1, 2}, 3, 
        get_opinions_at_t=lambda x: OPHISTS[x],
        get_network_at_t=get_network_stable,
        get_communities=nx_scc_wrapper,
        mo=max_opinion_distance,
    )
    # As between t=0 and t=1, opinions are not reinforced
    assert not is_opinion_getting_closer(
        {3, 4}, 3, 
        get_opinions_at_t=lambda x: OPHISTS[x],
        get_network_at_t=get_network_stable,
        get_communities=nx_scc_wrapper,
        mo=max_opinion_distance,
    )

    assert is_opinion_getting_closer(
        {0}, 3, 
        get_opinions_at_t=lambda x: OPHISTS[x],
        get_network_at_t=get_network_time_change,
        get_communities=nx_scc_wrapper,
        mo=max_opinion_distance,
    )
    assert is_opinion_getting_closer(
        {1, 2}, 3, 
        get_opinions_at_t=lambda x: OPHISTS[x],
        get_network_at_t=get_network_time_change,
        get_communities=nx_scc_wrapper,
        mo=max_opinion_distance,
    )
    assert is_opinion_getting_closer(
        {3, 4}, 3, 
        get_opinions_at_t=lambda x: OPHISTS[x],
        get_network_at_t=get_network_time_change,
        get_communities=nx_scc_wrapper,
        mo=max_opinion_distance,
    )

def test_is_belief_getting_closer():
    assert is_belief_getting_closer(
        {0}, 3, 
        get_beliefs_at_t=lambda x: BELHISTS[x],
        get_network_at_t=get_network_stable,
        get_communities=nx_scc_wrapper,
        mb=max_belief_distance,
    )
    assert is_belief_getting_closer(
        {1, 2}, 3, 
        get_beliefs_at_t=lambda x: BELHISTS[x],
        get_network_at_t=get_network_stable,
        get_communities=nx_scc_wrapper,
        mb=max_belief_distance,
    )
    # As between t=0 and t=1, beliefs are not reinforced
    assert not is_belief_getting_closer(
        {3, 4}, 3, 
        get_beliefs_at_t=lambda x: BELHISTS[x],
        get_network_at_t=get_network_stable,
        get_communities=nx_scc_wrapper,
        mb=max_belief_distance,
    )

    assert is_belief_getting_closer(
        {0}, 3, 
        get_beliefs_at_t=lambda x: BELHISTS[x],
        get_network_at_t=get_network_time_change,
        get_communities=nx_scc_wrapper,
        mb=max_belief_distance,
    )
    assert is_belief_getting_closer(
        {1, 2}, 3, 
        get_beliefs_at_t=lambda x: BELHISTS[x],
        get_network_at_t=get_network_time_change,
        get_communities=nx_scc_wrapper,
        mb=max_belief_distance,
    )
    assert is_belief_getting_closer(
        {3, 4}, 3, 
        get_beliefs_at_t=lambda x: BELHISTS[x],
        get_network_at_t=get_network_time_change,
        get_communities=nx_scc_wrapper,
        mb=max_belief_distance,
    )