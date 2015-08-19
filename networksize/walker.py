import snap
import random
from random import randint


class RandomWalkerDelegate:

    def __init__(self):
        pass

    def returned_to_start_node(self, step):
        pass


class RandomWalker:

    def __init__(self, crawler, estimator, start_node):
        self.delegate = None
        self.crawler = crawler
        self.estimator = estimator
        self.start_node = start_node
        self.current_node = None
        self.network = snap.TNEANet.New()
        self.running = False
        self.visited_nodes = set()
        self.step = 0

    def choose_next_node_randomly_using_weights(self):
        connected_nodes_with_degrees = self.crawler.getConnectedNodesWithDegrees(self.current_node)
        du = len(connected_nodes_with_degrees)

        # Weighted Random Walk
        rnd = random.random()
        psum = 0.0
        w_node = self.estimator.getNodeWeight(self.current_node, du, connected_nodes_with_degrees)
        for neighbour in connected_nodes_with_degrees:
            dv = connected_nodes_with_degrees[neighbour]
            w_edge = self.estimator.getEdgeWeight(self.current_node, neighbour, du, dv)
            p = w_edge / w_node
            psum += p
            if rnd <= psum:
                return neighbour
        return None

    def choose_next_node_randomly(self):
        connected_nodes = self.crawler.getConnectedNodes(self.current_node)

        # Simple Random Walk
        random_index = randint(0, len(connected_nodes)-1)
        next_node = connected_nodes[random_index]
        return next_node

    def choose_next_node(self):
        random_walk_type = self.estimator.randomWalkType()
        if random_walk_type == "simple":
            return self.choose_next_node_randomly()
        elif random_walk_type == "weighted":
            return self.choose_next_node_randomly_using_weights()

    def walk(self):
        self.running = True
        self.step = 0
        self.current_node = self.start_node
        self.visited_nodes.add(self.current_node)
        while self.running:
            # Choose next node
            self.current_node = self.choose_next_node()
            self.visited_nodes.add(self.current_node)
            self.step += 1

            if self.current_node == self.start_node:
                if self.delegate is not None:
                    self.delegate.returned_to_start_node(self.step)
                self.step = 0

    def stop(self):
        self.running = False