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

    def walk(self, steps):
        self.startNode = crawler.getRandomStartingNode()
        self.currentNode = self.startNode
        for self.step in range(0, steps):
            node = self.currentNode
            self.__addNode(node)
            connectedNodes = crawler.getConnectedNodes(node)
            for connectedNode in connectedNodes:
                self.__addNode(connectedNode)
                self.network.AddEdge(node, connectedNode)

            self.__output()
            self.__updateProgress(int(float(self.step+1)/steps*100.0))

            # Choose next node
            if len(connectedNodes) > 0:
                randomIndex = randint(0, len(connectedNodes)-1)
                nextNode = connectedNodes[randomIndex]
                self.currentNode=nextNode

        print ""



def printGraphInfo(graph, file):
    print("Printing Graph Info")
    snap.PrintInfo(graph, "Python type PNGraph", file, True)

def printFullGraphInfo(graph, file):
    print("Printing Full Graph Info")
    snap.PrintInfo(graph, "Python type PNGraph", file, False)

def plotDegreeDistribution(graph, file):
    print("Plotting Degree Distribution")
    snap.PlotOutDegDistr(graph, file, "Network - out-degree Distribution")

def visualiseGraph(graph, file, title):
    snap.DrawGViz(graph, snap.gvlDot, file, title)

if __name__ == '__main__':
    # Generates an Erdos-Renyi random graph
    network = snap.GenRndGnm(snap.PNEANet, 10000, 1000000)
    plotDegreeDistribution(network, "randomgraph")
    crawler = SnapGraphCrawler(network)
    walker = RandomWalker(crawler, 'randomgraph.csv')
    walker.walk(1000)

    # Generates a random scale-free, undirected graph using the Geometric Preferential Attachment model
    Rnd = snap.TRnd();
    UGraph = snap.GenGeoPrefAttach(100, 10, 0.25, Rnd)
    plotDegreeDistribution(UGraph, "scalefree")