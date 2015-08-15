class Estimator:
    def __init__(self, crawler):
        self.crawler = crawler

    def randomWalkType(self):
        return "weighted"

    def getEdgeWeight(self, u, v, du=None, dv=None):
        pass

    def getNodeWeight(self, u, du=None, connectedNodesWithDegrees=None):
        pass

class EdgeEstimator(Estimator):
    def randomWalkType(self):
        return "simple"

    def getEdgeWeight(self, u, v, du=None, dv=None):
        return 1.0

    def getNodeWeight(self, u, du=None, connectedNodesWithDegrees=None):
        return self.crawler.getDegreeOfNode(u)


class NodeEstimator(Estimator):
    def getEdgeWeight(self, u, v, du=None, dv=None):
        if du == None:
            du = self.crawler.getDegreeOfNode(u)
        if dv == None:
            dv = self.crawler.getDegreeOfNode(v)
        return (1.0 / du) + (1.0 / dv)

    def getNodeWeight(self, u, du=None, connectedNodesWithDegrees=None):
        if du == None:
            du = self.crawler.getDegreeOfNode(u)
        if connectedNodesWithDegrees == None:
            connectedNodesWithDegrees = self.crawler.getConnectedNodesWithDegrees(u)
        wsum = 0.0
        for node in connectedNodesWithDegrees:
            wsum += self.getEdgeWeight(u, node, du, connectedNodesWithDegrees[node])
        return wsum