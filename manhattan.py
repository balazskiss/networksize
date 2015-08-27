import snap
import networksize

if __name__ == '__main__':
    network = snap.GenGrid(snap.PUNGraph, 225, 11, False)
    networksize.print_graph_info(network)
    crawler = networksize.SnapGraphCrawler(network)
    networksize.Experiment(crawler, "edge", "results/manhattan-edge", return_limit=1000).run()
    networksize.Experiment(crawler, "node", "results/manhattan-node", return_limit=1000).run()
