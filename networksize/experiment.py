import csv
import time

from walker import *
from crawler import *
from estimator import *

class Experiment(RandomWalkerDelegate):
    def __init__(self, graph, name, returnLimit=0):
        self.returnTimes = []
        self.returnLimit = returnLimit
        self.graph = graph
        self.name = name

        random.seed(time.time())

        snap.PrintInfo(self.graph, "Network Info")

        self.outputFile = self.name + ".csv"

        if self.outputFile is not None:
            with open(self.outputFile, 'w') as csvfile:
                fieldnames = ['Return N', 'Steps', 'Return Avg', 'Estimate']
                self.writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                self.writer.writeheader()

    def printGraphInfo(self, file):
        print("Printing Graph Info")
        snap.PrintInfo(self.graph, "Python type PNGraph", file, True)

    def printFullGraphInfo(self, file):
        print("Printing Full Graph Info")
        snap.PrintInfo(self.graph, "Python type PNGraph", file, False)

    def plotDegreeDistribution(self, file):
        print("Plotting Degree Distribution")
        snap.PlotOutDegDistr(self.graph, file, "Network - out-degree Distribution")

    def visualiseGraph(self, file, title):
        snap.DrawGViz(self.graph, snap.gvlDot, file, title)

    def __updateProgress(self, progress):
        print '\r[{0}] {1}%'.format('#'*(progress/10), progress),

    def run(self):
        self.crawler = SnapGraphCrawler(self.graph)
        self.estimator = NodeEstimator(self.crawler)
        self.startNode = self.crawler.getHighestDegreeNode()
        print "Starting from node " + str(self.startNode) + " (degree:" + str(self.crawler.getDegreeOfNode(self.startNode)) + ")"
        self.walker = RandomWalker(self.crawler, self.estimator, self.startNode)
        self.walker.delegate = self
        self.walker.walk()

    # Walker Delegate

    def returnedToStartNode(self, step):
        self.returnTimes.append(step)
        returnTimeAverage = sum(self.returnTimes)/float(len(self.returnTimes))
        estimate = returnTimeAverage * (self.estimator.getNodeWeight(self.startNode)/2)

        with open(self.outputFile, 'a') as csvfile:
            fieldnames = ['Return N', 'Steps', 'Return Avg', 'Estimate']
            self.writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            field1 = len(self.returnTimes)
            field2 = step
            field3 = returnTimeAverage
            field4 = estimate
            self.writer.writerow({'Return N': field1, 'Steps': field2, 'Return Avg': field3, 'Estimate': field4})

        self.__updateProgress(int(float(len(self.returnTimes))/float(self.returnLimit)*100.0))
        if len(self.returnTimes) == self.returnLimit:
            self.walker.stop()




