import snap
from abc import ABCMeta
from random import randint
import urllib2
import json

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
        iterator = self.graph.GetNI(node)
        deg2 = iterator.GetOutDeg()
        return deg2

class RemoteGraphCrawler(GraphCrawler):

    def __init__(self, url):
        self.url = url

    def getRandomNode(self):
        url = self.url+"/randomNode"
        resp = urllib2.urlopen(url).read()
        dict = json.loads(resp)
        return int(dict["result"])

    def getHighestDegreeNode(self):
        url = self.url+"/highestDegreeNode"
        resp = urllib2.urlopen(url).read()
        dict = json.loads(resp)
        return int(dict["result"])

    def getConnectedNodes(self, node):
        url = self.url+"/connectedNodes/"+str(node)
        resp = urllib2.urlopen(url).read()
        dict = json.loads(resp)
        return dict["result"]

    def getDegreeOfNode(self, node):
        url = self.url+"/degreeOfNode/"+str(node)
        resp = urllib2.urlopen(url).read()
        dict = json.loads(resp)
        return int(dict["result"])
