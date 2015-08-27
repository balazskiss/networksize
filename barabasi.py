import snap, networksize

if __name__ == '__main__':
    # Generates an undirected graph with a power-law degree distribution using Barabasi-Albert model
    network = snap.GenPrefAttach(1000000, 10, snap.TRnd())
    networksize.print_graph_info(network)
    crawler = networksize.SnapGraphCrawler(network)
    networksize.Experiment(crawler, "edge", "results/barabasi-edge", step_limit=1000000).run(10)
    networksize.Experiment(crawler, "node", "results/barabasi-node", step_limit=1000000).run(10)
