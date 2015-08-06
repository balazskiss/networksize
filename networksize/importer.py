import snap

class GraphImporter:
    def __init__(self, file, limit):
        self.file = file
        self.limit = limit
        self.network = snap.TUNGraph.New(1000000, 10000000)

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
            # Ignores if node already exists
            except RuntimeError:
                pass

    def importGraph(self):
        print("Importing graph...")
        i = 0
        with open(self.file) as f:
            for line in f:
                nodes = line.split('\t')
                self.addEdge(self.network,int(nodes[0]),int(nodes[1]))
                i+= 1
                if i%1000000 == 0:
                    print(i)
                    snap.PrintInfo(self.network, "Network Info")
                if i==self.limit:
                    break
        print("Graph has been imported")
        snap.PrintInfo(self.network, "Network Info")
        return self.network