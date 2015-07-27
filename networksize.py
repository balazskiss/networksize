import random
import sys
import snap
from abc import ABCMeta
from random import randint
import csv
import time

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
        return len(self.getConnectedNodes(node)) # FIX THIS!!!!!!!!!!!!!!!!!!!!!!
        iterator = self.graph.GetNI(node)
        return iterator.GetDeg()

class RandomWalkerDelegate:

    def __init__(self):
        pass

    def returnedToStartNode(self, step):
        pass

class RandomWalker:

    def __init__(self, crawler, estimator, startNode):
        self.delegate = None
        self.crawler = crawler
        self.estimator = estimator
        self.startNode = startNode
        self.network = snap.TNEANet.New()


    def chooseNextNode(self, connectedNodes):
        if len(connectedNodes) == 0:
            return None

        # Weighted Random Walk
        rnd = random.random()
        rnd = randint(0,100000) / 100000.0
        psum = 0.0
        for neighbour in connectedNodes:
            w_edge = self.estimator.getEdgeWeight(self.currentNode, neighbour)
            w_node = self.estimator.getNodeWeight(self.currentNode)
            p = w_edge / w_node
            # p = 1.0 / len(connectedNodes)
            psum += p
            if rnd <= psum:
                return neighbour
        return connectedNodes[0]

        # Simple Random Walk
        randomIndex = randint(0, len(connectedNodes)-1)
        nextNode = connectedNodes[randomIndex]
        return nextNode


    def walk(self):
        self.step = 0
        self.currentNode = self.startNode
        while True:
            node = self.currentNode
            connectedNodes = self.crawler.getConnectedNodes(node)

            # Choose next node
            self.currentNode = self.chooseNextNode(connectedNodes)

            if self.currentNode == self.startNode :
                if self.delegate != None:
                    self.delegate.returnedToStartNode(self.step)
                self.step = 0

            self.step += 1

        print ""


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

class Experiment(RandomWalkerDelegate):
    def __init__(self, graph, name):
        self.returnTimes = []
        self.graph = graph
        self.name = name

        snap.PrintInfo(self.graph, "Network Info")

        self.outputFile = self.name + ".csv"

        if self.outputFile is not None:
            with open(self.outputFile, 'w') as csvfile:
                fieldnames = ['Return N', 'Steps', 'Return Avg', 'Estimate']
                self.writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                self.writer.writeheader()

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

    def __updateProgress(self, progress):
        print '\r[{0}] {1}%'.format('#'*(progress/10), progress),

    def run(self):
        self.crawler = SnapGraphCrawler(self.graph)
        self.estimator = EdgeEstimator(self.crawler)
        self.startNode = self.crawler.getHighestDegreeNode()
        print "Starting from node " + str(self.startNode) + " (degree:" + str(self.crawler.getDegreeOfNode(self.startNode)) + ")"
        walker = RandomWalker(self.crawler, self.estimator, self.startNode)
        walker.delegate = self
        walker.walk()

    # Walker Delegate

    def returnedToStartNode(self, step):
        self.returnTimes.append(step)
        returnTimeAverage = sum(self.returnTimes)/len(self.returnTimes)
        estimate = returnTimeAverage * (self.estimator.getNodeWeight(self.startNode)/2)

        self.__updateProgress(len(self.returnTimes)/10)

        with open(self.outputFile, 'a') as csvfile:
            fieldnames = ['Return N', 'Steps', 'Return Avg', 'Estimate']
            self.writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            field1 = len(self.returnTimes)
            field2 = step
            field3 = returnTimeAverage
            field4 = estimate
            self.writer.writerow({'Return N': field1, 'Steps': field2, 'Return Avg': field3, 'Estimate': field4})


if __name__ == '__main__':
    random.seed(time.time())

    # Generates an Erdos-Renyi random graph
    n1 = snap.GenRndGnm(snap.PNEANet, 1000, 32000, False)

    i = 1
    while i<=10:
        print("Experiment "+str(i))
        Experiment(n1, "randomgraph"+str(i)).run()
        i+=1


    # Generates a random scale-free, undirected graph using the Geometric Preferential Attachment model
    # Rnd = snap.TRnd();
    # n2 = snap.GenGeoPrefAttach(1000, 10000, 0.25, Rnd)
    # exp2 = Experiment(n2, "geoprefattach")
    # exp2.run()

    # Generates an undirected graph with a power-law degree distribution using Barabasi-Albert model
    # Rnd = snap.TRnd();
    # n3 = snap.GenPrefAttach(1000, 10000, Rnd)
    # exp3 = Experiment(n3, "barabasi")
    # exp3.visualiseGraph("prefattch.png", "prefattach")
    # exp3.run()


    #JUNKKKKKKK

    # def __addNode(self, node):
    #     try:
    #         self.network.AddNode(node)
    #     # Ignores if node already exists
    #     except RuntimeError:
    #         pass