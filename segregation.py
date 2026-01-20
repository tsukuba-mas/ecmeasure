import networkx as nx

def ratio_edges_to_outside(
    G: nx.DiGraph, 
    community: set[int]
) -> float:
    ## Return the ratio of edges whose target is outside of `community` to whose sources is in `community`.
    edges = G.edges(community)
    to_others = len([(a, b) for (a, b) in edges if b not in community])
    return to_others / len(list(edges))
