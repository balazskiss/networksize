import snap


def print_graph_info(graph, file=None):
    print("Printing Graph Info")
    if file is None:
        snap.PrintInfo(graph, "Python type PNGraph")
    else:
        snap.PrintInfo(graph, "Python type PNGraph", file, True)


def print_full_graph_info(graph, file):
    print("Printing Full Graph Info")
    snap.PrintInfo(graph, "Python type PNGraph", file, False)


def plot_degree_distribution(graph, file):
    print("Plotting Degree Distribution")
    snap.PlotOutDegDistr(graph, file, "Network - out-degree Distribution")


def visualise_graph(graph, file, title):
    snap.DrawGViz(graph, snap.gvlDot, file, title)
