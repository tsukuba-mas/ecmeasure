import networkx as nx

def get_edges_from_nodes(G, nodes) -> list[tuple[int, int]]:
    if type(G) == nx.DiGraph:
        return G.edges(nodes)
    else:
        # Because RustworkX does not provide G.edges(nodes) like above...
        return [(u, v) for (u, v) in G.edge_list() if u in nodes]

def ratio_edges_to_outside(
    G: nx.DiGraph, 
    community: set[int]
) -> float:
    ## Return the ratio of edges whose target is outside of `community` to whose sources is in `community`.
    edges = get_edges_from_nodes(G, community)
    to_others = len([(a, b) for (a, b) in edges if b not in community])
    return to_others / len(list(edges))
