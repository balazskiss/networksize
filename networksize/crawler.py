import snap
from abc import ABCMeta
from random import randint

class GraphCrawler:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def getRandomNode(self):
        return None

    def getHighestDegreeNode(self):
        return None

    def getConnectedNodes(self, node):
        return []

    def getDegreeOfNode(self, node):
        return 0


class SnapGraphCrawler(GraphCrawler):

    def __init__(self, graph):
        self.graph = graph

    def getRandomNode(self):
        return randint(0, self.graph.GetNodes()-1)

    def getHighestDegreeNode(self):
        return snap.GetMxDegNId(self.graph)

    def getConnectedNodes(self, node):
        nodeIterator=self.graph.GetNI(node)
        outNodes = []
        for n in range(0,nodeIterator.GetOutDeg()):
            nodeId = nodeIterator.GetOutNId(n)
            outNodes.append(nodeId)
        return outNodes

    def getDegreeOfNode(self, node):
        # deg1 =  len(self.getConnectedNodes(node)) # FIX THIS!!!!!!!!!!!!!!!!!!!!!!
        iterator = self.graph.GetNI(node)
        deg2 = iterator.GetOutDeg()
        return deg2