import random
import sys
import snap
from abc import ABCMeta
from random import randint


class GraphCrawler:
    __metaclass__ = ABCMeta

    def getRandomStartingNode(self):
        return None

    def getConnectedNodes(self, node):
        return []


class SnapGraphCrawler(GraphCrawler):

    def __init__(self, graph):
        self.graph = graph

    def getRandomStartingNode(self):
        return randint(0, self.graph.GetNodes()-1)

    def getConnectedNodes(self, node):
        nodeIterator=self.graph.GetNI(node)
        outNodes = []
        for n in range(0,nodeIterator.GetOutDeg()):
            nodeId = nodeIterator.GetOutNId(n)
            outNodes.append(nodeId)
        return outNodes

class RandomWalker:

    def __init__(self, crawler):
        self.crawler = crawler
        self.network = snap.TNEANet.New()

    def __addNode(self, node):
        try:
            self.network.AddNode(node)
        # Ignores if node already exists
        except RuntimeError:
            pass

    def walk(self, steps):
        node = crawler.getRandomStartingNode()
        for step in range(0, steps):
            print "step " + str(step)
            print "  node #" + str(node)
            self.__addNode(node)
            connectedNodes = crawler.getConnectedNodes(node)
            for connectedNode in connectedNodes:
                self.__addNode(connectedNode)
                self.network.AddEdge(node, connectedNode)

            print "  nodes: " + str(self.network.GetNodes())
            print "  edges: " + str(self.network.GetEdges())

            # snap.DrawGViz(self.network, snap.gvlDot, "evolution/step"+str(step)+".png", "Step "+str(step))

            if len(connectedNodes) > 0:
                randomIndex = randint(0, len(connectedNodes)-1)
                nextNode = connectedNodes[randomIndex]
                node=nextNode

if __name__ == '__main__':
    network = snap.GenRndGnm(snap.PNEANet, 10000, 1000000)
    # snap.PlotOutDegDistr(network, "example", "Network - out-degree Distribution")
    crawler = SnapGraphCrawler(network)
    walker = RandomWalker(crawler)
    walker.walk(100)