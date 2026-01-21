import pytest

from ecmeasure.segregation import ratio_edges_to_outside
import networkx as nx

def test_ratio_edges_to_outside():
    G = nx.DiGraph()
    G.add_nodes_from(range(6))
    # The network looks like:
    # 0 --> 123 --> 45
    G.add_edges_from([
        (0, 1),
        (1, 2), (2, 3), (3, 1),
        (3, 4),
        (4, 5), (5, 4)
    ])

    assert abs(ratio_edges_to_outside(G, {0}) - 1.0) <= 1e-5
    assert abs(ratio_edges_to_outside(G, {1, 2, 3}) - 0.25) <= 1e-5
    assert abs(ratio_edges_to_outside(G, {4, 5}) - 0.0) <= 1e-5