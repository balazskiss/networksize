class Estimator:
    def __init__(self, crawler):
        self.crawler = crawler

    def getEdgeWeight(self, u, v):
        pass

    def getNodeWeight(self, u):
        pass

class EdgeEstimator(Estimator):
    def getEdgeWeight(self, u, v):
        return 1.0

    def getNodeWeight(self, u):
        return self.crawler.getDegreeOfNode(u)


class NodeEstimator(Estimator):
    def getEdgeWeight(self, u, v):
        return (1.0 / self.crawler.getDegreeOfNode(u)) + (1.0 / self.crawler.getDegreeOfNode(v))

    def getNodeWeight(self, u):
        neighbours = self.crawler.getConnectedNodes(u)
        wsum = 0
        for neighbour in neighbours:
            wsum += self.getEdgeWeight(u, neighbour)
        return wsum