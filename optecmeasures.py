from ecmeasure.utils import VerboseECInfo, NetworkWrapper
from typing import Callable

def ec(
        time: int, 
        component: str,
        readgr: Callable[[int], NetworkWrapper], 
        maxd: Callable[[list[int], int], float], 
        seg_threshold: float, 
        hom_threshold: int | float, 
        shortcut=False, 
        verbose=False
) -> int | VerboseECInfo:
    """
    Unified and optimized echo chamber measure.
    This function is defined aiming at improving the performance and 
    unifying the two measures in ecmeasures.py.

    Args:
        time (int): discrete time specifying when this measure is applied
        component (str): string corresponding to component detection algorithm
        readgr (Callable[[int], NetworkWrapper]): a function that returns a network at given time
        maxd (Callable[[list[int], int], float]): a function that returns the maximal distance of
            an attribute of agents (typically opinions or beliefs) in the first argument 
            at given time (second one)
        seg_threshold (float): parameter for the segregation property
        hom_threshold (float or int): parameter for the homogeneity property
        shortcut (bool, default: False): if True, skip testing whether a component satisfies
            all of the properties if it becomes clear that it cannot be an echo chamber.
            Useful only if you want the list of echo chambers or the number of echo chambers.
        verbose (bool, default: False): if True, VerboseECInfo is returned;
            if False, only the number of echo chambers is returned.

    Returns:
        int: if verbose; 
        VerboseECInfo: otherwise.
    """
    components = {}

    # Cache all of the components during the time window [0, time]
    for t in range(time+1):
        G = readgr(t)   
        components[t] = G.getComponents(component)

    G = readgr(time)
    result = VerboseECInfo([], [], [], [])

    for comp in components[time]:
        is_ec = True

        # Homogeneity
        nowh = maxd(comp, time)
        if nowh > hom_threshold:
            is_ec = False
            if shortcut:
                continue
        else:
            result.homogeneity.append(comp)

        # Segregation
        edges_from = len(G.getEdgesBetween(comp))
        edges_recc = len(G.getEdgesBetween(comp, comp))
        if (edges_from - edges_recc) / edges_from > seg_threshold:
            is_ec = False
            if shortcut:
                continue
        else:
            result.segregation.append(comp)

        # Reinforcement
        beforeh = nowh
        for t in range(time-1, -1, -1):
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



