from ecmeasure.utils import NetworkWrapper
import networkx as nx

class NetworkXWrapper(NetworkWrapper):
    def getWCC(self):
        return list(nx.weakly_connected_components(self.G))

    def getSCC(self):
        return list(nx.strongly_connected_components(self.G))

    def getCNM(self):
        return list(nx.community.greedy_modularity_communities(self.G.to_undirected()))

    def getEdgesBetween(self, sources, targets=None):
        if targets:
            return list(nx.edge_boundary(self.G, sources, targets))
        else:
            return list(nx.edge_boundary(self.G, sources, self.G.nodes))