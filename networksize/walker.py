import snap
import random

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