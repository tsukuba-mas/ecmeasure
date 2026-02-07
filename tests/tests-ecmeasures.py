import pytest

from ecmeasure.ecmeasures import eo_raw, eb_raw
from ecmeasure.homogeneity import max_opinion_distance, max_belief_distance
from ecmeasure.segregation import ratio_edges_to_outside
from ecmeasure.reinforcement import is_opinion_getting_closer, is_belief_getting_closer, nx_scc_wrapper
from common import *

def test_eo_raw():
    # Only {1, 2} is ec
    assert eo_raw(
        time=3,
        is_homogeneous=lambda x: x <= 0.1,
        is_segregated=lambda x: x <= 0.5,
        is_reinforcing=is_opinion_getting_closer,
        get_network_at_t=get_network_stable,
        get_opinions_at_t=lambda time: OPHISTS[time],
        segregation=ratio_edges_to_outside,
        mo=max_opinion_distance,
        get_communities=nx_scc_wrapper,
    ) == 1

    info = eo_raw(
        time=3,
        is_homogeneous=lambda x: x <= 0.1,
        is_segregated=lambda x: x <= 0.5,
        is_reinforcing=is_opinion_getting_closer,
        get_network_at_t=get_network_stable,
        get_opinions_at_t=lambda time: OPHISTS[time],
        segregation=ratio_edges_to_outside,
        mo=max_opinion_distance,
        get_communities=nx_scc_wrapper,
        verbose=True,
    )
    assert info.ec == [{1, 2}]

def test_eb_raw():
    assert eb_raw(
        time=3,
        is_homogeneous=lambda x: x <= 0,
        is_segregated=lambda x: x <= 0.5,
        is_reinforcing=is_belief_getting_closer,
        get_network_at_t=get_network_time_change,
        get_belief_at_t=lambda time: BELHISTS[time],
        segregation=ratio_edges_to_outside,
        mb=max_belief_distance,
        get_communities=nx_scc_wrapper,
    ) == 2

    info = eb_raw(
        time=3,
        is_homogeneous=lambda x: x <= 0,
        is_segregated=lambda x: x <= 0.5,
        is_reinforcing=is_belief_getting_closer,
        get_network_at_t=get_network_time_change,
        get_belief_at_t=lambda time: BELHISTS[time],
        segregation=ratio_edges_to_outside,
        mb=max_belief_distance,
        get_communities=nx_scc_wrapper,
        verbose=True,
    )
    assert info.ec == [{1, 2}, {3, 4}]
    

