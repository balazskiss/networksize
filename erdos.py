import snap
import networksize

if __name__ == '__main__':
    # Generates an Erdos-Renyi random graph
    network = snap.GenRndGnm(snap.PUNGraph, 1000000, 10000000, False)
    networksize.print_graph_info(network)
    crawler = networksize.SnapGraphCrawler(network)
    networksize.Experiment(crawler, "edge", "results/erdos-edge", return_limit=100).run(10)
    networksize.Experiment(crawler, "node", "results/erdos-node", return_limit=100).run(10)
