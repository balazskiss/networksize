import csv
from time import strftime
from walker import *
from crawler import *
from estimator import *


class Experiment(RandomWalkerDelegate):
    def __init__(self, crawler, type, name, return_limit=0, step_limit=0):
        self.return_limit = return_limit
        self.step_limit = step_limit
        self.crawler = crawler
        self.name = name

        if type == "node":
            self.estimator = NodeEstimator(self.crawler)
        elif type == "edge":
            self.estimator = EdgeEstimator(self.crawler)

        self.__reset()


    def __reset(self):
        self.return_times = []
        self.walker = None
        self.start_node = None
        random.seed(time.time())

    def __init_csv_file(self):
        if self.csv_file_name is not None:
            with open(self.csv_file_name, 'w') as csvfile:
                fieldnames = ['Return N', 'Date', 'Steps', 'Return Avg', 'Total Steps', 'Visited Nodes', 'Estimate']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    def __append_to_csv_file(self, returns, step, return_time_avg, estimate, num_nodes):
        with open(self.csv_file_name, 'a') as csvfile:
            fieldnames = ['Return N', 'Date', 'Steps', 'Return Avg', 'Total Steps', 'Visited Nodes', 'Estimate']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'Return N': returns,
                'Date': strftime("%Y-%m-%d %H:%M:%S"),
                'Steps': step,
                'Return Avg': return_time_avg,
                'Total Steps': self.__total_steps(),
                'Visited Nodes': num_nodes,
                'Estimate': estimate,
            })

    def __write_to_degdist_file(self, deg_dist):
        with open(self.degdist_file_name, 'w') as degdistfile:
            degdistfile.write(json.dumps(deg_dist))

    def __total_steps(self):
        return sum(self.return_times)

    def __display_progess(self, percent, returns, estimate):
        progress = int(percent*100.0)
        print '\r[{0}{1}] {2}%, {3} returns, estimate: {4}'.format('#'*(progress/10), ' '*(10-progress/10), progress, returns, estimate),

    def run(self, repeat=1):
        for i in range(1,repeat+1):
            self.__reset()
            print("Experiment "+str(i))
            exp_name = self.name+str(i)
            self.csv_file_name = exp_name + ".csv"
            self.degdist_file_name = exp_name + ".degdist.json"
            self.__init_csv_file()

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
        # estimate = (estimate*2)/self.walker.average_degree()

        self.__append_to_csv_file(len(self.return_times), step, return_time_average, estimate, len(self.walker.visited_nodes))
        self.__write_to_degdist_file(self.walker.degree_distribution())

        percent = None
        stop = False

        if self.return_limit != 0:
            percent = float(len(self.return_times))/float(self.return_limit)
            if len(self.return_times) == self.return_limit:
                stop = True

        if self.step_limit != 0:
            steps = self.__total_steps()
            if percent is None:
                percent = float(steps)/float(self.step_limit)
            if steps >= self.step_limit:
                stop = True

        self.__display_progess(percent, len(self.return_times), estimate)
        if stop:
            self.walker.stop()
            print("\n")
