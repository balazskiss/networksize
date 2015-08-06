import snap
import threading
import time

class GraphImporter:
    def __init__(self, file, lineCount):
        self.file = file
        self.lineCount = lineCount
        self.linesToRead = lineCount

    def addNode(self, network, node):
            try:
                network.AddNode(node)
            # Ignores if node already exists
            except RuntimeError:
                pass

    def addEdge(self, network, node1, node2):
            self.addNode(network, node1)
            self.addNode(network, node2)
            try:
                network.AddEdge(node1,node2)
            # Ignores if edge already exists
            except RuntimeError:
                pass

    def displayProgess(self, progress, secondsRemaining):
        progress = int(progress*100.0)
        timeRemaining = str(secondsRemaining) + " secs"
        if secondsRemaining > 60:
            minsRemaining = secondsRemaining/60
            if minsRemaining == 1:
                timeRemaining = str(minsRemaining) + " min"
            else:
                timeRemaining = str(minsRemaining) + " mins"

        print '\r[{0}{1}] {2}%, {3} remaining'.format('#'*(progress/10), ' '*(10-progress/10), progress, timeRemaining),

    def progress(self):
        startTime = time.time()
        self.stoppedProgressThread = threading.Event()
        while not self.stoppedProgressThread.wait(1):
            percent = float(self.currentLine)/float(self.linesToRead)
            now = time.time()
            secondsElapsed = int(now - startTime)
            secondsRemaining = int(float(secondsElapsed)/percent - secondsElapsed)
            self.displayProgess(percent, secondsRemaining)

    def importGraph(self, importWholeGraph = True, lineLimit = 0):
        if not importWholeGraph:
            self.linesToRead = lineLimit

        self.network = snap.TUNGraph.New(max(1000, self.linesToRead/1000), self.linesToRead)

        t = threading.Thread(target=self.progress)
        t.start()

        print("Importing graph...")
        self.currentLine = 0
        with open(self.file) as f:
            for line in f:
                nodes = line.split('\t')
                self.addEdge(self.network,int(nodes[0]),int(nodes[1]))
                self.currentLine += 1
                if not importWholeGraph and self.currentLine==lineLimit:
                    break

        self.stoppedProgressThread.set()

        print("\nGraph has been imported")
        snap.PrintInfo(self.network, "Network Info")
        return self.network