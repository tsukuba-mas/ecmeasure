from ecmeasure.utils import NetworkWrapper
import igraph as ig

class IGraphWrapper(NetworkWrapper):
    def getWCC(self):
        return list(set(c) for c in ig.Graph.components(self.G, mode='weak'))

    def getSCC(self):
        return list(set(c) for c in ig.Graph.components(self.G, mode='strong'))

    def getCNM(self):
        return list(set(c) for c in ig.Graph.community_fastgreedy(self.G.as_undirected()).as_clustering())

    def getEdgesBetween(self, sources, targets=None):
        if targets:
            return self.G.es.select(_source_in=sources, _target_in=targets)
        else:
            return self.G.es.select(_source_in=sources)