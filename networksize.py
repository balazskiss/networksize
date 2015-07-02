import random
import sys
import snap
from abc import ABCMeta
from random import randint
import csv

class GraphCrawler:
    __metaclass__ = ABCMeta

    def getRandomStartingNode(self):
        return None

    def getConnectedNodes(self, node):
        return []

    def getDegreeOfNode(self, node):
        return 0


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

    def getDegreeOfNode(self, node):
        iterator = self.graph.GetNI(node)
        return iterator.GetDeg()

class RandomWalker:

    def __init__(self, crawler, outputFile=None):
        self.crawler = crawler
        self.network = snap.TNEANet.New()
        self.outputFile = outputFile

        if self.outputFile is not None:
            with open(self.outputFile, 'w') as csvfile:
                fieldnames = ['step', 'node', 'nodes', 'edges']
                self.writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                self.writer.writeheader()

    def __addNode(self, node):
        try:
            self.network.AddNode(node)
        # Ignores if node already exists
        except RuntimeError:
            pass

    def __updateProgress(self, progress):
        print '\r[{0}] {1}%'.format('#'*(progress/10), progress),

    def __output(self):
        if self.outputFile is not None:
            with open(self.outputFile, 'a') as csvfile:
                fieldnames = ['step', 'node', 'nodes', 'edges']
                self.writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                step = self.step
                node = self.currentNode
                nodes = self.network.GetNodes()
                edges = self.network.GetEdges()
                self.writer.writerow({'step': self.step, 'node': self.currentNode, 'nodes': nodes, 'edges': edges})

    def chooseNextNode(self, connectedNodes):
        if len(connectedNodes) == 0:
            return None

        # Simple Random Walk
        randomIndex = randint(0, len(connectedNodes)-1)
        nextNode = connectedNodes[randomIndex]
        return nextNode


    def walk(self, steps):
        self.returns = 0
        self.startNode = self.crawler.getRandomStartingNode()
        self.currentNode = self.startNode
        for self.step in range(0, steps):
            node = self.currentNode
            self.__addNode(node)
            connectedNodes = self.crawler.getConnectedNodes(node)
            for connectedNode in connectedNodes:
                self.__addNode(connectedNode)
                self.network.AddEdge(node, connectedNode)

            self.__output()
            self.__updateProgress(int(float(self.step+1)/steps*100.0))

            # Choose next node
            self.currentNode = self.chooseNextNode(connectedNodes)

            if self.currentNode == self.startNode :
                print "Return!"
                self.returns += 1
                nodeEstimate = self.__getNodeEstimate(self.step, self.startNode, self.returns)
                print nodeEstimate

        print ""


    def __getEdgeWeight(self, u, v):
        return 1/self.crawler.getDegreeOfNode(u) + 1/self.crawler.getDegreeOfNode(v)

    def __getVertexWeight(self, u):
        sum = 1
        for neighbour in self.crawler.getConnectedNodes(u):
            sum += 1/self.crawler.getDegreeOfNode(neighbour)
        return sum

    def __getEdgeProbability(self, u, v):
        return self.__getEdgeWeight(u, v) / self.__getVertexWeight(u)

    def __getNodeEstimate(self, time, node, nReturns):
        print "time: " + str(time)
        print "n Returns: " + str(nReturns)
        nodeEstimate = (time * self.__getVertexWeight(node)) / (2 * nReturns)
        return nodeEstimate



class Experiment:
    def __init__(self, graph, name):
        self.graph = graph
        self.name = name

    def printGraphInfo(self, file):
        print("Printing Graph Info")
        snap.PrintInfo(self.graph, "Python type PNGraph", file, True)

    def printFullGraphInfo(self, file):
        print("Printing Full Graph Info")
        snap.PrintInfo(self.graph, "Python type PNGraph", file, False)

    def plotDegreeDistribution(self, file):
        print("Plotting Degree Distribution")
        snap.PlotOutDegDistr(self.graph, file, "Network - out-degree Distribution")

    def visualiseGraph(self, file, title):
        snap.DrawGViz(self.graph, snap.gvlDot, file, title)

    def run(self, steps):
        crawler = SnapGraphCrawler(self.graph)
        walker = RandomWalker(crawler, self.name+'.csv')
        walker.walk(steps)

if __name__ == '__main__':
    # Generates an Erdos-Renyi random graph
    # n1 = snap.GenRndGnm(snap.PNEANet, 10000, 1000000)
    # exp1 = Experiment(n1, "randomgraph")
    # exp1.run()

    # # Generates a random scale-free, undirected graph using the Geometric Preferential Attachment model
    # Rnd = snap.TRnd();
    # n2 = snap.GenGeoPrefAttach(10000, 1000000, 0.25, Rnd)
    # exp2 = Experiment(n2, "geoprefattach")
    # exp2.run()
    #
    # Generates an undirected graph with a power-law degree distribution using Barabasi-Albert model
    Rnd = snap.TRnd();
    n3 = snap.GenPrefAttach(100, 1000, Rnd)
    exp3 = Experiment(n3, "barabasi")
    exp3.run(10000)