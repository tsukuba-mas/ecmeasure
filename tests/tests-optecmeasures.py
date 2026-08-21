import pytest

from ecmeasure.optecmeasures import ec
from ecmeasure.utils import hamming
from common import *
import igraph as ig

def test_eo_raw():
    def maxd(comp, time):
        xs = [OPHISTS[time][x] for x in comp]
        return max(xs) - min(xs)

    # Only {1, 2} is ec
    assert ec(
        tmax=3,
        hom_threshold=0.1,
        seg_threshold=0.5,
        readgr=lambda t: ig.Graph.from_networkx(get_network_stable(t)),
        maxd=maxd,
    ) == 1

    info = ec(
        tmax=3,
        hom_threshold=0.1,
        seg_threshold=0.5,
        readgr=lambda t: ig.Graph.from_networkx(get_network_stable(t)),
        maxd=maxd,
        verbose=True,
    )
    assert info.ec == [{1, 2}]

def test_eb_raw():
    def maxd(comp, time):
        xs = [BELHISTS[time][x] for x in comp]
        res = 0
        for x in xs:
            for y in xs:
                res = max(res, hamming(x, y))
        return res

    assert ec(
        tmax=3,
        hom_threshold=0,
        seg_threshold=0.5,
        readgr=lambda t: ig.Graph.from_networkx(get_network_time_change(t)),
        maxd=maxd,
    ) == 2

    res = ec(
        tmax=3,
        hom_threshold=0,
        seg_threshold=0.5,
        readgr=lambda t: ig.Graph.from_networkx(get_network_time_change(t)),
        maxd=maxd,
        verbose=True,
    ).ec
    expected = [{1, 2}, {3, 4}]
    assert all(x in expected for x in res)
    assert all(x in res for x in expected)

 