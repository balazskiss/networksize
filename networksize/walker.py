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

    def chooseNextNodeRandomlyUsingWeights(self, connectedNodes):
        # Weighted Random Walk
        rnd = random.random()
        psum = 0.0
        w_node = self.estimator.getNodeWeight(self.currentNode)
        for neighbour in connectedNodes:
            w_edge = self.estimator.getEdgeWeight(self.currentNode, neighbour)
            p = w_edge / w_node
            psum += p
            if rnd <= psum:
                return neighbour
        return connectedNodes[0]

    def chooseNextNodeRandomly(self, connectedNodes):
        # Simple Random Walk
        randomIndex = randint(0, len(connectedNodes)-1)
        nextNode = connectedNodes[randomIndex]
        return nextNode

    def chooseNextNode(self, connectedNodes):
        if len(connectedNodes) == 0:
            return None

        randomWalkType = self.estimator.randomWalkType()
        if randomWalkType == "simple":
            return self.chooseNextNodeRandomly(connectedNodes)
        elif randomWalkType == "weighted":
            return self.chooseNextNodeRandomlyUsingWeights(connectedNodes)

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