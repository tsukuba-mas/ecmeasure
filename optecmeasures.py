from ecmeasure.utils import VerboseECInfo
from typing import Callable
import igraph as ig

def ec(
        tmax: int, 
        readgr: Callable[[int], ig.Graph], 
        maxd: Callable[[list[int], int], float], 
        seg_threshold: float, 
        hom_threshold: int | float, 
        shortcut=False, 
        verbose=False
):
    components = {}

    # Cache all of the components during the time window [0, tmax]
    for t in range(tmax+1):
        G = readgr(t)
        # components[t] = [set(c) for c in G.as_undirected().community_fastgreedy().as_clustering()]    
        components[t] = [set(c) for c in ig.Graph.components(G, mode='strong')]    

    G = readgr(tmax)
    result = VerboseECInfo([], [], [], [])

    for comp in components[tmax]:
        is_ec = True

        # Homogeneity
        nowh = maxd(comp, tmax)
        if nowh > hom_threshold:
            is_ec = False
            if shortcut:
                continue
        else:
            result.homogeneity.append(comp)

        # Segregation
        edges_from = len(G.es.select(_source_in=comp))
        edges_recc = len(G.es.select(_source_in=comp, _target_in=comp))
        if (edges_from - edges_recc) / edges_from > seg_threshold:
            is_ec = False
            if shortcut:
                continue
        else:
            result.segregation.append(comp)

        # Reinforcement
        beforeh = nowh
        for t in range(tmax-1, -1, -1):
            if comp not in components[t]:
                break
            nowh = maxd(comp, t)
            if nowh < beforeh:
                is_ec = False
                break
            beforeh = nowh

        if is_ec:
            result.ec.append(comp)

    if verbose:
        return result
    else:
        return len(result.ec)



