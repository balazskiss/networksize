class Estimator:
    def __init__(self, crawler):
        self.crawler = crawler

    def random_walk_type(self):
        return "weighted"

    def get_edge_weight(self, u, v, du=None, dv=None):
        pass

    def get_node_weight(self, u, du=None, connected_nodes_with_degrees=None):
        pass


class EdgeEstimator(Estimator):
    def random_walk_type(self):
        return "simple"

    def get_edge_weight(self, u, v, du=None, dv=None):
        return 1.0

    def get_node_weight(self, u, du=None, connected_nodes_with_degrees=None):
        return self.crawler.get_degree_of_node(u)


class NodeEstimator(Estimator):
    def get_edge_weight(self, u, v, du=None, dv=None):
        if du is None:
            du = self.crawler.get_degree_of_node(u)
        if dv is None:
            dv = self.crawler.get_degree_of_node(v)
        return (1.0 / du) + (1.0 / dv)

    def get_node_weight(self, u, du=None, connected_nodes_with_degrees=None):
        if du is None:
            du = self.crawler.get_degree_of_node(u)
        if connected_nodes_with_degrees is None:
            connected_nodes_with_degrees = self.crawler.get_connected_nodes_with_degrees(u)
        wsum = 0.0
        for node in connected_nodes_with_degrees:
            wsum += self.get_edge_weight(u, node, du, connected_nodes_with_degrees[node])
        return wsum
