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
        self.visited_nodes = {}
        self.step = 0

    def __choose_next_node_randomly_using_weights(self):
        connected_nodes_with_degrees = self.crawler.get_connected_nodes_with_degrees(self.current_node)
        du = len(connected_nodes_with_degrees)

        # Weighted Random Walk
        rnd = random.random()
        psum = 0.0
        w_node = self.estimator.get_node_weight(self.current_node, du, connected_nodes_with_degrees)
        for neighbour in connected_nodes_with_degrees:
            dv = connected_nodes_with_degrees[neighbour]
            w_edge = self.estimator.get_edge_weight(self.current_node, neighbour, du, dv)
            p = w_edge / w_node
            psum += p
            if rnd <= psum:
                return neighbour, dv
        return None

    def __choose_next_node_randomly(self):
        connected_nodes = self.crawler.get_connected_nodes(self.current_node)
        du = len(connected_nodes)

        # Simple Random Walk
        random_index = randint(0, du-1)
        next_node = connected_nodes[random_index]
        return next_node, du

    def __choose_next_node(self):
        random_walk_type = self.estimator.random_walk_type()
        if random_walk_type == "simple":
            return self.__choose_next_node_randomly()
        elif random_walk_type == "weighted":
            return self.__choose_next_node_randomly_using_weights()

    def walk(self):
        self.running = True
        self.step = 0
        self.current_node = self.start_node
        self.visited_nodes[self.current_node] = self.crawler.get_degree_of_node(self.current_node)
        while self.running:
            # Choose next node
            node, degree = self.__choose_next_node()
            self.current_node = node
            self.visited_nodes[node] = degree
            self.step += 1

            if self.current_node == self.start_node:
                if self.delegate is not None:
                    self.delegate.returned_to_start_node(self.step)
                self.step = 0

    def stop(self):
        self.running = False

    def degree_distribution(self):
        dd = {}
        for node, degree in self.visited_nodes.iteritems():
            if degree not in dd:
                dd[degree] = 1
            else:
                dd[degree] += 1
        return dd

    def average_degree(self):
        sum = 0
        count = 0
        for node, degree in self.visited_nodes.iteritems():
            sum = sum + degree
            count = count + 1
        return sum/float(count)