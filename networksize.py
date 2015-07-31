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
        # deg1 =  len(self.getConnectedNodes(node)) # FIX THIS!!!!!!!!!!!!!!!!!!!!!!
        iterator = self.graph.GetNI(node)
        deg2 = iterator.GetOutDeg()
        return deg2

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
        self.running = False


    def chooseNextNode(self, connectedNodes):
        if len(connectedNodes) == 0:
            return None

        # Weighted Random Walk
        rnd = random.random()
        psum = 0.0
        for neighbour in connectedNodes:
            w_edge = self.estimator.getEdgeWeight(self.currentNode, neighbour)
            w_node = self.estimator.getNodeWeight(self.currentNode)
            p = w_edge / w_node
            psum += p
            if rnd <= psum:
                return neighbour
        return connectedNodes[0]

        # Simple Random Walk
        randomIndex = randint(0, len(connectedNodes)-1)
        nextNode = connectedNodes[randomIndex]
        return nextNode


    def walk(self):
        self.running = True
        self.step = 0
        self.currentNode = self.startNode
        while self.running:
            node = self.currentNode
            connectedNodes = self.crawler.getConnectedNodes(node)

            # Choose next node
            self.currentNode = self.chooseNextNode(connectedNodes)

            if self.currentNode == self.startNode :
                if self.delegate != None:
                    self.delegate.returnedToStartNode(self.step)
                self.step = 0

            self.step += 1

    def stop(self):
        self.running = False


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
    def __init__(self, graph, name, returnLimit=0):
        self.returnTimes = []
        self.returnLimit = returnLimit
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
        self.walker = RandomWalker(self.crawler, self.estimator, self.startNode)
        self.walker.delegate = self
        self.walker.walk()

    # Walker Delegate

    def returnedToStartNode(self, step):
        self.returnTimes.append(step)
        returnTimeAverage = sum(self.returnTimes)/len(self.returnTimes)
        estimate = returnTimeAverage * (self.estimator.getNodeWeight(self.startNode)/2)

        with open(self.outputFile, 'a') as csvfile:
            fieldnames = ['Return N', 'Steps', 'Return Avg', 'Estimate']
            self.writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            field1 = len(self.returnTimes)
            field2 = step
            field3 = returnTimeAverage
            field4 = estimate
            self.writer.writerow({'Return N': field1, 'Steps': field2, 'Return Avg': field3, 'Estimate': field4})

        self.__updateProgress(int(float(len(self.returnTimes))/float(self.returnLimit)*100.0))
        if len(self.returnTimes) == self.returnLimit:
            self.walker.stop()


class GraphImporter:
    def __init__(self, file, limit):
        self.file = file
        self.limit = limit
        self.network = snap.TUNGraph.New(1000000, 10000000)

    def addNode(self, network, node):
            try:
                network.AddNode(node)
            # Ignores if node already exists
            except RuntimeError:
                pass

    def addEdge(self, network, node1, node2):
            self.addNode(network, node1)
            self.addNode(network, node2)
            try:
                network.AddEdge(node1,node2)
            # Ignores if node already exists
            except RuntimeError:
                pass

    def importGraph(self):
        print("Importing graph...")
        i = 0
        with open(self.file) as f:
            for line in f:
                nodes = line.split('\t')
                self.addEdge(self.network,int(nodes[0]),int(nodes[1]))
                i+= 1
                if i%1000000 == 0:
                    print(i)
                    snap.PrintInfo(self.network, "Network Info")
                if i==self.limit:
                    break
        print("Graph has been imported")
        snap.PrintInfo(self.network, "Network Info")
        return self.network


if __name__ == '__main__':
    random.seed(time.time())
    Rnd = snap.TRnd();

    # Generates an Erdos-Renyi random graph
    # network = snap.GenRndGnm(snap.PUNGraph, 1000, 5000, False)
    # name = "randomgraph"

    # Generates a random scale-free, undirected graph using the Geometric Preferential Attachment model
    # network = snap.GenGeoPrefAttach(1000, 10000, 0.25, Rnd)
    # name = "geoprefattach"

    # Generates an undirected graph with a power-law degree distribution using Barabasi-Albert model
    # network = snap.GenPrefAttach(1000, 10000, Rnd)
    # name = "barabasi"

    # Twitter network sample
    importer = GraphImporter("/Volumes/Blaze's Disk/twitter/twitter_rv.net", 4561230)
    network = importer.importGraph()
    name="twitter"

    i = 1
    while i<=10:
        print("Experiment "+str(i))
        Experiment(network, name+str(i), 1000).run()
        i+=1




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