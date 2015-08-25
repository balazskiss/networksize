import snap
import networksize

if __name__ == '__main__':
    Rnd = snap.TRnd();

    # Generates an Erdos-Renyi random graph
    # network = snap.GenRndGnm(snap.PUNGraph, 1000000, 5000000, False)
    # name = "randomgraph"

    # Generates a random scale-free, undirected graph using the Geometric Preferential Attachment model
    # network = snap.GenGeoPrefAttach(100000, 1000000, 0.25, Rnd)
    # name = "geoprefattach"

    # Generates an undirected graph with a power-law degree distribution using Barabasi-Albert model
    network = snap.GenPrefAttach(10000, 10, Rnd)
    name = "barabasi"

    networksize.print_graph_info(network)
    # networksize.plotDegreeDistribution(network, "randomgraph-degree")
    # networksize.visualiseGraph(network, "randomgraph-graph.png", "Random Graph")

    i = 1
    while i<=10:
        print("Experiment "+str(i))
        crawler = networksize.SnapGraphCrawler(network)
        networksize.Experiment(crawler, "node", name+str(i), 1000).run()
        i+=1