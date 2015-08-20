import csv
from walker import *
from crawler import *
from estimator import *


class Experiment(RandomWalkerDelegate):
    def __init__(self, crawler, type, name, return_limit=0):
        super(Experiment, self).__init__()
        self.return_times = []
        self.return_limit = return_limit
        self.crawler = crawler
        self.name = name
        self.walker = None
        self.start_node = None

        if type == "node":
            self.estimator = NodeEstimator(self.crawler)
        elif type == "edge":
            self.estimator = EdgeEstimator(self.crawler)

        random.seed(time.time())

        self.output_file = self.name + ".csv"
        self.init_output_file()

    def init_output_file(self):
        if self.output_file is not None:
            with open(self.output_file, 'w') as csvfile:
                fieldnames = ['Return N', 'Steps', 'Return Avg', 'Estimate', 'Number of Nodes', 'Degree Distribution']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    def append_to_output_file(self, returns, step, return_time_avg, estimate, num_nodes, deg_dist):
        with open(self.output_file, 'a') as csvfile:
            fieldnames = ['Return N', 'Steps', 'Return Avg', 'Estimate', 'Number of Nodes', 'Degree Distribution']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'Return N': returns,
                'Steps': step,
                'Return Avg': return_time_avg,
                'Estimate': estimate,
                'Number of Nodes': num_nodes,
                'Degree Distribution': deg_dist
            })

    def display_progess(self, percent, returns, estimate):
        progress = int(percent*100.0)
        print '\r[{0}{1}] {2}%, {3} returns, estimate: {4}'.format('#'*(progress/10), ' '*(10-progress/10), progress, returns, estimate),

    def run(self):
        self.start_node = self.crawler.get_highest_degree_node()
        print "Starting from node " + str(self.start_node) + " (degree:" + str(self.crawler.get_degree_of_node(self.start_node)) + ")"
        self.walker = RandomWalker(self.crawler, self.estimator, self.start_node)
        self.walker.delegate = self
        self.walker.walk()

    # Walker Delegate

    def returned_to_start_node(self, step):
        self.return_times.append(step)
        return_time_average = sum(self.return_times)/float(len(self.return_times))
        estimate = int(return_time_average * (self.estimator.get_node_weight(self.start_node)/2))

        self.append_to_output_file(len(self.return_times), step, return_time_average, estimate, len(self.walker.visited_nodes), self.walker.degree_distribution())

        percent = float(len(self.return_times))/float(self.return_limit)
        self.display_progess(percent, len(self.return_times), estimate)

        if len(self.return_times) == self.return_limit:
            self.walker.stop()
            print("\n")
