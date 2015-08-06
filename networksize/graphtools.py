import snap

def printGraphInfo(graph, file):
    print("Printing Graph Info")
    snap.PrintInfo(graph, "Python type PNGraph", file, True)

def printFullGraphInfo(graph, file):
    print("Printing Full Graph Info")
    snap.PrintInfo(graph, "Python type PNGraph", file, False)

def plotDegreeDistribution(graph, file):
    print("Plotting Degree Distribution")
    snap.PlotOutDegDistr(graph, file, "Network - out-degree Distribution")

def visualiseGraph(graph, file, title):
    snap.DrawGViz(graph, snap.gvlDot, file, title)