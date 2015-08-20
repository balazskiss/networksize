import snap
import threading
import time


class GraphImporter:
    def __init__(self, file, line_count):
        self.file = file
        self.lineCount = line_count
        self.lines_to_read = line_count
        self.network = None
        self.stopped_progress_thread = None
        self.current_line = 0

    def add_node(self, network, node):
            try:
                network.AddNode(node)
            # Ignores if node already exists
            except RuntimeError:
                pass

    def add_edge(self, network, node1, node2):
            self.add_node(network, node1)
            self.add_node(network, node2)
            try:
                network.AddEdge(node1, node2)
            # Ignores if edge already exists
            except RuntimeError:
                pass

    def display_progess(self, progress, seconds_remaining):
        progress = int(progress*100.0)
        time_remaining = str(seconds_remaining) + " secs"
        if seconds_remaining > 60:
            mins_remaining = seconds_remaining / 60
            if 1 == mins_remaining:
                time_remaining = str(mins_remaining) + " min"
            else:
                time_remaining = str(mins_remaining) + " mins"

        print '\r[{0}{1}] {2}%, {3} remaining'.format('#'*(progress/10), ' '*(10-progress/10), progress, time_remaining),

    def progress(self):
        start_time = time.time()
        self.stopped_progress_thread = threading.Event()
        while not self.stopped_progress_thread.wait(1):
            percent = float(self.current_line)/float(self.lines_to_read)
            now = time.time()
            seconds_elapsed = int(now - start_time)
            seconds_remaining = int(float(seconds_elapsed)/percent - seconds_elapsed)
            self.display_progess(percent, seconds_remaining)

    def import_graph(self, import_whole_graph=True, line_limit=0):
        if not import_whole_graph:
            self.lines_to_read = line_limit

        self.network = snap.TUNGraph.New(max(1000, self.lines_to_read/1000), self.lines_to_read)

        t = threading.Thread(target=self.progress)
        t.start()

        print("Importing graph...")
        self.current_line = 0
        with open(self.file) as f:
            for line in f:
                nodes = line.split('\t')
                self.add_edge(self.network, int(nodes[0]), int(nodes[1]))
                self.current_line += 1
                if not import_whole_graph and self.current_line == line_limit:
                    break

        self.stopped_progress_thread.set()

        print("\nGraph has been imported")
        snap.PrintInfo(self.network, "Network Info")
        return self.network
