import pytest

from ecmeasure.homogeneity import max_opinion_distance, max_belief_distance

def test_max_opinion_distance():
    opinions = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    agents = {0}
    assert abs(max_opinion_distance(agents, opinions) - 0.0) <= 1e-5

    agents = {1, 2, 3}
    assert abs(max_opinion_distance(agents, opinions) - 0.2) <= 1e-5

    agents = {a for a in range(11)}
    assert abs(max_opinion_distance(agents, opinions) - 1.0) <= 1e-5

def test_max_belief_distance():
    beliefs = ['01', '10', '11']
    agents = {0}
    assert max_belief_distance(agents, beliefs) == 0
    
    agents = {1, 2}
    assert max_belief_distance(agents, beliefs) == 1

    agents = {0, 1, 2}
    assert max_belief_distance(agents, beliefs) == 2
