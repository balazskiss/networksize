import csv
import time

from walker import *
from crawler import *
from estimator import *

class Experiment(RandomWalkerDelegate):
    def __init__(self, crawler, type, name, returnLimit=0):
        self.returnTimes = []
        self.returnLimit = returnLimit
        self.crawler = crawler
        self.name = name

        if type == "node":
            self.estimator = NodeEstimator(self.crawler)
        elif type == "edge":
            self.estimator = EdgeEstimator(self.crawler)

        random.seed(time.time())

        self.outputFile = self.name + ".csv"

        if self.outputFile is not None:
            with open(self.outputFile, 'w') as csvfile:
                fieldnames = ['Return N', 'Steps', 'Return Avg', 'Estimate', 'Number of Nodes']
                self.writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                self.writer.writeheader()

    def displayProgess(self, percent, returns, estimate):
        progress = int(percent*100.0)
        print '\r[{0}{1}] {2}%, {3} returns, estimate: {4}'.format('#'*(progress/10), ' '*(10-progress/10), progress, returns, estimate),

    def run(self):
        self.startNode = self.crawler.getHighestDegreeNode()
        print "Starting from node " + str(self.startNode) + " (degree:" + str(self.crawler.getDegreeOfNode(self.startNode)) + ")"
        self.walker = RandomWalker(self.crawler, self.estimator, self.startNode)
        self.walker.delegate = self
        self.walker.walk()

    # Walker Delegate

    def returnedToStartNode(self, step):
        self.returnTimes.append(step)
        returnTimeAverage = sum(self.returnTimes)/float(len(self.returnTimes))
        estimate = int(returnTimeAverage * (self.estimator.getNodeWeight(self.startNode)/2))

        with open(self.outputFile, 'a') as csvfile:
            fieldnames = ['Return N', 'Steps', 'Return Avg', 'Estimate', 'Number of Nodes']
            self.writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            field1 = len(self.returnTimes)
            field2 = step
            field3 = returnTimeAverage
            field4 = estimate
            self.writer.writerow({'Return N': field1, 'Steps': field2, 'Return Avg': field3, 'Estimate': field4,'Number of Nodes':len(self.walker.visitedNodes)})

        percent = float(len(self.returnTimes))/float(self.returnLimit)
        self.displayProgess(percent, len(self.returnTimes), estimate)

        if len(self.returnTimes) == self.returnLimit:
            self.walker.stop()
            print("\n")





