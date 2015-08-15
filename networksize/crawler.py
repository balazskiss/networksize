import snap
from abc import ABCMeta
from random import randint
import urllib2
import json
import hermes.backend.dict
import twitter
import time

cache = hermes.Hermes(hermes.backend.dict.Backend)

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

    def getConnectedNodesWithDegrees(self, node):
        nodes = self.getConnectedNodes(node)
        dict = {}
        for n in nodes:
            dict[n] = self.getDegreeOfNode(n)
        return dict


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

    @cache
    def getConnectedNodes(self, node):
        url = self.url+"/connectedNodes/"+str(node)
        resp = urllib2.urlopen(url).read()
        dict = json.loads(resp)
        return dict["result"]

    @cache
    def getDegreeOfNode(self, node):
        url = self.url+"/degreeOfNode/"+str(node)
        resp = urllib2.urlopen(url).read()
        dict = json.loads(resp)
        return int(dict["result"])

    @cache
    def getConnectedNodesWithDegrees(self, node):
        url = self.url+"/connectedNodesWithDegrees/"+str(node)
        resp = urllib2.urlopen(url).read()
        dict = json.loads(resp)
        result = {}
        for strkey in dict["result"]:
            result[int(strkey)]=dict["result"][strkey]
        return result

class TwitterGraphCrawler(GraphCrawler):

    def __init__(self, consumer_key, consumers_secret, access_token_key, access_token_secret):
        self.api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumers_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)

    def getRandomNode(self):
        return 252636900 # me

    def getHighestDegreeNode(self):
        return 252636900
        return 21447363 # Katy Perry

    @cache
    def getConnectedNodes(self, node):
        followers = None
        while followers == None:
            try:
                followers=self.api.GetFollowerIDs(node, total_count=self.getDegreeOfNode(node))
            except twitter.error.TwitterError:
                sec = self.api.GetSleepTime('/followers/ids')
                time.sleep(sec)
        return followers

    @cache
    def getDegreeOfNode(self, node):
        user = self.api.GetUser(node)
        print user.name
        return user.followers_count