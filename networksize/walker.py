import snap
import random
from random import randint

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
        self.visitedNodes = set()

    def chooseNextNodeRandomlyUsingWeights(self):
        connectedNodesWithDegrees = self.crawler.getConnectedNodesWithDegrees(self.currentNode)
        du = len(connectedNodesWithDegrees)

        # Weighted Random Walk
        rnd = random.random()
        psum = 0.0
        w_node = self.estimator.getNodeWeight(self.currentNode, du, connectedNodesWithDegrees)
        for neighbour in connectedNodesWithDegrees:
            dv = connectedNodesWithDegrees[neighbour]
            w_edge = self.estimator.getEdgeWeight(self.currentNode, neighbour, du, dv)
            p = w_edge / w_node
            psum += p
            if rnd <= psum:
                return neighbour
        return None

    def chooseNextNodeRandomly(self):
        connectedNodes = self.crawler.getConnectedNodes(self.currentNode)

        # Simple Random Walk
        randomIndex = randint(0, len(connectedNodes)-1)
        nextNode = connectedNodes[randomIndex]
        return nextNode

    def chooseNextNode(self):
        randomWalkType = self.estimator.randomWalkType()
        if randomWalkType == "simple":
            return self.chooseNextNodeRandomly()
        elif randomWalkType == "weighted":
            return self.chooseNextNodeRandomlyUsingWeights()

    def walk(self):
        self.running = True
        self.step = 0
        self.currentNode = self.startNode
        self.visitedNodes.add(self.currentNode)
        while self.running:
            # Choose next node
            self.currentNode = self.chooseNextNode()
            self.visitedNodes.add(self.currentNode)
            self.step += 1

            if self.currentNode == self.startNode :
                if self.delegate != None:
                    self.delegate.returnedToStartNode(self.step)
                self.step = 0



    def stop(self):
        self.running = False