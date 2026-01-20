import networkx as nx

def get_network_stable(time: int) -> nx.DiGraph:
    # If the network does not change...
    G = nx.DiGraph()
    G.add_nodes_from(range(5))
    G.add_edges_from([
        (0, 1), 
        (1, 2), (2, 1),
        (3, 4), (4, 3),
    ])
    return G

def get_network_time_change(time: int) -> nx.DiGraph:
    # If the network varies
    if time > 0:
        return get_network_stable(time)
    else:
        G = nx.DiGraph()
        G.add_nodes_from(range(3))
        G.add_edges_from([
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
        ])
        return G

OPHISTS = {
    0: [0.8,  1.0,  0.5,  0.45, 0.45],
    1: [0.76, 0.8,  0.7,  0.4,  0.2],
    2: [0.75, 0.76, 0.74, 0.35, 0.25],
    3: [0.75, 0.75, 0.75, 0.3, 0.3],
}

BELHISTS = {
    0: ['1000', '0010', '0001', '0010', '0010'],
    1: ['0100', '0011', '0001', '0011', '0001'],
    2: ['0010', '0001', '0001', '0001', '0001'],
    3: ['0001', '0001', '0001', '0001', '0001'],
}