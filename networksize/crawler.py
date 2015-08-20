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

    def get_random_node(self):
        return None

    def get_highest_degree_node(self):
        return None

    def get_connected_nodes(self, node):
        return []

    def get_degree_of_node(self, node):
        return 0

    def get_connected_nodes_with_degrees(self, node):
        nodes = self.get_connected_nodes(node)
        nodes_dict = {}
        for n in nodes:
            nodes_dict[n] = self.get_degree_of_node(n)
        return nodes_dict


class SnapGraphCrawler(GraphCrawler):

    def __init__(self, graph):
        super(SnapGraphCrawler, self).__init__()
        self.graph = graph

    def get_random_node(self):
        return randint(0, self.graph.GetNodes()-1)

    def get_highest_degree_node(self):
        return snap.GetMxDegNId(self.graph)

    def get_connected_nodes(self, node):
        node_iterator = self.graph.GetNI(node)
        out_nodes = []
        for n in range(0, node_iterator.GetOutDeg()):
            node_id = node_iterator.GetOutNId(n)
            out_nodes.append(node_id)
        return out_nodes

    def get_degree_of_node(self, node):
        iterator = self.graph.GetNI(node)
        out_deg = iterator.GetOutDeg()
        return out_deg


class RemoteGraphCrawler(GraphCrawler):

    def __init__(self, url):
        super(RemoteGraphCrawler, self).__init__()
        self.url = url

    def get_random_node(self):
        url = self.url+"/randomNode"
        resp = urllib2.urlopen(url).read()
        resp_obj = json.loads(resp)
        return int(resp_obj["result"])

    def get_highest_degree_node(self):
        url = self.url+"/highestDegreeNode"
        resp = urllib2.urlopen(url).read()
        resp_obj = json.loads(resp)
        return int(resp_obj["result"])

    @cache
    def get_connected_nodes(self, node):
        url = self.url+"/connectedNodes/"+str(node)
        resp = urllib2.urlopen(url).read()
        resp_obj = json.loads(resp)
        return resp_obj["result"]

    @cache
    def get_degree_of_node(self, node):
        url = self.url+"/degreeOfNode/"+str(node)
        resp = urllib2.urlopen(url).read()
        resp_obj = json.loads(resp)
        return int(resp_obj["result"])

    @cache
    def get_connected_nodes_with_degrees(self, node):
        url = self.url+"/connectedNodesWithDegrees/"+str(node)
        resp = urllib2.urlopen(url).read()
        resp_obj = json.loads(resp)
        result = {}
        for strkey in resp_obj["result"]:
            result[int(strkey)] = resp_obj["result"][strkey]
        return result


class TwitterGraphCrawler(GraphCrawler):

    def __init__(self, consumer_key, consumers_secret, access_token_key, access_token_secret):
        super(TwitterGraphCrawler, self).__init__()
        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumers_secret,
                               access_token_key=access_token_key,
                               access_token_secret=access_token_secret)

    def get_random_node(self):
        return 252636900  # me

    def get_highest_degree_node(self):
        return 252636900
        # return 21447363  # Katy Perry

    @cache
    def get_connected_nodes(self, node):
        followers = None
        while followers is None:
            try:
                followers = self.api.GetFollowerIDs(node)
            except twitter.error.TwitterError:
                sec = self.api.GetSleepTime('/followers/ids')
                time.sleep(sec)
        return followers

    @cache
    def get_degree_of_node(self, node):
        user = self.api.GetUser(node)
        print user.name
        return user.followers_count
